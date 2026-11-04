"""Apply reviewed synopsis fields without replacing other enrichment fields."""
import copy
import datetime
import json


def initial_record(checked_at):
    """UI-complete empty metadata for an explicitly reviewed synopsis only."""
    datetime.date.fromisoformat(checked_at)
    return {'level': 'basic', 'summary': '', 'pages': None, 'pagesSource': '',
            'coverSource': '', 'checkedAt': checked_at, 'sources': [],
            'characters': [], 'stories': [], 'issueKeys': [],
            'readingPath': {'name': '', 'position': 0, 'alternative': False,
                            'note': 'Reading order has not been checked.'},
            'contentsNote': 'Collected issues and supplemental material have not been indexed.',
            'startingPoint': False}


def apply(books, path):
    result = copy.deepcopy(books)
    if path.exists():
        for key, patch in json.loads(path.read_text(encoding='utf-8'))['books'].items():
            if key not in result and patch.get('initializeMissing'):
                marker = patch['initializeMissing']
                if marker.get('kind') != 'reviewed_synopsis_only':
                    raise ValueError('Unknown approved synopsis initialization')
                result[key] = initial_record(marker['checkedAt'])
            if key in result:
                for field in ('summary', 'synopsisReview'):
                    result[key][field] = patch[field]
                for source in patch['sources']:
                    if not any(s.get('url') == source.get('url') for s in result[key].get('sources', [])):
                        result[key].setdefault('sources', []).append(source)
    return result
