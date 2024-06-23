# Quizlet write my version
- Find the flash cards that work with this program here: https://github.com/RubberDuckCollector/subject-resources
- note: i recommend using this for german vocab where the plural conjugation is in brackets. the program will preserve contents in the brackets so you don't have to memorise what's in the brackets.
- e.g: the recipe - das Rezept *(-e)*

<details><summary>Disclaimer:</summary>
    <ul>
        <code>results.txt</code> may have random vocab answers in it, i guess it can be a demonstration of what goes on during program execution and the file when you abort the program with Ctrl + C (contents of the file haven't been cleared yet) but it's mainly from my testing of the program
        <p>I also know how cursed this file is if you open it raw. Try not to think about it.</p>
    </ul>
</details>

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

# Demo video
<https://youtu.be/rUKUTK_Q52E>

# Technical Explanation
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

- if you don't want the `records/` dict to have my records in it when you download the repo, just delete the files

# Build log

## 2024-02-20
- completed development of first revision
- if there are vocab files that are empty, that is known (2023-03-08 update: vocab is at <https://github.com/RubberDuckCollector/subject-resources>)
## 2024-02-21
- starting development of more command line arguments (--randomise)

## 2024-02-22
- implemented command line arguments

## 2024-03-07
- i have new hint algorithms

## 2024-03-08
- i think i'm finally finished with it (the code)
- started development on the technical explanation
- need to comment the whole code before starting on code lower than the `Color` class

## 2024-05-15
- added percentage correct next to correct counter (in brackets)
- added percentage progress

## 2024-05-15 14:33
- having trouble with the streak functionality and scope. idk how to actually do it

## next features
- [x] streak feature (100% = perfect streak)
- [x] records system where the program dumps the contents of `results.txt` into a new file with the current date and time accurate to the second into a records dir
- [x] statistics and tracking - daily word count of terms done
- [ ] a new command line argument where i use regex to highlight numbers in a special colour

## lesson of the day
- if you want to combine function arguments with string parsing, don't rely on chatgpt at all
- 2023-03-07 update: i lied
