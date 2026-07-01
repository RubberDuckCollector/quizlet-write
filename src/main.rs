use console::style;
use std::{thread, time};

mod file_reading;

fn main() {
    // TODO: write this proc
    file_reading::validate_cards();

    clear_screen();

    // thread::sleep(time::Duration::from_secs(1));

    let basque_family_members =
        "/Users/luna/flash-cards/languages/basque/self-study/family_members.txt".to_string();

    let words: Vec<Vec<String>> = file_reading::render_cards(&basque_family_members);
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

fn quiz() {}
