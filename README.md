# Table of contents

<!-- vim-markdown-toc GFM -->

* [Quizlet write my version](#quizlet-write-my-version)
* [Install](#install)
* [Uninstall](#uninstall)
* [Hints](#hints)
    * [Hint settings](#hint-settings)
* [Features](#features)
* [Why I made this](#why-i-made-this)
* [Disclaimers and Prerequisites](#disclaimers-and-prerequisites)
    * [input for the program:](#input-for-the-program)
* [Demo video (old)](#demo-video-old)
* [Notes](#notes)

<!-- vim-markdown-toc -->

# Quizlet write my version

- Find the flash cards that work with this program here: https://github.com/RubberDuckCollector/my-flash-cards
- note: i recommend using this for german vocab where the plural conjugation can be in brackets. the program will preserve contents in the brackets so you don't have to memorise what's in the brackets.
- e.g: the recipe - das Rezept*(-e)*

[Click here for the build log](https://github.com/RubberDuckCollector/quizlet-write/blob/main/BUILD_LOG.md)

# Install

Run this command from where you want this project to be: `git clone https://github.com/RubberDuckCollector/quizlet-write.git`

# Uninstall

To uninstall, simply delete the folder you copied this project to. All of its data will be inside of that.

# Hints

The user types the answer to the flash card prompt.
There is a hint system for this app. For example, `easy` gives the user the first 3 characters of each space-separated word on the flash card, and `very-hard` removes the hint entirely.

## Hint settings

There are different hint settings. See help screen/potential error messages to see all hints. The current hints as of 2025-11-27 are:

| Hint name          | function                                                                             |
|--------------------|--------------------------------------------------------------------------------------|
| `easy`             | gives the user the first 3 characters of each space-separated word on the flash card |
| `normal`           | gives the first character of the flash card answer                                   |
| `hard`             | only gives content inside brackets `()` and symbols                                  |
| `hard-with-spaces` | same as `hard` but spaces `" "` are present instead of underscores `_`               |
| `very-hard`        | no hints!                                                                            |

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

# Disclaimers and Prerequisites

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
- [matplotlib](https://matplotlib.org/)
- a nerd font, set one of these in your terminal settings as the font <https://www.nerdfonts.com/>
- ***To type an umlaut by itself (¨)***
    - Mac: opt + u, then press Space
    - Linux: AltGr + ;, then press Escape, or press that button combination once more
    - Windows: With numlock on, hold down Alt and then press 0168, then release Alt.

## input for the program:

- a text file in the format `content|more-content`, on each line of the file like this:
```txt
hello (spanish)|hola
goodbye (spanish)|adiós
how are you? (spanish)|¿qué tal?
hello (japanese)|こんにちは
```
For the whole length of the file, save for empty lines and lines starting with a `#`. They'll be ignored by the program as code comments/handled separately.

# Demo video (old)

<https://youtu.be/rUKUTK_Q52E>

# Notes

none
