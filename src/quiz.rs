use clap::{Error, Parser, ValueEnum};
use json::object;
use ratatui::crossterm::style::Stylize;
use rpassword::read_password;
use rustyline::DefaultEditor;
use rustyline::error::ReadlineError;
use std::cmp::Ordering;
use std::fs;
use std::io::{Write, stdin, stdout};
use std::ops::Index;
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

#[derive(Debug)]
struct SessionCardAggregate {
    total_correct: usize,
    round_num: usize,
    total_available_cards: Vec<Vec<Vec<String>>>,  // tracks the cards that are available to be
    // picked from each round
    round_correct_cards: Vec<Vec<String>>,
    round_incorrect_cards: Vec<Vec<String>>,
}

impl SessionCardAggregate {
    fn new(
        total_correct: usize,
        round_num: usize,
        total_available_cards: Vec<Vec<Vec<String>>>,
        round_correct_cards: Vec<Vec<String>>,
        round_incorrect_cards: Vec<Vec<String>>,
    ) -> Self {
        Self {
            total_correct,
            round_num,
            total_available_cards,
            round_correct_cards,
            round_incorrect_cards,
            // add a space for current card set in question and replace card_set.len() != 0 with
            // that
        }
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
    let mut s_c_a: SessionCardAggregate = SessionCardAggregate::new(0, 0, Vec::new(), Vec::new(), Vec::new());

    s_c_a.total_available_cards.push(card_set.clone());
    s_c_a.round_correct_cards.push(Vec::new());
    s_c_a.round_incorrect_cards.push(Vec::new());
    println!("{:#?}", s_c_a);

    let test_indicator: &str = match &args.test {
        true => " TEST MODE - NO STATS SAVED",
        false => "",
    };
    let conceal_inputs: &str = match &args.conceal_inputs {
        true => " -- INPUTS HIDDEN",
        false => "",
    };

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

    println!("{:#?}", s_c_a.total_available_cards[0][0]);
    while s_c_a.total_correct != s_c_a.total_available_cards[0][0].len() {
        let mut num_correct: u32 = 0;
        let mut num_answered: u32 = 0;
        let mut num_incorrect: u32 = 0;
        let mut num_remaining = card_set.len();
        let mut cards_to_remove: Vec<Vec<String>> = Vec::new();

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
            println!("Working from file {}{}{}", fs::canonicalize(&args.flashcard_filepath).unwrap().to_str().unwrap().dim(), &test_indicator, &conceal_inputs.bold());
            println!("Remaining: {}", num_remaining);
            println!("Correct: {} ({:.2})", &num_correct.to_string().green(), &current_percent_correct);
            println!("Incorrect: {}", &num_incorrect.to_string().red());
            println!("Progress: {}", &progress.to_string().blue());
            println!("Streak: {} ({})", &quiz_counter.get_current_streak().to_string().magenta(), &quiz_counter.get_highest_streak().to_string().magenta());
            println!("What's the answer to {}?", prompt.clone().cyan());
            println!("Hint: {}", &hint.dim());
            stdout().flush().unwrap();

            // logic for answering a question
            let user_response: Result<String, ReadlineError> = match &args.conceal_inputs {
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
            match user_response {
                Ok(ref _string) => (),
                Err(ReadlineError::Eof) => return Err(ReadlineError::Eof),
                Err(ReadlineError::Interrupted) => return Err(ReadlineError::Interrupted),
                Err(err) => return Err(err),
            }
            let user_response_trimmed = user_response.unwrap().as_str().trim().to_string();

            if user_response_trimmed.len() == 0 {
                quiz_counter.reset_streak();
                num_incorrect += 1;
                s_c_a.round_incorrect_cards.push(subl.clone());
                println!("Don't know? Copy out the answer so you remember it!");
                loop {
                    print!("Copy the answer below ↓\n- {}\n> ", answer);
                    let user_response_dont_know = user_input::get_user_response();
                    match user_response_dont_know {
                            Ok(ref _string) => (),
                            Err(ReadlineError::Eof) => return Err(ReadlineError::Eof),
                            Err(ReadlineError::Interrupted) => return Err(ReadlineError::Interrupted),
                            Err(err) => return Err(err)
                        }
                    let user_response_dont_know_trimmed = user_response_dont_know.unwrap().as_str().trim().to_string();
                    // user_response_trimmed = user_response.trim();
                    if user_response_dont_know_trimmed.to_lowercase() == answer.to_lowercase() {
                        println!("{}", "Next question.".cyan());
                        thread::sleep(time::Duration::from_millis(500));
                        clearscreen::clear().expect("failed to clear screen");
                        break
                    } println!("Try again.");
                    // FIXME: add file stuff here (python below)
                    // # mark as incorrect as the user doesn't know the answer
                    // f.write(f"✗ {prompt.ljust(max_left_length)} {answer}\n")
                    // f.flush()  # essential to prevent a file error
                }
            } else {
                if &user_response_trimmed == answer {
                    quiz_counter.increment_streak();
                    num_correct += 1;
                    s_c_a.total_correct += 1;
                    s_c_a.round_correct_cards.push(subl.clone());
                    println!("{}", "Correct. Well done!".green());
                    thread::sleep(time::Duration::from_millis(500));
                    clearscreen::clear().expect("failed to clear screen");
                    // FIXME: write files here
                    // f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                    // f.flush()
                } else if user_response_trimmed.to_lowercase() == answer.to_lowercase() {
                    quiz_counter.increment_streak();
                    num_correct += 1;
                    s_c_a.total_correct += 1;
                    s_c_a.round_correct_cards.push(subl.clone());
                    println!("{}", "Correct".green());
                    thread::sleep(time::Duration::from_millis(500));
                    clearscreen::clear().expect("failed to clear screen");
                } else {
                    stdout().flush().unwrap();
                    println!("\n✓ {}", answer.clone().green());
                    println!("✗ {}", user_response_trimmed.magenta());
                    println!("{} {} and {} above.", "Incorrect.".red(), "Correct answer".green(), "your answer".magenta());
                    stdout().flush().unwrap();

                    print!("Override as correct? (empty answer = don't override) ");
                    let veto_answer: String = read!("{}\n");

                    if veto_answer.len() == 0 {
                        quiz_counter.reset_streak();
                        num_incorrect += 1;
                        s_c_a.round_incorrect_cards.push(subl.clone());
                        println!("{}", "Not overridden.".yellow());
                        thread::sleep(time::Duration::from_millis(500));
                        clearscreen::clear().expect("failed to clear screen");
                    } else {
                        quiz_counter.increment_streak();
                        num_correct += 1;
                        s_c_a.total_correct += 1;
                        s_c_a.round_correct_cards.push(subl.clone());
                        println!("Overridden as {}.", "Correct".green());
                        thread::sleep(time::Duration::from_millis(500));
                        clearscreen::clear().expect("failed to clear screen");
                    }
                }
            }

            num_answered += 1;
            num_remaining -= 1;

            // WARNING: before anything else regarding stats collection, develop saving and resuming functionality
        }

        // println!("{:?}", card_set);
        println!("{:#?}", &s_c_a.total_available_cards);

        // TODO: make it so the round can be described in terms of a list that holds the available cards the
        // quiz can pull from
        // this means that index 0 would have all of the cards, index 1 would mean round 1 and have only the
        // incorrect cards from round 1 which will be forwarded to round 2, etc.
        // this repeats until there are no cards left to be passed on to another round and therefore all
        // cards have been answered correctly

        // TODO:
        // 3-D vector where each round is a sublist containing 3 sublists:
        // 1. the full flash card ste
        // 2. the correct answers
        // 3. the incorrect answers
        // the incorrect answers are passed on to the next round if the length is > 0
        // this way, the history of the session is preserved fully without compromises
        // NEED TO NOW MAKE THE ROUND USE THE LAST ELEMENT OF S_C_A.TOTAL_AVAILABLE_CARDS

        // tidy up each list by removing elements that are empty vectors
        s_c_a.round_incorrect_cards.retain(|x| !x.is_empty());
        s_c_a.round_correct_cards.retain(|x| !x.is_empty());

        s_c_a.total_available_cards.push(s_c_a.round_incorrect_cards.clone());

        // NOTE: this would only be needed if the data coming in from `s_c_a.round_incorrect_cards`
        // has empty list elements
        // for outer in &mut s_c_a.total_available_cards {
        //     outer.retain(|inner| !inner.is_empty());
        // }

        println!("{:?}", s_c_a.total_available_cards);

        s_c_a.round_num += 1;
    }

    return Ok(QuizData::new(
        x_axes,
        y_axes,
        session_data,
    ));
}
