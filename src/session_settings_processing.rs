use json::{self, JsonValue};
use clap::{Parser, ValueEnum};
use std::{fmt, path::PathBuf};

// TODO: add descriptions for optional args

// Source - https://stackoverflow.com/q/74721827
// Posted by WebOrCode
// Retrieved 2026-07-29, License - CC BY-SA 4.0
#[derive(Parser, Debug)]
pub struct Args {
    pub flashcard_filepath: PathBuf,
    pub difficulty: Difficulty,
    pub rand: RandomSetting,
    pub flip: FlipSetting,
    #[clap(short, long, default_value_t = false)]
    pub test: bool,
    #[clap(short, long, default_value_t = false)]
    pub conceal_user_input: bool,
}

#[derive(ValueEnum, Clone, Debug, PartialEq, Eq)]
pub enum Difficulty {
    // these are interpreted as strings by clap, i.e `Easy` corresponds to `easy` when running the
    // program
    Easy,
    Normal,
    Hard,
    HardWithSpaces,
    VeryHard,
}
// Source - https://stackoverflow.com/a/32712140
// Posted by Vladimir Matveev, modified by community. See post 'Timeline' for change history
// Retrieved 2026-07-27, License - CC BY-SA 4.0

impl fmt::Display for Difficulty {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
        // or, alternatively:
        // fmt::Debug::fmt(self, f)
    }
}

#[derive(ValueEnum, Clone, Debug, PartialEq, Eq)]
pub enum RandomSetting {
    RandOnce,
    RandEveryRound,
    NoRand,
    Test,
}

impl fmt::Display for RandomSetting {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
        // or, alternatively:
        // fmt::Debug::fmt(self, f)
    }
}

#[derive(ValueEnum, Clone, Debug, PartialEq, Eq)]
pub enum FlipSetting {
    Flip,
    NoFlip,
}

impl fmt::Display for FlipSetting {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
        // or, alternatively:
        // fmt::Debug::fmt(self, f)
    }
}
