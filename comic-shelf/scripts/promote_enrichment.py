"""Guarded local promotion/rollback. Requires human-reviewed staging; no remote deployment."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import tempfile
import stage_enrichment as stage


@contextmanager
def collector_lock(root):
    import msvcrt
    with (root/'data/enrichment.lock').open('a+b') as stream:
        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def replace(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        stream.write(data)
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode('utf-8')


def promote(root, package, queue, decisions, receipt):
    manifest = json.loads((package/'manifest.json').read_text(encoding='utf-8'))
    if manifest['previewOnly'] or not manifest['changes']:
        raise ValueError('Only nonempty human-approved packages may be promoted')
    if stage.digest((root/'public/enrichment.json').read_bytes()) != manifest['beforeSha256']:
        raise ValueError('Live enrichment changed; rebuild staging')
    if stage.digest((package/'enrichment.staged.json').read_bytes()) != manifest['stagedSha256']:
        raise ValueError('Staged payload changed')
    # Rebuild from current queue/decisions/catalog. Approval withdrawal or changed
    # sources invalidates the package even if the stored payload was untouched.
    with tempfile.TemporaryDirectory() as directory:
        checked = stage.build(queue, decisions, root/'public/catalog.json', root/'public/enrichment.json', Path(directory)/'check',
                              initialize_isbns=manifest.get('initializeIsbns', []))
        for field in ('queueSha256', 'catalogSha256', 'beforeSha256', 'stagedSha256', 'decisionsSha256', 'changes'):
            if checked[field] != manifest[field]:
                raise ValueError('Stale staging inputs: '+field)
    overlay_path = root/'data/approved-synopses.json'
    overlay = json.loads(overlay_path.read_text(encoding='utf-8')) if overlay_path.exists() else {'books': {}}
    for change in manifest['changes']:
        after = change['after']
        key = change['catalogId']
        marker = overlay['books'].get(key, {}).get('initializeMissing')
        if change['before'] is None:
            marker = {'kind': 'reviewed_synopsis_only', 'checkedAt': after['checkedAt']}
        overlay['books'][key] = {k: after[k] for k in ('summary', 'synopsisReview', 'sources')}
        if marker:
            overlay['books'][key]['initializeMissing'] = marker
    payload = (package/'enrichment.staged.json').read_bytes()
    targets = {overlay_path: encoded(overlay), root/'public/enrichment.json': payload}
    if (root/'dist/client').exists():
        targets[root/'dist/client/enrichment.json'] = payload
    receipt.mkdir(exist_ok=False)
    entries = []
    for index, (path, data) in enumerate(targets.items()):
        before = path.read_bytes() if path.exists() else None
        backup = f'{index}.before'
        if before is not None:
            (receipt/backup).write_bytes(before)
        entries.append({'path': path.relative_to(root).as_posix(), 'backup': backup,
                        'beforeSha256': stage.digest(before) if before is not None else None,
                        'afterSha256': stage.digest(data)})
    transaction = {'state': 'prepared', 'files': entries}
    replace(receipt/'receipt.json', encoded(transaction))
    written = []
    try:
        for (path, data), entry in zip(targets.items(), entries):
            # Prevent stale writes after validation; collectors share the lock.
            current = stage.digest(path.read_bytes()) if path.exists() else None
            if current != entry['beforeSha256']:
                raise ValueError('Target changed during promotion')
            replace(path, data)
            written.append(entry)
        transaction['state'] = 'promoted'
        replace(receipt/'receipt.json', encoded(transaction))
    except Exception:
        for entry in reversed(written):
            restore(root, receipt, entry)
        transaction['state'] = 'failed_restored'
        replace(receipt/'receipt.json', encoded(transaction))
        raise
    return transaction


def restore(root, receipt, entry):
    path = (root/entry['path']).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Receipt target leaves project')
    if entry['beforeSha256'] is None:
        path.unlink(missing_ok=True)
    else:
        backup = (receipt/entry['backup']).resolve()
        if not backup.is_relative_to(receipt.resolve()):
            raise ValueError('Backup leaves receipt directory')
        data = backup.read_bytes()
        if stage.digest(data) != entry['beforeSha256']:
            raise ValueError('Backup hash mismatch')
        replace(path, data)


def rollback(root, receipt):
    transaction = json.loads((receipt/'receipt.json').read_text(encoding='utf-8'))
    if transaction['state'] != 'promoted':
        raise ValueError('Receipt is not an active promotion')
    # Validate every file/backup before restoring any file.
    for entry in transaction['files']:
        path = (root/entry['path']).resolve()
        if not path.is_relative_to(root.resolve()) or stage.digest(path.read_bytes()) != entry['afterSha256']:
            raise ValueError('Files changed since promotion; refusing stale rollback')
        if entry['beforeSha256'] is not None:
            backup = (receipt/entry['backup']).resolve()
            if not backup.is_relative_to(receipt.resolve()) or stage.digest(backup.read_bytes()) != entry['beforeSha256']:
                raise ValueError('Invalid rollback backup')
    for entry in reversed(transaction['files']):
        restore(root, receipt, entry)
    transaction['state'] = 'rolled_back'
    replace(receipt/'receipt.json', encoded(transaction))
    return transaction


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--rollback', action='store_true')
    for name in ('package', 'queue', 'decisions'):
        parser.add_argument('--'+name, type=Path)
    args = parser.parse_args()
    if not args.rollback and not all((args.package, args.queue, args.decisions)):
        parser.error('Promotion requires --package, --queue and --decisions')
    with collector_lock(args.root):
        result = rollback(args.root, args.receipt) if args.rollback else promote(args.root, args.package, args.queue, args.decisions, args.receipt)
    print(result['state'])
