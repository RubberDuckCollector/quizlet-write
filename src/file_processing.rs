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

// TODO: make it so it returns a Result<<Vec<Vec<String>>>, String>
// do a match on this in `main()` to catch errors
pub fn render_cards<P>(filepath: P) -> Vec<Vec<String>>
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

/// Returns nothing if flashcards have valid formatting, else returns a String which is handled in
/// `main()`
pub fn validate_cards<P>(filepath: P) -> Result<(), String>
where
    P: AsRef<Path>,
{
    let separator: &str = "|";
    let separators_per_line: u8 = 1;

    fn separator_exists(line: &String, sep: &str) -> bool {
        line.contains(sep)
    }

    fn is_separator_only_char(line: &String, sep: &str) -> bool {
        line.len() == sep.len() && line.contains(sep)
    }

    fn separator_too_many(line: &String, sep: &str, expected_num: &u8) -> (u8, bool) {
        let mut too_many_separators: bool = false;
        let separator_count: u8 = line.matches(sep).count().try_into().unwrap();
        if separator_count > *expected_num {
            too_many_separators = true;
        }
        (separator_count, too_many_separators)
    }

    fn separator_content_exists(line: &String, sep: &str) -> Result<(), String> {
        // a separator cannot be on the left OR right ends of the line
        // 2 or more separators cannot be directly next to each other
        if true {
            Ok(())
        } else {
            Err("".to_string())
        }
    }

    let mut output: Result<(), String> =
        Err("I'm an error by default until the flashcards have been validated. Double check the code's logic!".to_string());
    assert!(output == Err("I'm an error by default until the flashcards have been validated. Double check the code's logic!".to_string()));

    match fs::exists(&filepath) {
        Ok(true) => output = Ok(()),
        Ok(false) => {
            return Err("File does not exist.".to_string());
        }
        Err(_) => {
            // fundamental error
            return Err("Couldn't check for file's existence.".to_string());
        }
    };

    // TODO:
    // - [x] 1. check if file exists
    // - [x] 2. check if file exists but empty
    // - [x] 2.1. check presence of | (display line number)
    // - [x] 2.2. check if the only char on the line is |
    // - [x] 2.3. check if there are more than `expected_count` | chars (display line number)
    // 2.4. check if no content to the left of |
    // 2.5. check if no content to the right of |
    //      2.6: infer that there has to be content on both sides of every separator

    // if the file exists, try to return an Err by doing formatting checks
    if output == Ok(()) {
        if fs::read_to_string(&filepath)
            .expect("Should have been able to read the file")
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
                    let msg: String = format!(
                        "LINE {}: The designated separator ({}) wasn't found.",
                        &line_number, separator
                    );
                    return Err(msg);
                }

                if is_separator_only_char(&line, separator) {
                    let msg: String = format!(
                        "LINE {}: The designated separator ({}) was the only character the line. The line needs a prompt and an answer on the left and right sides of the separator ({}) respectively.",
                        &line_number, separator, separator
                    );
                    return Err(msg);
                }

                match separator_too_many(&line, separator, &separators_per_line) {
                    (sep_count, true) => {
                        let msg: String = format!(
                            "LINE {}: The designated separator ({}) appeared {} times -- more than the desired {} times.",
                            &line_number, separator, sep_count, &separators_per_line);
                        return Err(msg)
                    },
                    (_, false) => () // do nothing if it returns false
                }


            }
        }
    }

    // HOPEFULLY Ok(()) here
    // OTHERWISE Err("...") by default
    // all desired cases should be handled in the above branches
    output
}
