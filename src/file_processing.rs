use std::fs;
use std::io::{self, BufRead, Write};
use std::path::Path;

#[path = "./terminal_processing.rs"]
mod terminal_processing;

pub struct ValidateFileError(pub &'static str);

// https://doc.rust-lang.org/stable/rust-by-example/std_misc/file/read_lines.html#a-more-efficient-approach
pub fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<fs::File>>>
where
    P: AsRef<Path>,
{
    let file = fs::File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

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

    words
}

pub fn validate_cards<P>(filepath: P) -> Result<bool, ValidateFileError>
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

    let result = fs::exists(filepath);
    match result {
        // will not give an output if file DOES INDEED exist
        Ok(true) => Ok(true), // file exists
        Ok(false) => Err(ValidateFileError("File does not exist.")), // file does not exist
        Err(_) => Err(ValidateFileError("Couldn't check for file's existence.")), // fundamental error
    }
}
