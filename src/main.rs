use clap::Parser;
use clearscreen;
use ratatui::crossterm::style::Stylize;
use std::{thread, time};

mod file_processing;
mod terminal_processing;

fn main() {
    let args: terminal_processing::Args = terminal_processing::Args::parse();

    // clearscreen::clear().expect("failed to clear screen");

    // // the addons turn PathBuf into a String to allow us to change its color with ratatui::cossterm...
    // let file_path: String = args
    //     .flashcard_filepath
    //     .clone()
    //     .into_os_string()
    //     .into_string()
    //     .unwrap();

    match file_processing::validate_cards(&args.flashcard_filepath) {
        Ok(()) => (),
        Err(e) => {
            eprintln!(
                "Error validating file {}: {}\nStopping program.",
                &args
                    .flashcard_filepath
                    .into_os_string()
                    .into_string()
                    .unwrap()
                    .red(),
                e
            );
            // exit the program with an error code because i don't want the program to run if the
            // flashcards are deemed invalid
            std::process::exit(1);
        }
    }

    // TODO: define required and optional args

    // terminal_processing::clear_screen();

    // thread::sleep(time::Duration::from_secs(1));

    let words: Vec<Vec<String>> = file_processing::render_cards(&args.flashcard_filepath);
    println!("{:?}", words);

    /* TODO:
        run `quiz()` which will be in `quiz.rs`
        get outputs of `quiz()` and then run graph plotting functions here
    */
}

fn quiz() {}
