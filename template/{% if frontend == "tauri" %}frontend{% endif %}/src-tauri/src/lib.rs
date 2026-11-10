//! The app's core: the commands the front calls (`src/core.ts`), and the window's start.

/// Version of the core, as Cargo.toml gives it.
#[tauri::command]
fn core_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

/// Starts the app: its window, and the commands the front may call.
///
/// # Panics
///
/// When the window cannot be created: the app has nothing to show then.
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![core_version])
        .run(tauri::generate_context!())
        .expect("the app's window could not start");
}

#[cfg(test)]
mod tests {
    use super::core_version;

    #[test]
    fn core_version_is_the_crates() {
        assert_eq!(core_version(), env!("CARGO_PKG_VERSION"));
    }
}
