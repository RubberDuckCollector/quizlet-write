use rustyline::error::ReadlineError;
use rustyline::{DefaultEditor};

pub fn get_user_response() -> Result<String, ReadlineError> {
    // `()` can be used when no completer is required
    let mut rl = DefaultEditor::new()?;
    loop {
        let readline = rl.readline("> ");
        match readline {
            Ok(line) => {
                return Ok(line);
            }
            Err(ReadlineError::Interrupted) => {
                println!("CTRL-C");
                return Err(ReadlineError::Interrupted);
            }
            Err(ReadlineError::Eof) => {
                println!("CTRL-D");
                return Err(ReadlineError::Eof);
            }
            Err(err) => {
                println!("Error: {:?}", err);
                return Err(err)
            }
        }
    }
}
