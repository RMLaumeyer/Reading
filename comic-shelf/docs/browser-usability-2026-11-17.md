# Browser usability check — November 17, 2026

Checked the saved production app at http://localhost:5173/ in the in-app browser.

Fixed two queue recovery issues in app/shelf.tsx:
- Reset now clears the queue filter as well as catalog filters and pagination.
- Empty queue views explain how to add books and offer Browse all books, which clears queue and catalog restrictions and returns to page one.

Verified in the rebuilt app:
- Kraven search returned 34 matches; pagination reached page 2 of 2.
- Spider-Man character selection and clearing search returned 758 matches.
- Kraven's Last Hunt details opened with synopsis, sources, overlap alternatives and next-in-run navigation; the close control returned to results.
- Borrowing links point to exact Hoopla title 14056957 and its OCLS grouped record. Link destinations were inspected; external availability and borrowing were not checked.
- Empty saved queue displayed the new guidance; Browse all books returned 4,000 records.
- Reset after selecting My queue returned Show books to All books.
- A nonexistent search recovered through Search the full catalog and Clear filters.
- At a 390 by 844 viewport, the shelf used a single column and document width stayed within the viewport (375 pixels). Restored the default viewport afterward.

Validation: npm run typecheck and npm run build passed, including static export. Earlier queue persistence, guide sharing and cross-tab status checks are documented in README.md. No saved reading statuses were changed during this pass.
