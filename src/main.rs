use crate::streak_counter::StreakTrait;
use clap::Parser;
use clearscreen;
use ratatui::crossterm::style::Stylize;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use std::{thread, time};

mod flashcard_processing;
mod hint_system;
mod quiz;
mod session_settings_processing;
mod streak_counter;

fn main() {
    let args: session_settings_processing::Args = session_settings_processing::Args::parse();

    // println!("{:?}", &args);

    let now = SystemTime::now();
    let now_ms = now.duration_since(UNIX_EPOCH).expect("Time went backwards");
    // println!("{:?}", now_ms);

    println!("{:#?}", args);

    // clearscreen::clear().expect("failed to clear screen");

    match flashcard_processing::validate_cards(&args.flashcard_filepath) {
        Ok(()) => (),
        Err(e) => {
            #[rustfmt::skip]
            eprintln!("Error validating the file {}: {}\nStopping program.",
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

    // clearscreen::clear().expect("Should be able to clear the screen.");

    // thread::sleep(time::Duration::from_secs(1));

    let separator: &str = "|";

    #[allow(unused_variables)]
    #[rustfmt::skip]
    let mut card_set: Vec<Vec<String>> = flashcard_processing::render_cards(&args.flashcard_filepath, separator);
    println!("{:?}", card_set);

    /* TODO:
        run `quiz()` which will be in `quiz.rs`
        get outputs of `quiz()`
        write graph plotting functions in a separate file
        call those functions here

        OPTIMIZE: i want quiz() to fully end before writing the session's x and y coordinate data
        and plotting the graph for the session.
            - essentially, quiz() SHOULD be called by assigning the output to a variable
            `(e.g.: let session_data = quiz(card_set))`
        = to implement saving and resuming a session, maybe return early from `quiz()`
        with a special flag and if the flag is found, invoke saving session procedures
    */

    let quiz_data: quiz::QuizData = quiz::quiz(card_set, args, now_ms);
}

#[cfg(test)]
mod main_tests {
    use super::*;

    #[test]
    fn streak_counter() {
        let mut my_streak_counter = streak_counter::StreakCounter::new(0, 0);
        assert_eq!(0, my_streak_counter.get_current_streak());

        my_streak_counter.increment_streak();
        assert_eq!(1, my_streak_counter.get_current_streak());
        assert_eq!(1, my_streak_counter.get_highest_streak());

        my_streak_counter.increment_streak();
        assert_eq!(2, my_streak_counter.get_current_streak());
        assert_eq!(2, my_streak_counter.get_highest_streak());

        my_streak_counter.decrement_streak();
        assert_eq!(1, my_streak_counter.get_current_streak());
        assert_eq!(2, my_streak_counter.get_highest_streak());

        my_streak_counter.reset_streak();
        assert_eq!(0, my_streak_counter.get_current_streak());
        assert_eq!(2, my_streak_counter.get_highest_streak());

        my_streak_counter.set_current_streak(1001);
        assert_eq!(1001, my_streak_counter.get_current_streak());
        assert_eq!(1001, my_streak_counter.get_highest_streak());

        my_streak_counter.set_highest_streak(65535);
        assert_eq!(65535, my_streak_counter.get_highest_streak());
        assert_eq!(1001, my_streak_counter.get_current_streak());
    }

    #[test]
    fn compare_times() {
        let unix_time_1 = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        println!("{}", unix_time_1);

        let unix_time_2 = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        println!("{}", unix_time_2);

        assert_eq!(unix_time_2, unix_time_1);
    }
}
