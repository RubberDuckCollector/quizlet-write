use clap::{Parser, ValueEnum};

#[derive(Parser, Debug)]
pub struct Args {
    pub flashcard_filepath: std::path::PathBuf,
    pub difficulty: Difficulty,
    pub rand: RandomSetting,
    pub flip: FlipSetting,
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

#[derive(ValueEnum, Clone, Debug, PartialEq, Eq)]
pub enum RandomSetting {
    RandOnce,
    RandEveryRound,
    NoRand,
    Test,
}

#[derive(ValueEnum, Clone, Debug, PartialEq, Eq)]
pub enum FlipSetting {
    Flip,
    NoFlip,
}
