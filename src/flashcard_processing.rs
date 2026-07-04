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
    line.trim().contains(sep)
}

fn is_separator_only_char(line: &String, sep: &str) -> bool {
    line.trim().len() == sep.len() && line.trim().contains(sep)
}

fn separator_too_many(line: &String, sep: &str, expected_num: &u16) -> (u16, bool) {
    let mut too_many_separators: bool = false;
    let separator_count: u16 = line.trim().matches(sep).count().try_into().unwrap();
    if separator_count > *expected_num {
        too_many_separators = true;
    }
    (separator_count, too_many_separators)
}

fn separator_on_ends_of_line(line: &String, sep: &str) -> (bool, bool) {
    let mut is_sep_at_first_last: (bool, bool) = (false, false);

    if line.trim().starts_with(sep) {
        is_sep_at_first_last.0 = true;
    }

    if line.trim().ends_with(sep) {
        is_sep_at_first_last.1 = true;
    }

    is_sep_at_first_last
}

// TODO: see below
/// Returns a vector where each element is a tuple with two u32s that represent the start and end of
/// where any consecutive separators are found (consecutive separators is disallowed).
/// e.g: (10, 14) would be contiguous separators that start on index 10 and end on index 14; so
/// 10..=14

// fn separator_consecutive(line: &String, sep: &str) -> Vec<(u32, u32)> {

// }

/// Returns nothing if flashcards have valid formatting, else returns a String which is handled in
/// `main()`.
pub fn validate_cards<P>(filepath: P) -> Result<(), String>
where
    P: AsRef<Path>,
{
    // TODO:
    // - [x] 1. check if file exists
    // - [x] 2. check if file exists but empty
    // - [x] 2.1. check presence of | (display line number)
    // - [x] 2.2. check if the only char on the line is |
    // - [x] 2.3. check if there are more than `expected_count` | chars (display line number)
    // - [x] 2.4. make sure a separator cannot be on the extreme left or right of the line
    // - [ ] 2.5. disallow consecutive separators

    // OPTIMIZE: let the user specify the separator on the command line
    // in the future by using a config file?
    let separator: &str = "|";
    let separators_per_line: u16 = 1;
    // TODO: using the defined number of separators per line,
    // calculate the expected number of content elements per line.
    // on each line, count the number of content elements we actually see.
    // see NOTE

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
            // Consumes the iterator, returns an (Optional) String

            // Likely to not need to read a file with 2^32 / 2^64 lines in it.
            let mut line_number: usize = 0;

            for line in lines.map_while(Result::ok) {
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
                    (_, false) => (), // do nothing if it returns false
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
                        // NOTE: there must be an algorithm for determining how many content
                        // elements there are for a given number of separators, given that
                        // separators cannot be on the far left end, far right end, OR be directly
                        // next to each other
                        // after calculating that, if the number of content elements is too low,
                        // retur that info in the error message accordingly
                        let msg: String = format!("LINE {}: The separator ({}) was found at the LEFT of the line (after trimming whitespace), which is disallowed.", &line_number, separator);
                        return Err(msg);
                    }
                    (false, true) => {
                        #[rustfmt::skip]
                        // TODO: improve the below message
                        // ("please add content to the RIGHT of the separator or remove the
                        // separator.")
                        let msg: String = format!("LINE {}: The separator ({}) was found at the RIGHT of the line (after trimming whitespace), which is disallowed.", &line_number, separator);
                        return Err(msg);
                    }
                };
            }
        }
    }
    // HOPEFULLY Ok(()) here
    // OTHERWISE Err("...") by default
    // all desired cases should be handled in the above branches
    output
}

// TODO: make it so it returns a Result<<Vec<Vec<String>>>, String>
// do a match on this in `main()` to catch errors
pub fn render_cards<P>(filepath: P, /* sep: &str */) -> Vec<Vec<String>>
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

                // OPTIMIZE: change this to split on every separator.
                //      (i.e if there are 3 content elements on the line, the sublist would be of length 3).
                //      USE THE `sep` PARAMETER
                // WARNING: even though this can work with more than 1 separator on each line,
                // extending funcionality and implementing tagging would lend itself better to json
                // so don't create technical debt by pursuing this more simplistic structure!
                if let Some((term, definition)) = trimmed_line.split_once('|') {
                    // convert the borrowed &str halves into owned Strings
                    // so everything is owned and can be looped on an returned safely
                    words.push(vec![term.to_string(), definition.to_string()]);
                }
            } else {
                println!("# found on line {}", line_number);
            }
        }
    }
    // TODO: return an anonymous Result if that's valid
    words
}
