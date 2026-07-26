use clap::{Parser, ValueEnum};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use unicode_segmentation::UnicodeSegmentation;

use crate::streak_counter;
use crate::StreakTrait;
use crate::hint_system;
use crate::terminal_processing;

// TODO:
// add session.json
// session.txt will have to be handled differently
#[derive(Debug)]
pub struct QuizData {
    pub x_axes: Vec<Vec<u32>>,
    pub y_axes: Vec<Vec<f32>>,
    pub session_settings_data: json::JsonValue,
    // session_settings_data = {
    //     "file_path_to_cards": sys.argv[1],
    //     "difficulty": p_args.difficulty,
    //     "randomize": p_args.randomize,
    //     "flip": p_args.flip_cards,
    //     "num_cards_in_set": str(NUM_CARDS),
    //     "num_rounds": len(x_axes),
    //     "highest_streak": str(quiz_counter.get_highest_streak()),
    //     "is_perfect_streak": str(quiz_counter.get_highest_streak() == THEORETICAL_MAX_STREAK)
    // }
}

impl QuizData {
    pub fn new(
        x_axes: Vec<Vec<u32>>,
        y_axes: Vec<Vec<f32>>,
        session_settings_data: json::JsonValue,
    ) -> Self {
        Self {
            x_axes,
            y_axes,
            session_settings_data,
        }
    }
}

#[rustfmt::skip]
pub fn quiz( card_set: Vec<Vec<String>>, args: terminal_processing::Args, start_time: Duration,) -> QuizData {
    let mut correct_answers: Vec<Vec<String>> = Vec::new();
    let mut round_num: u16 = 0;
    let NUM_CARDS = card_set.len();
    let THEORETICAL_MAX_STREAK = &NUM_CARDS;
    let mut x_axes: Vec<Vec<u32>> = Vec::new();
    let mut y_axes: Vec<Vec<f32>> = Vec::new();

    // TODO: make outline of quiz functionality from first commit of main branch

    // Source - https://stackoverflow.com/a/58770681
    // Posted by Lukas Kalbertodt, modified by community. See post 'Timeline' for change history
    // Retrieved 2026-07-26, License - CC BY-SA 4.0
    let mut max_left_len: usize = 0;
    for sublst in card_set {
        // this counts characters as 1 character regardless of diacritics
        if sublst[0].graphemes(true).collect::<Vec<&str>>().len() > max_left_len {
            max_left_len = sublst[0].graphemes(true).collect::<Vec<&str>>().len();
        }
    }

    let mut quiz_counter: streak_counter::StreakCounter = streak_counter::StreakCounter::new(0, 0);

    return QuizData::new(
        x_axes,
        y_axes,
        json::JsonValue::new_object(),
    );
}
