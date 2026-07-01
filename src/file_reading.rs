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

pub fn render_cards(filepath: &str) -> Vec<Vec<String>> {
    let mut words: Vec<Vec<String>> = Vec::new();

    // read whole file
    // let result = fs::read_to_string(filepath);
    // match result {
    //     Ok(v) => println!("{}", v),
    //     Err(e) => panic!("Error while reading file: {}\n{}", filepath, e)
    // }

    if let Ok(lines) = read_lines(filepath) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines.map_while(Result::ok) {
            // trim the whitespace off either side
            let trimmed_line: &str = line.trim();

            // split the string on | and then collect into Vec to allow for indexing
            // let splitted_trimmed_line: Vec<&str> = trimmed_line.split("|").collect::<Vec<_>>();

            if let Some((term, definition)) = trimmed_line.split_once('|') {
                // convert the borrowed &str halves into owned Strings
                // so everything is owned and can be looped on an returned safely
                words.push(vec![term.to_string(), definition.to_string()]);
            }

        }
    }

    words
}
