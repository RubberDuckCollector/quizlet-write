use clap::{Parser, ValueEnum};
use json::object;
use ratatui::crossterm::style::Stylize;
use rpassword::read_password;
use rustyline::error::ReadlineError;
use rustyline::{DefaultEditor};
use std::cmp::Ordering;
use std::fs;
use std::io::{Write, stdin, stdout};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use std::{thread, time};
use text_io::read;
use unicode_segmentation::UnicodeSegmentation;

use crate::StreakTrait;
use crate::hint_system;
use crate::session_settings_processing;
use crate::session_settings_processing::Difficulty;
use crate::streak_counter;
use crate::user_input;

#[derive(Debug)]
pub struct QuizData(pub Vec<Vec<u32>>, pub Vec<Vec<f32>>, pub json::JsonValue);

impl QuizData {
    pub fn new(
        x_axes: Vec<Vec<u32>>,
        y_axes: Vec<Vec<f32>>,
        session_settings_data: json::JsonValue,
    ) -> Self {
        Self(x_axes, y_axes, session_settings_data)
    }
}

#[rustfmt::skip]
pub fn quiz( mut card_set: Vec<Vec<String>>, args: session_settings_processing::Args, start_time: Duration,) -> Result<QuizData, ReadlineError> {
    let mut correct_answers: Vec<Vec<String>> = Vec::new();
    let mut round_num: u32 = 0;
    let NUM_CARDS = card_set.len();
    let THEORETICAL_MAX_STREAK = &NUM_CARDS;
    let mut x_axes: Vec<Vec<u32>> = Vec::new();
    let mut y_axes: Vec<Vec<f32>> = Vec::new();
    let mut rl = DefaultEditor::new()?;

    // OPTIMIZE: assign these variables based on the --test and --conceal-user-input optional args
    let test_indicator: &str = match &args.test {
        true => " TEST MODE - NO STATS SAVED",
        false => "",
    };
    let conceal_inputs: &str = match &args.conceal_inputs {
        true => " -- INPUTS HIDDEN",
        false => "",
    };

    // TODO: make outline of quiz functionality from first commit of main branch

    // Source - https://stackoverflow.com/a/58770681
    // Posted by Lukas Kalbertodt, modified by community. See post 'Timeline' for change history
    // Retrieved 2026-07-26, License - CC BY-SA 4.0
    let mut max_left_len: usize = 0;
    for sublst in &card_set {
        // this counts characters as 1 character regardless of diacritics
        if sublst[0].graphemes(true).collect::<Vec<&str>>().len() > max_left_len {
            max_left_len = sublst[0].graphemes(true).collect::<Vec<&str>>().len();
        }
    }

    let mut quiz_counter: streak_counter::StreakCounter = streak_counter::StreakCounter::new(0, 0);

    let session_data = object! {
        "file_path_to_cards": args.flashcard_filepath.to_str(),
        "difficulty": args.difficulty.to_string(),
        "randomize": args.rand.to_string(),
        "flip": args.flip.to_string(),
        "num_cards_in_set": NUM_CARDS.to_string(),
        "num_rounds": x_axes.len(),
        "highest_streak": quiz_counter.get_highest_streak(),
        "is_perfect_streak": &quiz_counter.get_highest_streak() == THEORETICAL_MAX_STREAK,
    };

    // println!("SESSION DATA: {:?}", session_data);

    // println!("{:#?}", &card_set);

    while card_set.len() != 0 {
        round_num += 1;
        let mut num_correct: u32 = 0;
        let mut num_answered: u32 = 0;
        let mut num_incorrect: u32 = 0;
        let mut num_remaining = card_set.len();

        for subl in &card_set {
            let [prompt, answer] = &subl[..] else {
                unreachable!("Every inner vec has length 2")
            };

            let hint: String = match args.difficulty {
                Difficulty::Easy => {
                    hint_system::make_easy_hint(&answer)
                }
                Difficulty::Normal => {
                    hint_system::make_normal_hint(&answer)
                }
                Difficulty::Hard => {
                    hint_system::make_hard_hint(&answer)
                }
                Difficulty::HardWithSpaces => {
                    hint_system::make_hard_with_spaces_hint(&answer)
                }
                Difficulty::VeryHard => {
                    hint_system::make_very_hard_hint()
                }
            };

            // https://users.rust-lang.org/t/greater-than-less-than-in-a-match-block/63399/5
            let mut current_percent_correct: f32 = match num_answered.cmp(&0) {
                Ordering::Greater => num_correct as f32 / num_answered as f32 * 100.0,
                _ => 0.0
            };

            let mut progress: f32 = match num_answered.cmp(&0) {
                Ordering::Greater => num_answered as f32 / card_set.len() as f32 * 100.0,
                _ => 0.0
            };

            // Source - https://stackoverflow.com/a/38384901
            // Posted by alexwlchan
            // Retrieved 2026-07-29, License - CC BY-SA 3.0
            stdout().flush().unwrap();
            println!("Working from file {}{}{}", fs::canonicalize(&args.flashcard_filepath).unwrap().to_str().unwrap().dim(), &test_indicator, &conceal_inputs);
            println!("Remaining: {}", num_remaining);
            println!("Correct: {} ({:.2})", &num_correct.to_string().green(), &current_percent_correct);
            println!("Incorrect: {}", &num_incorrect.to_string().red());
            println!("Progress: {}", &progress.to_string().blue());
            println!("Streak: {} ({})", &quiz_counter.get_current_streak().to_string().magenta(), &quiz_counter.get_highest_streak().to_string().magenta());
            println!("What's the answer to {}?", prompt.clone().cyan());
            println!("Hint: {}", &hint.dim());
            // print!("> ");
            stdout().flush().unwrap();

            let mut user_response: Result<String, ReadlineError> = match &args.conceal_inputs {
                true => {
                    stdout().flush().unwrap();
                    print!("> ");
                    read_password()
                    .map_err(|_| ReadlineError::Io(std::io::Error::other("failed to read password")))
                }
                false => {
                    user_input::get_user_response()
                }
            };
            let mut user_response_trimmed = user_response.unwrap().as_str().trim();

            // if user_response_trimmed.len() == 0 {
            //     quiz_counter.reset_streak();
            //     num_incorrect += 1;
            //     println!("Don't know? Copy out the answer so you remember it!");
            //     loop {
            //         print!("Copy the answer below ↓\n- {}\n> ", answer);
            //         user_response = read!("{}\n");
            //         user_response_trimmed = user_response.trim();
            //         if user_response_trimmed.to_lowercase() == answer.to_lowercase() {
            //             println!("{}", "Next question.".cyan());
            //             thread::sleep(time::Duration::from_millis(500));
            //             clearscreen::clear().expect("failed to clear screen");
            //             break
            //         } println!("Try again.");
            //         // FIXME: add file stuff here (python below)
            //         // # mark as incorrect as the user doesn't know the answer
            //         // f.write(f"✗ {prompt.ljust(max_left_length)} {answer}\n")
            //         // f.flush()  # essential to prevent a file error
            //     }
            // } else {
            //     if user_response_trimmed == answer {
            //         quiz_counter.increment_streak();
            //         num_correct += 1;
            //         println!("{}", "Correct. Well done!".green());
            //         thread::sleep(time::Duration::from_millis(500));
            //         clearscreen::clear().expect("failed to clear screen");
            //         // FIXME: write files here
            //         // f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
            //         // f.flush()
            //     } else if user_response_trimmed.to_lowercase() == answer.to_lowercase() {
            //         quiz_counter.increment_streak();
            //         num_correct += 1;
            //         println!("{}", "Correct".green());
            //         thread::sleep(time::Duration::from_millis(500));
            //         clearscreen::clear().expect("failed to clear screen");
            //     } else {
            //         stdout().flush().unwrap();
            //         println!("\n✓ {}", answer.clone().green());
            //         println!("✗ {}", user_response_trimmed.magenta());
            //         println!("{} {} and {} above.", "Incorrect.".red(), "Correct answer".green(), "your answer".magenta());
            //         stdout().flush().unwrap();

            //         print!("Override as correct? (empty answer = don't override) ");
            //         let veto_answer: String = read!("{}\n");

            //         if veto_answer.len() == 0 {
            //             quiz_counter.reset_streak();
            //             num_incorrect += 1;
            //             println!("{}", "Not overridden.".yellow());
            //             thread::sleep(time::Duration::from_millis(500));
            //             clearscreen::clear().expect("failed to clear screen");
            //         }
            //     }
            // }

            num_answered += 1;
            num_remaining -= 1;

            // WARNING: before anything else regarding stats collection, develop saving and resuming functionality
        }
    }

    return Ok(QuizData::new(
        x_axes,
        y_axes,
        session_data,
    ));
}
