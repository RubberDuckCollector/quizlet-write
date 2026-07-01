use std::env;
use std::{thread, time};
use ratatui::crossterm::style::Stylize;

mod file_processing;
mod terminal_processing;

fn main() {
    // TODO: write this proc

    // this will later be a command line argument
    let file_path: &str = "/Users/luna/flash-cards/languages/basque/self-study/family_members.txt";
    match file_processing::validate_cards(file_path) {
        Ok(true) => println!("Validated GOOD"),
        Ok(false) => println!("Validated BAD"),
        Err(e) => {
            eprintln!("Error validating file {}: {}", file_path.red(), e.0);
            std::process::exit(1); // Exit the program with an error code
        }
    }

    // terminal_processing::clear_screen();

    // thread::sleep(time::Duration::from_secs(1));

    // let basque_family_members =
    //     "/Users/luna/flash-cards/languages/basque/self-study/family_members.txt".to_string();

    // let words: Vec<Vec<String>> = file_processing::render_cards(&basque_family_members);
    // println!("{:#?}", words);

}

fn quiz() {}
