"""Apply reviewed synopsis fields without replacing other enrichment fields."""
import copy
import json


def apply(books, path):
    result = copy.deepcopy(books)
    if path.exists():
        for key, patch in json.loads(path.read_text(encoding='utf-8'))['books'].items():
            if key in result:
                for field in ('summary', 'synopsisReview'):
                    result[key][field] = patch[field]
                for source in patch['sources']:
                    if not any(s.get('url') == source.get('url') for s in result[key].get('sources', [])):
                        result[key].setdefault('sources', []).append(source)
    return result
