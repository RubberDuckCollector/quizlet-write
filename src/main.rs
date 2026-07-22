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

    // TODO: define required and optional args

    // clearscreen::clear().expect("Should be able to clear the screen.");

    // thread::sleep(time::Duration::from_secs(1));

    let separator: &str = "|";

    #[allow(unused_variables)]
    #[rustfmt::skip]
    let words: Vec<Vec<String>> = flashcard_processing::render_cards(&args.flashcard_filepath, separator);
    println!("{:#?}", words);

    /* TODO:
        run `quiz()` which will be in `quiz.rs`
        get outputs of `quiz()`
        write graph plotting functions in a separate file
        call those functions here

        OPTIMIZE: i want quiz() to fully end before writing the session's x and y coordinate data
        and plotting the graph for the session.
            - essentially, quiz() SHOULD be called by assigning the output to a variable
            `(e.g.: let session_data = quiz(words))`
        = to implement saving and resuming a session, maybe return early from `quiz()`
        with a special flag and if the flag is found, invoke saving session procedures
    */
}

struct StreakCounter {
    current_streak: u16,
    highest_streak: u16,
}

trait StreakTrait {
    fn new(current_streak: u16, highest_streak: u16) -> Self;

    fn increment_streak(&mut self);

    fn decrement_streak(&mut self);

    fn reset_streak(&mut self);

    fn set_current_streak(&mut self, curr_streak: u16);

    fn set_highest_streak(&mut self, highest_streak: u16);

    fn get_current_streak(&self) -> u16;

    fn get_highest_streak(&self) -> u16;
}

impl StreakTrait for StreakCounter {
    fn new(current_streak: u16, highest_streak: u16) -> Self {
        Self {
            current_streak,
            highest_streak,
        }
    }

    fn increment_streak(&mut self) {
        self.current_streak += 1;

        if self.current_streak > self.highest_streak {
            self.highest_streak = self.current_streak
        }
    }

    fn decrement_streak(&mut self) {
        if self.current_streak <= 0 {
            self.current_streak = 0
        } else {
            self.current_streak -= 1
        }
    }

    fn reset_streak(&mut self) {
        self.current_streak = 0
    }

    fn set_current_streak(&mut self, curr_streak: u16) {
        self.current_streak = curr_streak;

        if self.current_streak > self.highest_streak {
            self.highest_streak = self.current_streak
        }
    }

    fn set_highest_streak(&mut self, highest_streak: u16) {
        self.highest_streak = highest_streak
    }

    fn get_current_streak(&self) -> u16 {
        return self.current_streak;
    }

    fn get_highest_streak(&self) -> u16 {
        return self.highest_streak;
    }
}

#[allow(dead_code)]
fn quiz() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn streak_counter() {
        let mut my_streak_counter = StreakCounter::new(0, 0);
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
}
