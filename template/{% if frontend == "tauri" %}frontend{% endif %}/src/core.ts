// The Rust core's commands (src-tauri/src/lib.rs), typed once for the front.
import { invoke } from '@tauri-apps/api/core';

export async function readCoreVersion(): Promise<string> {
  return invoke<string>('core_version');
}
