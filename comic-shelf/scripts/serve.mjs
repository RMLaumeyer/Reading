// Zero-dependency local server. Only compiled public files are exposed.
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { enrichmentApi } from './enrichment_api.mjs';
const api = enrichmentApi(fileURLToPath(new URL('../', import.meta.url)));
const root = path.resolve(
  fileURLToPath(new URL('../dist/client/', import.meta.url)),
);
const port = 5173;
await stat(path.join(root, 'index.html'));
const types = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.txt': 'text/plain; charset=utf-8',
};
const server = http.createServer(async (req, res) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'no-referrer');
  try {
    if (await api(req, res, new URL(req.url, 'http://127.0.0.1'))) return;
  } catch { res.writeHead(500); res.end('Enrichment service unavailable'); return; }
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405);
    res.end();
    return;
  }
  try {
    const url = new URL(req.url, 'http://127.0.0.1');
    if (url.pathname === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ app: 'panel-comic-shelf' }));
      return;
    }
    const name = decodeURIComponent(url.pathname);
    if (name.includes('\\') || name.includes('\0')) {
      res.writeHead(400);
      res.end();
      return;
    }
    let file = path.resolve(root, '.' + (name === '/' ? '/index.html' : name));
    if (!file.startsWith(root + path.sep)) {
      res.writeHead(403);
      res.end();
      return;
    }
    let info = await stat(file);
    if (info.isDirectory()) {
      file = path.join(file, 'index.html');
      info = await stat(file);
    }
    if (!info.isFile()) {
      res.writeHead(404);
      res.end();
      return;
    }
    res.writeHead(200, {
      'Content-Type': types[path.extname(file)] ?? 'application/octet-stream',
      'Cache-Control': 'no-cache',
      'Content-Length': info.size,
    });
    res.end(req.method === 'HEAD' ? undefined : await readFile(file));
  } catch {
    res.writeHead(404);
    res.end('Not found');
  }
});
server.on('error', (error) => {
  console.error(
    error.code === 'EADDRINUSE'
      ? 'Port 5173 is already in use. Close the other app or the development preview.'
      : error.message,
  );
  process.exit(1);
});
server.listen(port, '127.0.0.1', () =>
  console.log(`Panel is running at http://localhost:${port}/`),
);
