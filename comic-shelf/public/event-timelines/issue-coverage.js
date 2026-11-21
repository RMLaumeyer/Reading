export function routeCoverage(steps, evidence, booksByIsbn, queue) {
  const editions = Object.entries(evidence.editions).flatMap(([isbn, edition]) => {
    const book = booksByIsbn.get(isbn);
    return book ? [{ book, edition }] : [];
  });
  const core = steps.filter(step => step.role === 'Core');
  const required = [...new Set(core.flatMap(step => evidence.core[step.id] ?? []))];
  const available = new Set(editions.flatMap(({ edition }) => edition.issueKeys));
  const finished = new Set(editions.flatMap(({ book, edition }) =>
    queue[book.id]?.status === 'finished' ? edition.issueKeys : [],
  ));
  const missing = required.filter(issue => !available.has(issue));
  const stage = core.find(step => evidence.core[step.id]?.some(issue => !finished.has(issue)));
  const nextIssue = stage && evidence.core[stage.id].find(issue => !finished.has(issue));
  const candidates = nextIssue ? editions.filter(({ edition }) => edition.issueKeys.includes(nextIssue)) : [];
  const remaining = new Set(required.filter(issue => !finished.has(issue)));
  const countNew = ({ edition }) => edition.issueKeys.filter(issue => remaining.has(issue)).length;
  candidates.sort((a, b) =>
    Number(b.book.hooplaListed) - Number(a.book.hooplaListed) || countNew(b) - countNew(a),
  );
  const next = candidates[0];
  return {
    total: required.length,
    read: required.length - remaining.size,
    missing,
    fullyMappedStages: core.filter(step => evidence.core[step.id]?.every(issue => available.has(issue))).length,
    stage,
    nextIssue,
    next,
    adds: next ? next.edition.issueKeys.filter(issue => remaining.has(issue)) : [],
    repeats: next ? next.edition.issueKeys.filter(issue => finished.has(issue)) : [],
  };
}
