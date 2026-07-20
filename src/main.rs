use clap::Parser;
use clearscreen;
use ratatui::crossterm::style::Stylize;
use std::{thread, time};

mod flashcard_processing;
mod terminal_processing;

fn main() {
    let args: terminal_processing::Args = terminal_processing::Args::parse();

    // clearscreen::clear().expect("failed to clear screen");

    match flashcard_processing::validate_cards(&args.flashcard_filepath) {
        Ok(()) => (),
        Err(e) => {
            #[rustfmt::skip]
            eprintln!("Error validating file {}: {}\nStopping program.",
                &args
                    .flashcard_filepath
                    .into_os_string()
                    .into_string()
                    .unwrap()
                    .red(),
                e.bold()
            );
            // exit the program with an error code because i don't want the program to run if the
            // flashcards are deemed invalid
            std::process::exit(1);
        }
    }

    // TODO: define required and optional args

    // clearscreen::clear().expect("Should be able to clear the screen.");

    // thread::sleep(time::Duration::from_secs(1));

    let separator: &str = "|";

    #[allow(unused_variables)]
    #[rustfmt::skip]
    let words: Vec<Vec<String>> = flashcard_processing::render_cards(&args.flashcard_filepath, separator);
    println!("{:?}", words);

    /* TODO:
        run `quiz()` which will be in `quiz.rs`
        get outputs of `quiz()`
        write graph plotting functions in a separate file
        call those functions here

        OPTIMIZE: i want quiz() to fully end before writing the session's x and y coordinate data
        and plotting the graph for the session.
            - essentially, quiz() SHOULD be called by assigning the output to a variable
            `(e.g.: let session_data = quiz(words))`
    */
}

#[allow(dead_code)]
fn quiz() {}
