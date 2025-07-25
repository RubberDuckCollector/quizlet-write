# Table of contents

<!-- vim-markdown-toc GFM -->

* [Quizlet write my version](#quizlet-write-my-version)
* [Features](#features)
* [Why I made this](#why-i-made-this)
* [Disclaimer and Prerequisites](#disclaimer-and-prerequisites)
    * [input for the program:](#input-for-the-program)
* [Demo video (old)](#demo-video-old)
* [Notes](#notes)
* [Top Priority TODO](#top-priority-todo)
    * [Next features/TODO](#next-featurestodo)

<!-- vim-markdown-toc -->

# Quizlet write my version

- Find the flash cards that work with this program here: https://github.com/RubberDuckCollector/my-flash-cards
- note: i recommend using this for german vocab where the plural conjugation can be in brackets. the program will preserve contents in the brackets so you don't have to memorise what's in the brackets.
- e.g: the recipe - das Rezept*(-e)*

Build log: <https://github.com/RubberDuckCollector/quizlet-write/blob/main/BUILD_LOG.md>

# Features

- Overall, the same as Quizlet Write (type the answer on the flash card)
- Can have multiple sessions going at the same time (they're all tracked independently)
- Can generate cool graphs of how you did on each round of the quiz

# Why I made this

- I was getting annoyed at how I had to navigate the quizlet flash cards with tab and shift+tab, so I made a replica of their flash card system to give me more control over the vocab learning process. I can use my own editor (Vim) to write the flash cards instead of quizlet's one and use Vim remaps to insert text really fast into the flash cards
- No waiting for web page loads, just the program loading
- I have my own system for the format of flash cards now, so I can change the source code to my needs. E.g: I've incorportated a streak function and progress percentages -> more control, software can be tailored to my needs instead of living with an imperfect offering from a company serving the software to me
- This solution to flash cards is also ad-free.
- Because this program is open source, the user can clone this repo and edit their version of the source code to suit their specific needs, another benefit over Quizlet
- analysis of study patterns - `stats/cards-per-day.json` holds the number of flash cards studied on each day. JSON is easily machine-readable. Benefits:
    - [x] I can import the file to a progam and create a graph of my revision
        - [x] Data mining opportunities
    - Current drawbacks:
        - cannot filter activity by language.

# Disclaimer and Prerequisites

- **NOT TESTED/ADAPTED FOR WINDOWS, ONLY MACOS AND LINUX**
- ***For this reason. I personally recommend running this in WSL or changing the code to accommodate Windows if you want to use this program Windows.***
***"term" or "question" refers to just the question on the flash card.***
    - "definition" or "answer" refers to the answer on the flash card
    - "term" and "question" are interchangeable
    - "definition" and "answer" are interchangeable.
- Due to how [datetime](https://docs.python.org/3/library/datetime.html) formats the time, filenames may have colons in them. I don't know how these filenames behave on different systems.
- A "session" is one completion of all the flash cards from a file. A completed session means you've answered all the cards correctly at least once.
- If you wait until tomorrow to finish a session, you'll get credit for the day you finish the session on. e.g starting a session on the 1st of Jan. but finishing it on the 2nd will increase the cards done count for the 2nd of Jan., when the session is completed.
- I know how cursed this file is if you open it raw. Try not to think about it.

- a Python version >= 3.10 because of the `match` key word (this was built on python 3.12)
- [matplotlib](https://matplotlib.org/) (i install this with `/usr/local/bin/python3 -m pip install matplotlib` on my MacOS computer)
- a nerd font, set one of these in your terminal settings as the font <https://www.nerdfonts.com/>
- ***To type an umlaut by itself (¨)***
    - Mac: opt + u, then press Space
    - Linux: AltGr + ;, then press Escape, or press that button combination once more
    - Windows: With numlock on, hold down Alt and then press 0168, then release Alt.

## input for the program:
- a text file in the format `content|more-content`, on each line of the file like this:
```txt
hello (spanish)|hola
goodbye|adiós
how are you?|¿qué tal?
hello (japanese)|こんにちは
```
For the whole length of the file, save for empty lines and lines starting with a `#`. They'll be ignored by the program as code comments/handled separately.

# Demo video (old)

<https://youtu.be/rUKUTK_Q52E>

# Notes

none

# Top Priority TODO

- [ ] add a parity function to sync() that looks at sessions without a `session.json` file and retroactively creates it
    - [ ] add a function to sync() that corrects terms and sessions done on each day in `lifetime_stats.json["cards_per_day"]` and the same for sessions per day
        - need to get all session dir names, get all the text after the word "to" and parse that as a datetime object then go to each session.txt file for the specific day in question and count ONLY the ticks in each session.txt file and then overwrite the new figure in lifetime_stats.json
- [ ] make an optional command line argument that outputs the average and total number of sessions/flash cards done between 2 dates
- [ ] add a `--verbose` flag that prints to the user when each external module is loading when the program is executed
- [ ] make an automatic backup feature (basically duplicate all user data in a backup directory)
    - [ ] make the user able to restore from backup or manually overwrite backup
- [wip] break up `main.py` into many smaller files containing their own procedures
    - maybe separate ones for the hint system, the quiz, and others
- [ ] pretty print a flash card file
- [ ] implement a feature that allows the user to exit and save a session and resume a session
    - need to save `card_set` dict and the index of the current flash card
    - need to save the stats when the session is exited
    - need to save the time the session was started at
    - implement `--resume` command line argument that prompts an interactive selection mode for the saved sessions
    - need to take `start_time` as a parameter to `quiz()` if start time can be set arbritrarily by resuming a session
- [ ] compile the program to be shipped
- [ ] implement quizlet's bars that fill up and deplete as in the write mode according to the user's progress
    - [ ] for the progress through the quiz, make a progress bar
        - increment the bar when the progress is divisible by a certain number, which corresponds to a pre-mapped version of the progress bar
        - store the progress bar stages in a separate file and import them in `main.py`
- [wip] somewhat complete 2025-07-11: make a sync function that goes through all files in `records/` and counts how many ticks and crosses there are in each file, then overwrites those figures as the `lifetime_correct` and `lifetime_incorrect` stats in `lifetime_stats.json`
- [x] complete 2025-07-15: migrate to x.isalpha() (works for different alphabets) instead of a list of chars to ignore
- [x] complete 2025-07-15: make it so normal/easy hints show the first 1/3 letters (that is, return True from .isalpha()) as well as any non-alpha character, not just the old behaviour of showing the first 1/3 chars no matter what and possibly wasting the hint chars
    - maybe use counters but not decrement the counters when there's a non-alpha char
        - figure out when to put the counter check in the if statement branches
- [x] complete 2025-07-11: put the end of session data into a `session.json` file
- [x] complete 2025-07-11: added `--sync` optional argument that reads data from `stats/records` and overwrites `stats/lifetime_stats.json` with the data collected
- [x] complete 2025-07-10: implement an optional command line argument where the program switches the position of the term and answer on each line of a flash card file, creates a "{filename}_OUTPUT.txt" file
- [x] complete 2025-07-09: add lifetime session correct and lifetime session incorrect counters to the program that get printed out at the end of the session
- [x] make it so the key in the PDF graph is shown to the left of the plot instead of the right

## Next features/TODO

- [ ] use a proper logging system with a logging library
- [ ] optional command line argument that turns user input (except spaces) into * characters as they type
- [ ] make an automatic backup feature (basically duplicate all user data in a backup directory)- [ ] make the colours on the bar charts pretty
- [ ] a new command line argument where i use regex to highlight numbers and all 3 types of opening/closing brackets in a special colour
- [ ] implement a feature where at the end of a session, ask the user if they want to save the cards they got incorrect on the first round to a new file
    - file called `"{filename} {session_end_date_and_time} incorrect.txt"`
    - REQUIREMENTS: would need to make every session inside `stats/records` its own directory containing the record file and the graph
    - accuracy on the y axis, words done on the x axis
    - could do x axis as "cards remaining" and count down, or as "cards completed" and count up
    - could also do x axis as "% cards completed" or "% cards remaining"
    - this would be a measure of consistency
- [ ] implement a feature where the time taken to complete the quiz is written to the record file
- [ ] implement a feature where the command line arguments accept multiple files like this: `/file /file /file -difficulty -rand -flip`
    - files are appended to each other for the test (hold file paths in a list?)
    - maybe make the program run a bash script, integrating the `less` command or something idk
- [ ] add a fast mode where time.sleep() doesn't activate and the last term the user answered is displayed at the top of the screen as correct/incorrect
- [ ] add feature that puts the start and end date/times in the results file
- [ ] port the app to the blessed library and make it a fully featured TUI app
- [ ] turn it into a spaced repitition software
- [wip] implement a `-help` command line argument
    - can now calculate the average length of a flash card set/average time taken on a given day knowing the total number of cards studied and the total number sessions studied
    - implement it as a command line argument taken at the first position
- [x] complete 2025-07-11: put the data stored at the bottom of the session `txt` file in a separate file as JSON
- [x] mirgrate to argparse
- [x] streak feature (100% = perfect streak)
- [x] records system where the program dumps the contents of `results.txt` into a new file with the current date and time accurate to the second into a records dir
- [x] statistics and tracking - daily word count of cards done
- [x] expand --rand functionality to randomize at the end of each round, instead of only at the start of the session
- [x] tell the user the previous cards done today and the new cards done today
- [x] 2024-08-31: implement a feature that allows the user to have more than one session open at a time 
    - 11-10-2024: (this is done by having separate files tracking the progress of each session, no two files would conceivably be of the same session because the name is decided by time up to 6 digits on the second)
- [x] implement a feature that tracks every session's % correct and generates a line graph of the session
- [x] implement a feature where the command line arguments that are passed into the quiz are also written to the record file
- [x] add a stats tracker for the number of sessions finished in that day, not just the already established cards studied per day
- [x] implement a feature where the program ignores lines starting with a # in the flash card file. this allows me to put metadata in the flash card file and print it out when the session starts.
- [x] remove the 0/0 on the graph (2024-11-01)
- [x] might not be recording accuracy at 100% completion of the round PLEASE FIX (2024-11-01)
- [x] implement a feature where each round on the line graph has a different coloured line (2024-11-01)
- [x] write the path to flash cards on the graph title
- [x] make 2 txt files each for the data used to plot the x and y axis, saved under that session's particular dir
- [x] make the graph generated gradute in 1s instead of 5s (have to make the graph taller to do so)
- [x] add signals that tell the user the program is loading/importing libraries/when the program is first run and there's a big loading time, this would let the user that nothing's going wrong
    - maybe with a ... that increments
- [x] implement a feature that creates bar charts of how many sessions completed with each command line argument (e.g how many sessions with `-rand-once`/`-rand-every-round`/`-no-rand`? how many sessions with `-flip`/`-no-flip`? how many sessions with each difficuly?)
- [x] implement a feature that creates a bar chart with cards done on each day (Y axis) and date (X axis). days with 0 cards do not take up a space on the bar chart (maybe add an option to show all days regardless?)
- [x] make it so a string such as `test/test` renders as `t___/t___` on normal mode and `tes_/tes_` on easy mode instead of `t___/____`
- [x] sort out build log on github
- [x] ***make it so the graph only saves the relevant segment of the graph***
    - [x] make it so the saved graph adjusts to the relevant y axis coordinates that are saved
- [x] make it so the session and cards bar charts have a minimum size to accommodoate for bar charts with little data
- [x] fix warning that generates if the lower and greater values for the y axis are the same
- [x] implement a --test keyword that prevents stats from being saved but still allows the program to function normally otherwise
