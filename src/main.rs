use console::style;
use std::{thread, time};

fn clear_screen() {
    // std::process::Command::new("clear");
    clearscreen::clear().expect("failed to clear screen");
}

fn main() {
    // clear_screen();

    let ten_millis = time::Duration::from_millis(10);
    let now = time::Instant::now();

    thread::sleep(ten_millis);

    assert!(now.elapsed() >= ten_millis);
}
