// Vinext calls process.exit(0) immediately after building. On Windows, native
// bundler callbacks can still be closing and Node asserts in uv_async teardown.
// Allow those callbacks to finish. Nonzero exits and native errors stay failures.
if (process.platform === 'win32') {
  const originalExit = process.exit.bind(process);
  let scheduled = false;
  process.exit = function (code) {
    const status = code == null ? process.exitCode || 0 : Number(code);
    if (status !== 0) return originalExit(status);
    process.exitCode = 0;
    if (!scheduled) {
      scheduled = true;
      setTimeout(() => originalExit(process.exitCode || 0), 1000).unref();
    }
  };
}
