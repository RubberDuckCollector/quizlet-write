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
                // split the string on | and then collect into Vec to allow for indexing
                // let splitted_trimmed_line: Vec<&str> = trimmed_line.split("|").collect::<Vec<_>>();

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
    // TODO:
    // 1. check if file exists
    // 2. check if file exists but not empty
    // 2.1. check presence of | (display line number)
    // 2.2. check if the only char on the line is |
    // 2.3. check if there are more than 1 | chars (display line number)
    // 2.4. check if no content to the left of |
    // 2.5. check if no content to the right of |

    // if output is ever inspected before an appropriate check returns Ok, it will be an error by
    // default
    let mut output: Result<(), String> =
        Err("I'm an error by default until the flashcards have been validated. Double check the code's logic!".to_string());
    assert!(output == Err("I'm an error by default until the flashcards have been validated. Double check the code's logic!".to_string()));

    match fs::exists(filepath) {
        Ok(true) => output = Ok(()),
        Ok(false) => {
            // file does not exist
            return Err("File does not exist.".to_string());
            // return output
        }
        Err(_) => {
            // fundamental error
            return Err("Couldn't check for file's existence.".to_string());
        }
    };

    // HOPEFULLY Ok(()) here
    // OTHERWISE Err("...") by default
    // all desired cases should be handled in the above branches
    output
}
