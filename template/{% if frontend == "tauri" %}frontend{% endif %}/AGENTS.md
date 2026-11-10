## Development

`ion repo dev` runs `pnpm tauri dev`: Vite serves the front on http://localhost:1420 and Tauri opens
the app's window on it, rebuilding the Rust core of `src-tauri/` at each change. On Linux and WSL
the window needs WebKitGTK (`ion repo install` says how); Windows and macOS bring their webview.

- Front: `src/`, React; the core's commands are called through `src/core.ts` only.
- Core: `src-tauri/src/lib.rs`, one `#[tauri::command]` per action, registered in
  `generate_handler!`; what the window may call is listed in `src-tauri/capabilities/`.
- Installers: `pnpm tauri build` on the system they are for (`.msi`/`.exe` on Windows,
  `.dmg`/`.app` on macOS); the CI builds both.

## Documentation

- [Tauri 2](https://v2.tauri.app/start/)
- [Tauri commands](https://v2.tauri.app/develop/calling-rust/)
- [Tauri capabilities](https://v2.tauri.app/security/capabilities/)
- [Vite](https://vite.dev/guide/)
- [React](https://react.dev/reference/react)
- [Vitest](https://vitest.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
