# Table of contents

<!-- vim-markdown-toc GFM -->

* [Quizlet write my version](#quizlet-write-my-version)
* [Features](#features)
* [Why I made this](#why-i-made-this)
* [Disclaimer](#disclaimer)
* [Prerequisites](#prerequisites)
    * [input for the program:](#input-for-the-program)
* [Optional](#optional)
* [Overview](#overview)
* [Demo video (old)](#demo-video-old)
* [Technical Explanation (WIP)](#technical-explanation-wip)
* [Notes](#notes)
* [Next features/TODO](#next-featurestodo)

<!-- vim-markdown-toc -->

# Quizlet write my version

- Find the flash cards that work with this program here: https://github.com/RubberDuckCollector/my-flash-cards
- note: i recommend using this for german vocab where the plural conjugation can be in brackets. the program will preserve contents in the brackets so you don't have to memorise what's in the brackets.
- e.g: the recipe - das Rezept *(-e)*

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
- analysis of study patterns - `stats/terms-per-day.json` holds the number of flash cards studied on each day. JSON is easily machine-readable. Benefits:
    - [x] I can import the file to a progam and create a graph of my study
        - [x] Data mining opportunities
    Current drawbacks:
        - cannot filter activity by language.

# Disclaimer

- **NOT TESTED/ADAPTED FOR WINDOWS, ONLY MACOS AND LINUX**
- **"terms" and "flash cards" are interchangable. "term" refers to both the question and answer on each side of the flash card.**
- **File names will have colons : in them, which is prohibited on Windows but not MacOS or Linux. I personally recommend running this in WSL or changing the code to accommodate Windows if you want to use this program Windows.**
- A "session" is one completion of all the flash cards from a file. A completed session means you've answered all the cards correctly at least once.
- If you wait until tomorrow to finish a session, you'll get credit for the day you finish the session on. e.g starting a session on the 1st of Jan. but finishing it on the 2nd will increase the terms done count for the 2nd of Jan., when the session is completed.
- I know how cursed this file is if you open it raw. Try not to think about it.
- If you don't want the `records/` dir to have my records in it when you download the repo, just delete the files

# Prerequisites

- a Python version past 3.10 (this was built on python 3.12)
- matplotlib (i install this with `/usr/local/bin/python3 -m pip install matplotlib` on my MacOS computer)
- a nerd font <https://www.nerdfonts.com/>

## input for the program:
- a text file in the format `content|more-content`, on each line of the file like this:
```txt
hello (spanish)|hola
goodbye|adiós
how are you?|¿qué tal?
hello (japanese)|こんにちは
```
for the whole length of the file, save for empty lines and starting with a `#`. They'll be ignored by the program as code comments/handled separately.

# Optional

# Overview

<details><summary>Overview:</summary>
    <ol type="1">
        <li>The user runs the program (e.g <code>python3 main.py ~/subject-resources/cards/languages/spanish/as/unit2.txt --normal --rand --noflip</code>). I have my flash cards at <code>~/subject-resources</code>.</li>
        <li>The program parses the flash cards. The format of the flash cards should be: <code>term|definition</code>. The cards are allowed to have () brackets, but each set of brackets has to be separate from each other embedded brackets shouldn't happen. For example, this is the only allowed formation: <code>term|definition (data1) (data2)</code></li>
        <li>The program asks the user the questions. The key is the question and the value is the answer.</li>
        <li>If the user gets the question right, the program will add that key and value pair to a new dictionary called <code>correct_answers</code>. The program also writes a line to <code>results.txt</code> with a tick on the left, the prompt on the left, and the answer on the right.</li>
        <li>If the user gets the question wrong, the program will tell the user. The program asks the user to confirm the answer, and if they don't, the program will write a line to <code>results.txt</code>, where there's a cross on the left, then the promt, then the answer.</li>
        <li>If the user inputs an empty string/answer made up of only spaces, the program will make them copy out the answer until they get it right. It then considers this as incorrect.</li>
    </ol>
</details>

# Demo video (old)

<https://youtu.be/rUKUTK_Q52E>

# Technical Explanation (WIP)

<details><summary>Technical Explanation:</summary>
    <ul> <!-- DON'T USE LIST ELEMENTS ON THIS LIST, THIS LIST IS HERE TO CREATE INDENTATION -->
        <details><summary><b>Files:</b></summary>
            <ul>
                <li>
                    <p><u>File structure:</u></p>
                    <pre>
                        <code>
.
├── LICENSE
├── README.md
├── __pycache__
│   └── constants.cpython-312.pyc
├── constants.py
├── main.py
├── results.txt
└── tests
    ├── graveyard.py
    ├── test.py
    ├── test2.py
    ├── test3.py
    └── test4.py
                        </code>
                    </pre>
                </li>
                <li><a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/constants.py"><code>constants.py</code></a>: contains the <code>chars_to_ignore</code> list. It's in the file because It can be imported to all my test files. It lets me manage a global variable across many scripts, making it easy to test code in different files with a known piece of data. Being requireable in a separate file makes it easier to debug too. I want all my tests and <code>main.py</code> to be on the same page and working with the same constants.</li>
                <li><code>main.py</code>: stores all of the logic of the program. Run this file to use it</li>
                <li><code>README.md</code>: this file.</li>
                <li><code>constants.py</code>: contains <code>chars_to_ignore</code> and is imported by my python scripts</li>
                <li><code>LICENSE</code>: license</li>
                <li><code>tests/</code>: contains files I've used to test python code that I've later added to <code>main.py</code>. I used these test files becauase I don't want to test within <code>main.py</code> to prevent something bad from happening. Feel free to poke around and read the shitty code</li>
            </ul>
        </details>
        <details><summary><strong>The code:</strong></summary> <!-- THE CODE -->
            <ul>
                <li>I'll try to cover this line by line going downwards through the file</li>
                <li>But this may not be possible because it's really hard</li>
                <li>There may not be links to line numbers, and instead there'll be a reference of what is written <code>like this</code> because keeping this file up to date with line numbers that can change is a very daunting task. This is also only my second documentation project (apart from the ocr-programming-challenges) and it's also daunting because of that. I want to keep it at least somewhat easy for myself.</li>
            </ul>
            <ul> <!-- DON'T USE LIST ELEMENTS ON THIS LIST, THIS LIST IS HERE TO CREATE INDENTATION -->
                <details><summary><u>Imports:</u></summary> <!-- IMPORTS -->
                    <ol type="1">
                        <li><code class="language-python">os</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L1"><code>main.py</code></a>: used to detect the operating system the user is running the revision on, clears the terminal to make sure each question appears starting from the same place. https://docs.python.org/3/library/os.html</li>
                        <li><code>sys</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L2"><code>main.py</code></a>: used in conjunction with <code>os</code> to clear the terminal, also manages the command line arguments. https://docs.python.org/3/library/sys.html</li>
                        <li><code>time</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L3"><code>main.py</code></a>: used to pause the program to let the user read what's on the screen. The text is also in different colours which makes it a bit easier to read because it stands out. https://docs.python.org/3/library/time.html</li>
                        <li><code>random</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L4"><code>main.py</code></a>: I used <code>random.shuffle</code> to jumble up the key and value pairs in the <code>cards</code> dict, they will be in a pseudo-random order when they're looped through if user specifies <code>--rand</code> in the command line arguments. https://docs.python.org/3/library/random.html</li>
                        <li><code>readline</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L5"><code>main.py</code></a>: this library attaches onto the builtin python <code>input</code> procedure, it adds support for UP arrow bringing back your last input, pasting from clipboard, arrow keys etc. It's really helpful if you mistype something and only have to change 1 letter, press UP and your previous answer will come back. https://stackoverflow.com/questions/45772230/arrow-keys-not-working-while-entering-data-for-input-function</li>
                        <li><code>platform</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L6"><code>main.py</code></a>: need this to add Windows support. See <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L40"><code>here</code></a> for its usage. https://docs.python.org/3/library/platform.html https://www.geeksforgeeks.org/platform-module-in-python/</li>
                        <li><code>from constants import chars_to_ignore</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L7"><code>main.py</code></a>: I'm importing/requiring <code>chars_to_ignore</code> from <code>constants.py</code> (the <code>.py</code> extension is not needed here). The <code>chars_to_ignore</code> list is now able to be used throughout <code>main.py</code>. https://www.educative.io/answers/how-to-import-custom-module-in-python</li>
                    </ol>
                </details>
                <details><summary><u>Other data:</u></summary>
                    <ul>
                        <li>Class <code>Color</code> in <a href="https://github.com/RubberDuckCollector/quizlet-write/blob/main/main.py#L13"><code>main.py</code></a>: This defines the colours that the terminal can use. Python can print to the terminal using these colours. This is useful to me because showing important elements of the program's output to the user in different colours increases the program's usability. This isn't an import because it doesn't need to be. I'm only using this in one file.</li>
                    </ul>
                </details>
            </ul>
        </details>
    </ul>
</details>

# Notes

none

# Next features/TODO

- [x] streak feature (100% = perfect streak)
- [x] records system where the program dumps the contents of `results.txt` into a new file with the current date and time accurate to the second into a records dir
- [x] statistics and tracking - daily word count of terms done
- [x] expand --rand functionality to randomise at the end of each round, instead of only at the start of the session
- [x] tell the user the previous terms done today and the new terms done today
- [x] 2024-08-31: implement a feature that allows the user to have more than one session open at a time 
    - 11-10-2024: (this is done by having separate files tracking the progress of each session, no two files would conceivably be of the same session because the name is decided by time up to 6 digits on the second)
- [x] implement a feature that tracks every session's % correct and generates a line graph of the session
- [x] implement a feature where the command line arguments that are passed into the quiz are also written to the record file
- [x] add a stats tracker for the number of sessions finished in that day, not just the already established terms studied per day
- [x] implement a feature where the program ignores lines starting with a # in the flash card file. this allows me to put metadata in the flash card file and print it out when the session starts.
- [x] remove the 0/0 on the graph (2024-11-01)
- [x] might not be recording accuracy at 100% completion of the round PLEASE FIX (2024-11-01)
- [x] implement a feature where each round on the line graph has a different coloured line (2024-11-01)
- [x] write the path to flash cards on the graph title
- [x] make 2 txt files each for the data used to plot the x and y axis, saved under that session's particular dir
- [x] make the graph generated gradute in 1s instead of 5s (have to make the graph taller to do so)
- [x] add signals that tell the user the program is loading/importing libraries/when the program is first run and there's a big loading time, this would let the user that nothing's going wrong
    - maybe with a ... that increments
    - or integrate a logging system (with proper standardised logging library)
- [x] implement a feature that creates bar charts of how many sessions completed with each command line argument (e.g how many sessions with `-rand-once`/`-rand-every-round`/`-no-rand`? how many sessions with `-flip`/`-no-flip`? how many sessions with each difficuly?)
- [x] implement a feature that creates a bar chart with terms done on each day (Y axis) and date (X axis). days with 0 terms do not take up a space on the bar chart (maybe add an option to show all days regardless?)
- [x] make it so a string such as `test/test` renders as `t___/t___` on normal mode and `tes_/tes_` on easy mode instead of `t___/____`
- [wip] break up `main.py` into many smaller files containing their own procedures
    - maybe separate ones for the hint system, the quiz, and others
- [wip] implement a `-help` command line argument
    - can now calculate the average length of a flash card set/average time taken on a given day knowing the total number of terms studied and the total number sessions studied
    - implement it as a command line argument taken at the first position
- [ ] implement an optional command line argument where the program switches the position of the term and answer on each line of a flash card file
- [ ] implement a feature that allows the user to exit and save a session and resume a session
    - need to save `card_set` dict and the index of the current flash card
    - need to save the stats when the session is exited
    - need to save the time the session was started at
- [ ] sort out build log on github
- [ ] make it so the session and terms bar charts have a minimum size to accommodoate for bar charts with little data
- [ ] compile the program to be shipped
- [ ] make an optional command line argument that outputs the average number of sessions/flash cards done between 2 dates and overall
- [ ] mirgrage to argparse
- [ ] make the colours on the bar charts pretty
- [ ] a new command line argument where i use regex to highlight numbers and all 3 types of opening/closing brackets in a special colour
- [ ] implement a feature where at the end of a session, ask the user if they want to save the terms they got incorrect on the first round to a new file
    - file called `"{filename} {session_end_date_and_time} incorrect.txt"`
    - REQUIREMENTS: would need to make every session inside `stats/records` its own directory containing the record file and the graph
    - accuracy on the y axis, words done on the x axis
    - could do x axis as "terms remaining" and count down, or as "terms completed" and count up
    - could also do x axis as "% terms completed" or "% terms remaining"
    - this would be a measure of consistency
- [ ] implement a feature where the time taken to complete the quiz is written to the record file
- [ ] implement a feature where the command line arguments accept multiple files like this: `/file /file /file -difficulty -rand -flip`
    - files are appended to each other for the test (hold file paths in a list?)
    - maybe make the program run a bash script, integrating the `less` command or something idk
- [ ] add a fast mode where time.sleep() doesn't activate and the last term the user answered is displayed at the top of the screen as correct/incorrect
- [ ] add feature that puts the start and end date/times in the results file
- [ ] for the progress through the quiz, make a progress bar
    - increment the bar when the progress is divisible by a certain number, which corresponds to a pre-mapped version of the progress bar
    - store the progress bar stages in a separate file and import them in `main.py`
- [ ] put the data stored at the bottom of the session `txt` file in a separate file as JSON
- [ ] port the app to the blessed library and make it a fully featured TUI app
