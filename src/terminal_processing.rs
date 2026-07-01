pub fn clear_screen() {
    // std::process::Command::new("clear");
    clearscreen::clear().expect("failed to clear screen");
}
