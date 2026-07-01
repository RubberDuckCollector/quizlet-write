use console::style;
use std::collections::BTreeMap;
use std::collections::HashMap;
use std::fs;
use std::io::{self, BufRead, Write};
use std::path::Path;
use std::{thread, time};
use itertools::Itertools;

fn main() {
    validate_cards();

    clear_screen();

    // thread::sleep(time::Duration::from_secs(1));

    let basque_family_members =
        "/Users/luna/flash-cards/languages/basque/self-study/family_members.txt".to_string();

    let words: Vec<Vec<String>> = render_cards(&basque_family_members);
    println!("{:#?}", words);

    // for (key, value) in words {
    //     println!("{}, {}", key, value);
    // }

    // match render_cards(&basque_family_members).len() {
    //     0 => println!("CARD SET IS EMPTY"),
    //     _ => println!("CARD SET IS NOT EMPTY"),
    // }

    // cards = render_cards(filepath);
    // quiz(cards);

    // let mut test_vec: Vec<Vec<String>> = vec![vec!["hello".to_string(), "world".to_string()], vec!["test1".to_string(), "test2".to_string()]];
    // println!("{:?}", test_vec);

    // test_vec[1].remove(0);
    // println!("{:?}", test_vec);

}

pub fn clear_screen() {
    // std::process::Command::new("clear");
    clearscreen::clear().expect("failed to clear screen");
}

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

fn quiz() {}
