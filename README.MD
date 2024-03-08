# Quizlet write my version
- Find the flash cards that work with this program here: https://github.com/RubberDuckCollector/subject-resources
- note: i recommend using this for german vocab where the plural conjugation is in brackets. the program will preserve contents in the brackets so you don't have to memorise what's in the brackets.
- e.g: the recipe - das Rezept *(-e)*

<details><summary>Disclaimer:</summary>
<code>results.txt</code> may have random vocab answers in it, i guess it can be a demonstration of what goes on during program execution and the file when you abort the program with Ctrl + C (contents of the file haven't been cleared yet) but it's mainly from my testing of the program
</details>

# Technical Explanation
<details><summary>Technical Explanation:</summary>
    <details><summary>Imports:</summary> <!-- IMPORTS -->
        <ol>
            <li><code>os</code>: used to detect the operating system the user is running the revision on, clears the terminal to make sure each question appears starting from the same place.</li>
            <li><code>sys</code>: used in conjunction with <code>os</code> to clear the terminal, also manages the command line arguments.</li>
            <li><code>time</code>: used to pause the program to let the user read what's on the screen. The text is also in different colours which makes it a bit easier to read because it stands out.</li>
            <li><code>random</code>: use <code>random.shuffle</code> to jumble up the key and value pairs in the <code></code> dict, they will be in a pseudo-random order when they're looped through if user specifies <code>--rand</code> in the command line arguments.</li>
        </ol>
    </details>
</details>

## 2023-02-20
- completed development of first revision
- if there are vocab files that are empty, that is known

## 2023-02-21
- starting development of more command line arguments (--randomise)

## 2023-02-22
- implemented command line arguments

## 2023-03-07
- i have new hint algorithms

## 2023-03-08
- i think i'm finally finished with it (the code)
- started development on the technical explanation

## next features


## future plans
- statistics and tracking

## lesson of the day
- if you want to combine function arguments with string parsing, don't rely on chatgpt at all
- 2023-03-07 update: i lied
