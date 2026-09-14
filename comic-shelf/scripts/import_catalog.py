"""Import the user's CSV snapshot without changing source files."""
import csv
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    with (ROOT.parent / 'OCLS_Marvel_Combined.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    books = [dict(id=r['Link'].rsplit('/',1)[-1], title=r['Title'], author=r['Author'], isbn=r['ISBN'], publisher=r['Publisher'], publication=r['Publish Date'], format=r['Format'], catalogUrl=r['Link'], holdings=r['Location & Call Number'], hooplaListed='hoopla' in r['Location & Call Number'].lower()) for r in rows]
    assert len({b['id'] for b in books}) == len(books)
    (ROOT/'public/catalog.json').write_text(json.dumps({'importedAt':'2026-09-08','books':books},ensure_ascii=False),encoding='utf-8')
    print(f'Imported {len(books)} records; {sum(b["hooplaListed"] for b in books)} explicitly list Hoopla.')
if __name__ == '__main__': main()
