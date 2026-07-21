use std::any::{Any, type_name};
use std::fs;
use std::io::{self, BufRead, Write};
use std::path::Path;

// https://doc.rust-lang.org/stable/rust-by-example/std_misc/file/read_lines.html#a-more-efficient-approach
pub fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<fs::File>>>
where
    P: AsRef<Path>,
{
    let file = fs::File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn separator_exists(line: &String, sep: &str) -> bool {
    line.contains(sep)
}

fn is_separator_only_char(line: &String, sep: &str) -> bool {
    line.len() == sep.len() && line.contains(sep)
}

fn separator_too_many(line: &String, sep: &str, expected_num: &u16) -> (u16, bool) {
    let mut too_many_separators: bool = false;
    let sep_count: u16 = line.matches(sep).count().try_into().unwrap();
    if sep_count > *expected_num {
        too_many_separators = true;
    }
    (sep_count, too_many_separators)
}

fn separator_on_ends_of_line(line: &String, sep: &str) -> (bool, bool) {
    let mut is_sep_at_first_last: (bool, bool) = (false, false);

    if line.starts_with(sep) {
        is_sep_at_first_last.0 = true;
    }

    if line.ends_with(sep) {
        is_sep_at_first_last.1 = true;
    }

    is_sep_at_first_last
}

/// Returns a vector where each element is a tuple with two u32s that represent the start and end of
/// where any consecutive separators are found (consecutive separators is disallowed).
/// e.g: (10, 14) would signify contiguous separators that start on index 10 and end ON, NOT BEFORE index 14; so
/// 10..=14 (as represented by a Rust range)
///
/// We can make some assumptions here:
/// line.len() > sep.len() due to requiring content on the flashcards.
fn collate_consecutive_separators(line: &String, sep: &str) -> Vec<(usize, usize)> {
    let mut consecutive_sep_ranges: Vec<(usize, usize)> = Vec::new();

    let line_bytes = line.as_bytes();
    let sep_bytes = sep.as_bytes();

    let mut i: usize = 0;

    let last_possible_start_idx: usize = line_bytes.len() - sep.len();

    while i <= last_possible_start_idx {
        // look for the first separator in the line.
        // loop once more if a separator isn't found
        if &line_bytes[i..i + sep_bytes.len()] != sep_bytes {
            i += 1;
            continue;
        }

        // we found a separator if the code reaches this line
        let consecutive_seps_start: usize = i;
        let mut consecutive_seps_end: usize = i + sep_bytes.len() - 1; // final index of the line
        let mut separator_count: usize = 1;

        i += sep_bytes.len(); // progress through the line by the length of the sep as bytes

        // while we're not at the end of the line,
        // AND we've found a separator
        while i + sep_bytes.len() <= line_bytes.len()
            && &line_bytes[i..i + sep_bytes.len()] == sep_bytes
        {
            separator_count += 1; // we've seen 2 separators here, so increment this
            consecutive_seps_end = i + sep_bytes.len() - 1; // final index
            i += sep_bytes.len(); // progress through the line by the length of the sep as bytes
        }

        // only store runs of this algorithm where we find 2+ consecutive separators.
        if separator_count >= 2 {
            consecutive_sep_ranges.push((consecutive_seps_start, consecutive_seps_end));
        }
    }

    consecutive_sep_ranges
}

/// Returns nothing if flashcards have valid formatting, else returns a String.
/// The String is the error message which is pushed up to main() and handled there.
pub fn validate_cards<P>(filepath: P) -> Result<(), String>
where
    P: AsRef<Path>,
{
    // - [x] 1. check if file exists
    // - [x] 2. check if file exists but empty
    // - [x] 2.1. check presence of | (display line number)
    // - [x] 2.2. check if the only char on the line is |
    // - [x] 2.3. check if there are more than `expected_count` | chars (display line number)
    // - [x] 2.4. make sure a separator cannot be on the extreme left or right of the line
    // - [x] 2.5. disallow consecutive separators by 2 methods

    // OPTIMIZE: let the user specify the separator on the command line
    // in the future by using a config file?
    let separator: &str = "|";
    let separators_per_line: u16 = 1; // expected MAX number of seps per line
    // NOTE: using the defined number of separators per line,
    // calculate the expected number of content elements per line.
    // on each line, count the number of content elements we actually see.
    // NOTE: there must be an algorithm for determining how many content
    // elements there are for a given number of separators, given that
    // separators cannot be on the far left end, far right end, OR be directly
    // next to each other
    // XXX: there are 2 competing solutions that both catch consecutive separators: the above
    // solution, and `collate_consecutive_separators`

    #[rustfmt::skip]
    let mut output: Result<(), String> = Err("I'm an error by default until the flashcards have been validated. Double check the code's logic!".to_string());
    assert_eq!(output, Err("I'm an error by default until the flashcards have been validated. Double check the code's logic!".to_string()));

    match fs::exists(&filepath) {
        Ok(true) => output = Ok(()),
        Ok(false) => {
            return Err("File does not exist.".to_string());
        }
        Err(_) => {
            return Err("Couldn't check for file's existence.".to_string());
        }
    };

    // if the file exists, try to return an Err by doing formatting checks
    if output == Ok(()) {
        if fs::read_to_string(&filepath)
            .expect("Should have been able to read the file.")
            .len()
            == 0
        {
            return Err("File exists but is empty.".to_string());
        }

        if let Ok(lines) = read_lines(filepath) {
            // consumes the iterator, returns an (Optional) String

            let mut line_number: usize = 0;

            for mut line in lines.map_while(Result::ok) {
                line = line.trim().to_string();
                line_number += 1;

                if !separator_exists(&line, separator) {
                    #[rustfmt::skip]
                    let msg: String = format!("LINE {}: The designated separator ({}) wasn't found.", &line_number, separator);
                    return Err(msg);
                }

                if is_separator_only_char(&line, separator) {
                    #[rustfmt::skip]
                    let msg: String = format!("LINE {}: The designated separator ({}) was the only character the line after trimming whitespace. The line needs a prompt and an answer on the left and right sides of the separator ({}) respectively.", &line_number, separator, separator);
                    return Err(msg);
                }

                match separator_too_many(&line, separator, &separators_per_line) {
                    (sep_count, true) => {
                        #[rustfmt::skip]
                        let msg: String = format!("LINE {}: The designated separator ({}) appeared {} times -- more than the desired {} times.", &line_number, separator, sep_count, &separators_per_line);
                        return Err(msg);
                    }
                    (_, false) => (), // do nothing if it returns false, in this case we also don't care about how many separators there are
                }

                match separator_on_ends_of_line(&line, separator) {
                    // do nothing if no separators were found at either end of the line
                    (false, false) => (),

                    (true, true) => {
                        #[rustfmt::skip]
                        let msg: String = format!("LINE {}: The separator ({}) was found at BOTH ENDS of the line (after trimming whitespace), which is disallowed.", &line_number, separator);
                        return Err(msg);
                    }
                    (true, false) => {
                        #[rustfmt::skip]
                        // TODO: improve the below message
                        // ("please add content to the LEFT of the separator or remove the
                        // separator.")
                        // after calculating that, if the number of content elements is too low,
                        // return that info in the error message accordingly
                        let msg: String = format!("LINE {}: The separator ({}) was found at the LEFT of the line (after trimming whitespace), which is disallowed. If you can have more than one separator per line (which is customisable), please add content to the LEFT of this separator.", &line_number, separator);
                        return Err(msg);
                    }
                    (false, true) => {
                        #[rustfmt::skip]
                        // TODO: improve the below message
                        // ("please add content to the RIGHT of the separator or remove the
                        // separator.")
                        let msg: String = format!("LINE {}: The separator ({}) was found at the RIGHT of the line (after trimming whitespace), which is disallowed. If you can have more than one separator per line (which is customisable), please add content to the RIGHT of this separator.", &line_number, separator);
                        return Err(msg);
                    }
                };

                if separators_per_line > 1 {
                    // if we expect more than 1 separator per line, consecutive separators are
                    // possible
                    let mut consecutive_seps_result: Vec<(usize, usize)> =
                        collate_consecutive_separators(&line, separator);
                    match consecutive_seps_result.len() {
                        0 => (),
                        _ => {
                            // FIXME: write this error message
                            // SHOW THE TUPLES
                            // E.G.: "CONSECUTIVE SEPARATORS FOUND AT X, Y, Z. THIS IS NOT ALLOWED
                            // AS THERE MUST BE CONTENT IN BETWEEN ALL SEPARATORS"
                            for (start_idx, end_idx) in consecutive_seps_result.iter_mut() {
                                *start_idx += 1;
                                *end_idx += 1;
                            }
                            let msg: String = format!(
                                "LINE {}: consecutive separators were found on the following columns in the line: {:?}. Please correct this by adding content in between the consecutive separators, or delete separators until there are no consecutive separators.\nThere must be one separator at a time.",
                                &line_number, consecutive_seps_result
                            );
                            return Err(msg);
                        }
                    }
                }
            }
        }
    }
    // HOPEFULLY Ok(()) here
    // OTHERWISE Err("...") by default
    // all desired cases should have be handled in the above branches
    //
    output
}

// TODO: make it so it returns a Result<<Vec<Vec<String>>>, String>
// do a match on this in `main()` to catch errors
pub fn render_cards<P>(filepath: P, sep: &str) -> Vec<Vec<String>>
where
    P: AsRef<Path>,
{
    let mut words: Vec<Vec<String>> = Vec::new();

    if let Ok(lines) = read_lines(filepath) {
        // Consumes the iterator, returns an (Optional) String

        // Likely to not need to read a file with 2^32 / 2^64 lines in it.
        let mut line_number: usize = 0;

        for line in lines.map_while(Result::ok) {
            line_number += 1;

            // trim the whitespace off either side
            let trimmed_line: &str = line.trim();

            if trimmed_line.chars().nth(0).unwrap() != '#' {
                // lines starting with # are skipped

                // WARNING: even though this can work with more than 1 separator on each line,
                // extending funcionality and implementing tagging would lend itself better to json
                // so don't create technical debt by pursuing this more simplistic structure!
                let content: Vec<String> = trimmed_line
                    .split(sep)
                    .map(str::trim)
                    .map(String::from)
                    .collect();
                // convert the borrowed &str halves into owned Strings
                // so everything is owned and can be looped on an returned safely
                if !content.is_empty() {
                    words.push(content);
                }
            } else {
                println!("# found on line {}", line_number);
            }
        }
    }
    words
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sep_too_many() {
        let a: String = String::from("asf?!?d;lkjasd;?!?fljkasd;?!?flkjasdf;lkj?!!!?");
        let sep_count: u16 = a.matches("?!?").count().try_into().unwrap();
        // let seps_vec: Vec<&str> = a.matches("?!?").collect();
        assert_eq!(sep_count, 3);
    }

    #[test]
    fn find_sep() {
        // let a: String = String::from("asf?!?d;lkjasd;?!??!?fljkasd;?!??!?!?flkjasdf;lkj?!!!?");
        // println!("{}", a.len());
        // let b: Vec<(usize, usize)> = collate_consecutive_separators(&a, "?!?");
        // println!("{:?}", b);

        let a: String = String::from("a|b||c||");
        println!("{}", a.len());
        let b: Vec<(usize, usize)> = collate_consecutive_separators(&a, "|");
        println!("{:?}", b);
    }
}
