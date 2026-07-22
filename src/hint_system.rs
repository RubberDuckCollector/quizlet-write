use ratatui::crossterm::style::Stylize;

const fn is_cjk_char(c: char) -> bool {
    matches!(c,
        '\u{3040}'..='\u{30FF}' |
        '\u{4E00}'..='\u{9FFF}' |
        '\u{3400}'..='\u{4DBF}' |
        '\u{F900}'..='\u{FAFF}'
    )
}

fn make_very_hard_hint() -> String {
    "No hints!".to_string()
}

fn make_hard_with_spaces_hint(msg: &str) -> String {
    let mut hint: String = String::with_capacity(msg.len());
    let mut inside_brackets: bool = false;

    for ch in msg.chars() {
        if ch == '(' || ch == '（' {
            inside_brackets = true;
            hint.push(ch);
        } else if ch == ')' || ch == '）' {
            inside_brackets = false;
            hint.push(ch);
        } else if inside_brackets {
            // always reveal the character to the user if we're inside a pair of brackets
            hint.push(ch);
        } else if !ch.is_alphabetic() {
            hint.push(ch);
        } else {
            // if we get here, it means the character has to be hidden from the user and replaced
            // with an underscore
            hint.push(if is_cjk_char(ch) { '　' } else { ' ' });
        }
    }

    hint
}

// fn make_hard_hint(msg: &str) -> &str {}

fn make_normal_hint(msg: &str) -> String {
    let mut hint: String = String::with_capacity(msg.len());
    let mut inside_brackets: bool = false;
    let mut given_chars_in_hint: u16 = 1;

    for ch in msg.chars() {
        if ch == '(' || ch == '（' {
            inside_brackets = true;
            hint.push(ch);
        } else if ch == ')' || ch == '）' {
            inside_brackets = false;
            hint.push(ch);
        } else if inside_brackets {
            // always reveal the character to the user if we're inside a pair of brackets
            hint.push(ch);
        } else if matches!(ch, '/' | '／' | '⁄' | '⧸') {
            // reset the count for normal mode, so the next char can be
            // revealed to the user as intended
            given_chars_in_hint = 1;
            hint.push(ch); // of course we want to append the slash itself to the hint
        } else if !ch.is_alphabetic() {
            if ch.is_whitespace() {
                // ALWAYS SHOW TO USER
                // reset the count if it's whitespace as these ALWAYS
                // are included in the hint, so we don't want them to steal the status of being
                // shown from the next character
                given_chars_in_hint = 1;
            }
            hint.push(ch);
        } else if given_chars_in_hint > 0 {
            // if we can reveal a character, do so and then decrement the count to keep proper track
            // of how the hint's formatted
            hint.push(ch);
            given_chars_in_hint -= 1;
        } else {
            // if we get here, it means the character has to be hidden from the user and replaced
            // with an underscore
            hint.push(if is_cjk_char(ch) { '＿' } else { '_' });
        }
    }

    hint
}

fn make_easy_hint(msg: &str) -> String {
    let mut hint: String = String::with_capacity(msg.len());
    let mut inside_brackets: bool = false;
    let mut given_chars_in_hint: u16 = 3;

    for ch in msg.chars() {
        if ch == '(' || ch == '（' {
            inside_brackets = true;
            hint.push(ch);
        } else if ch == ')' || ch == '）' {
            inside_brackets = false;
            hint.push(ch);
        } else if inside_brackets {
            // always reveal the character to the user if we're inside a pair of brackets
            hint.push(ch);
        } else if matches!(ch, '/' | '／' | '⁄' | '⧸') {
            // reset the count for normal mode, so the next char can be
            // revealed to the user as intended
            given_chars_in_hint = 3;
            hint.push(ch); // of course we want to append the slash itself to the hint
        } else if !ch.is_alphabetic() {
            if ch.is_whitespace() {
                // ALWAYS SHOW TO USER
                // reset the count if it's whitespace as these ALWAYS
                // are included in the hint, so we don't want them to steal the status of being
                // shown from the next character
                given_chars_in_hint = 3;
            }
            hint.push(ch);
        } else if given_chars_in_hint > 0 {
            // if we can reveal a character, do so and then decrement the count to keep proper track
            // of how the hint's formatted
            hint.push(ch);
            given_chars_in_hint -= 1;
        } else {
            // if we get here, it means the character has to be hidden from the user and replaced
            // with an underscore
            hint.push(if is_cjk_char(ch) { '＿' } else { '_' });
        }
    }

    hint
}

#[cfg(test)]
mod hint_tests {
    use super::*;

    #[test]
    fn test_normal_ascii_slash() {
        assert_eq!(make_normal_hint("hello/world"), "h____/w____");
    }

    #[test]
    fn test_normal_fullwidth_slash() {
        assert_eq!(make_normal_hint("hello／world"), "h____／w____");
    }

    #[test]
    fn test_normal_fraction_slash() {
        assert_eq!(make_normal_hint("a⁄b"), "a⁄b");
    }

    #[test]
    fn test_normal_mixed_slashes() {
        assert_eq!(make_normal_hint("hello/world／test"), "h____/w____／t___");
    }

    #[test]
    fn test_normal_with_parentheses() {
        assert_eq!(
            make_normal_hint("hello/world (test) example"),
            "h____/w____ (test) e______"
        );
    }

    #[test]
    fn test_hard_with_spaces_very_hard() {
        assert_eq!(make_very_hard_hint(), "No hints!");
    }

    #[test]
    fn test_hard_with_spaces_single_latin_word() {
        assert_eq!(make_hard_with_spaces_hint("hello"), "     "); // 5 spaces
    }

    #[test]
    fn test_hard_with_spaces_multiple_latin_words() {
        assert_eq!(make_hard_with_spaces_hint("hello world"), "           "); // 10 spaces
    }

    #[test]
    fn test_hard_with_spaces_with_slash() {
        assert_eq!(make_hard_with_spaces_hint("hello/world"), "     /     ");
    }

    #[test]
    fn test_hard_with_spaces_with_parentheses() {
        assert_eq!(make_hard_with_spaces_hint("(test)"), "(test)");
    }

    #[test]
    fn test_hard_with_spaces_preserve_non_alpha() {
        assert_eq!(make_hard_with_spaces_hint("abc 123 xyz!"), "    123    !");
    }

    #[test]
    fn test_hard_with_spaces_preserve_tabs_newlines() {
        assert_eq!(make_hard_with_spaces_hint("hi\t\nworld"), "  \t\n     ");
    }

    // === Full-width slash tests ===
    #[test]
    fn test_hard_with_spaces_fullwidth_slash() {
        assert_eq!(make_hard_with_spaces_hint("hello／world"), "     ／     ");
    }

    #[test]
    fn test_hard_with_spaces_mixed_slashes() {
        assert_eq!(make_hard_with_spaces_hint("a/b／c⁄d"), " / ／ ⁄ "); // All slashes preserved
    }

    // === CJK character tests ===
    #[test]
    fn test_hard_with_spaces_single_cjk_char() {
        assert_eq!(make_hard_with_spaces_hint("你"), "　"); // Full-width space
    }

    #[test]
    fn test_hard_with_spaces_cjk_word() {
        // 你好 = 2 CJK chars → 2 full-width spaces
        assert_eq!(make_hard_with_spaces_hint("你好"), "　　");
    }

    #[test]
    fn test_hard_with_spaces_cjk_with_latin() {
        // Mix: latin space + CJK full-width space + latin space
        assert_eq!(make_hard_with_spaces_hint("你hello"), "　     ");
    }

    #[test]
    fn test_hard_with_spaces_cjk_with_slash() {
        assert_eq!(make_hard_with_spaces_hint("你好／世界"), "　　／　　");
    }

    #[test]
    fn test_hard_with_spaces_cjk_katakana() {
        // カタカナ (katakana, 4 chars)
        assert_eq!(make_hard_with_spaces_hint("カタカナ"), "　　　　");
    }

    // === Mixed content tests ===
    #[test]
    fn test_hard_with_spaces_complex_mixed_input() {
        // hello/world (test) example
        // 5 + 1 + 5 + 1 + 6 + 1 + 7 = 26 chars total
        assert_eq!( make_hard_with_spaces_hint("hello/world (test) example"), "     /      (test)        ");
    }

    #[test]
    fn test_hard_with_spaces_numbers_preserved() {
        assert_eq!(make_hard_with_spaces_hint("pass123word"), "    123    ");
    }

    #[test]
    fn test_hard_with_spaces_underscore_and_symbols() {
        assert_eq!(make_hard_with_spaces_hint("hello_world@2024"), "     _     @2024");
    }

    // === Edge cases ===
    #[test]
    fn test_hard_with_spaces_single_char_latin() {
        assert_eq!(make_hard_with_spaces_hint("a"), " ");
    }

    #[test]
    fn test_hard_with_spaces_single_char_cjk() {
        assert_eq!(make_hard_with_spaces_hint("あ"), "　"); // hiragana
    }

    #[test]
    fn test_hard_with_spaces_only_punctuation() {
        assert_eq!(make_hard_with_spaces_hint("!!!"), "!!!");
    }

    #[test]
    fn test_hard_with_spaces_only_spaces() {
        assert_eq!(make_hard_with_spaces_hint("   "), "   "); // Spaces preserved
    }

    #[test]
    fn test_hard_with_spaces_roundtrip_length() {
        // Output length should match input length
        let inputs = [
            "hello",
            "hello/world",
            "你好世界",
            "(test)",
            "a1b2c3",
            "日本語テスト",
        ];

        for input in inputs {
            let output = make_hard_with_spaces_hint(input);
            assert_eq!(
                input.chars().count(),
                output.chars().count(),
                "Length mismatch for input: '{}'",
                input
            );
        }
    }

    #[test]
    fn test_hard_with_spaces_space_count_matches_alpha_count() {
        // Count spaces in output should equal count of alpha chars in input
        let input = "hello world";
        let output = make_hard_with_spaces_hint(input);

        assert_eq!(output.len(), input.len());
    }

    #[test]
    fn test_easy_ascii_slash() {
        assert_eq!(make_easy_hint("hello/world"), "hel__/wor__");
    }

    #[test]
    fn test_easy_fullwidth_slash() {
        assert_eq!(make_easy_hint("hello／world"), "hel__／wor__");
    }

    #[test]
    fn test_easy_fraction_slash() {
        assert_eq!(make_easy_hint("a⁄b"), "a⁄b");
    }

    #[test]
    fn test_easy_mixed_slashes() {
        assert_eq!(make_easy_hint("hello/world／test"), "hel__/wor__／tes_");
    }

    #[test]
    fn test_easy_with_parentheses() {
        assert_eq!(
            make_easy_hint("hello/world (test) example"),
            "hel__/wor__ (test) exa____"
        );
    }

    #[test]
    fn test_easy_with_spaces_underscore_and_symbols() {
        assert_eq!(make_easy_hint("hello_world@2024"), "hel________@2024");
    }

    #[test]
    fn test_easy_with_spaces_numbers_preserved() {
        assert_eq!(make_easy_hint("pass123word"), "pas_123____");
    }
}
