pub struct StreakCounter {
    current_streak: u16,
    highest_streak: u16,
}

pub trait StreakTrait {
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

