import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

// The address the app's window loads in development (`devUrl` of src-tauri/tauri.conf.json).
const DEV_PORT = 1420;

// https://v2.tauri.app/start/frontend/vite/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // Tauri's own messages stay readable above Vite's.
  clearScreen: false,
  server: {
    port: DEV_PORT,
    strictPort: true,
    // The Rust core is rebuilt by `tauri dev`, not reloaded by Vite.
    watch: { ignored: ['**/src-tauri/**'] },
  },
  build: {
    // The webviews Tauri runs on: WebView2 (Chromium) on Windows, WebKit on macOS.
    target: process.env.TAURI_ENV_PLATFORM === 'windows' ? 'chrome120' : 'safari16',
  },
});
