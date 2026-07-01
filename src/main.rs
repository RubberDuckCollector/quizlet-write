use console::style;
use std::collections::HashMap;
use std::fs;
use std::io::{self, BufRead, Write};
use std::path::Path;
use std::{thread, time};

fn clear_screen() {
    // std::process::Command::new("clear");
    clearscreen::clear().expect("failed to clear screen");
}

// https://doc.rust-lang.org/stable/rust-by-example/std_misc/file/read_lines.html#a-more-efficient-approach
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<fs::File>>>
where
    P: AsRef<Path>,
{
    let file = fs::File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn render_cards(filepath: &str) -> HashMap<&str, &str> {
    let mut words: HashMap<&str, &str> = HashMap::new();

    // read whole file
    // let result = fs::read_to_string(filepath);
    // match result {
    //     Ok(v) => println!("{}", v),
    //     Err(e) => panic!("Error while reading file: {}\n{}", filepath, e)
    // }

    if let Ok(lines) = read_lines(filepath) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines.map_while(Result::ok) {
            println!("{}", line);

            // TODO: strip whitespace
            // split on |
            // insert each 2 strings on a given line into the hashmap

            // println!("press ENTER to see next line.");
            // std::io::stdout().flush().unwrap(); // makes the text print immediately
            // let mut msg = "".to_string();
            // std::io::stdin().read_line(&mut msg).unwrap(); // input to pause execution after the colored text is done (can verify the screen works)

        }
    }


    words
}

fn quiz() {

}

fn main() {
    clear_screen();

    // thread::sleep(time::Duration::from_secs(1));

    let basque_family_members =
        "/Users/luna/flash-cards/languages/basque/self-study/family_members.txt".to_string();

    match render_cards(&basque_family_members).len() {
        0 => println!("CARD SET IS EMPTY"),
        _ => println!("CARD SET IS NOT EMPTY"),
    }

    // cards = render_cards(filepath);
    // quiz(cards);
}
