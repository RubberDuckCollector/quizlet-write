use console::style;
use std::fs;
use std::{thread, time};
use std::collections::HashMap;

fn clear_screen() {
    // std::process::Command::new("clear");
    clearscreen::clear().expect("failed to clear screen");
}

fn render_cards(filepath: &str) -> HashMap<&str, &str> {
    let mut words: HashMap<&str, &str> = HashMap::new();

    let result = fs::read_to_string(filepath);
    match result {
        Ok(v) => println!("{}", v),
        Err(e) => panic!("Error while reading file: {}\n{}", filepath, e)
    }

    // TODO: loop through each line of the file
    // strip whitespace
    // split on |
    // insert each 2 strings on a given line into the hashmap

    words
}

fn quiz() {

}

fn main() {
    clear_screen();

    // thread::sleep(time::Duration::from_secs(1));

    println!("{:?}", render_cards("/Users/luna/flash-cards/languages/basque/self-study/family_members.txt"));

}
