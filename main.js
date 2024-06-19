const fs = require('fs');
const prompt = require('prompt-sync')();
const charsToIgnore = require('./constants')

function assert(condition, message) {
    if (!condition) {
        throw new Error(message || "Assertion failed");
    }
}

// to be used in quiz proc
class Streakcounter {
    constructor() {
        this.currentStreak = 0;
        this.maxStreak = 0;
    }

    incrementStreak() {
        // increment the current streak by one
        this.currentStreak++;

        // if the current streak then exceeds the max, it must mean there's a new highest
        // therefore reassign max_streak to current_streak
        if (this.currentStreak > this.maxStreak) { this.maxStreak = this.currentStreak };
    }

    resetStreak() { this.currentStreak = 0; }

    getCurrentStreak() { return this.currentStreak; }

    getMaxStreak() { return this.maxStreak; }
}

// msg: String
function makeVeryHardHint(msg) {
    return "No hints!";
}

// msg: String
function makeHardHint(msg) {
    var hint = "";

    var insideBrackets = false;

    for (let i = 0; i < msg.length; i++) {
        if (charsToIgnore.includes(msg[i])) {
            // if char should be preserved when hint is being built

            hint += msg[i];
        } else if (msg[i] === "(") {
            // if we're currently looking at a (
            // inside_brackets will be assigned True
            // add the(to the hint

            hint += "(";
            insideBrackets = true;
        } else if (msg[i] === ")") {
            // if we're at the end of the bracket
            // add the ) to the hint
            // inside_brackets becomes False

            hint += ")";
            insideBrackets = false;
        } else if (insideBrackets === true) {
            // add the character stright to the hint
            // we want to preserve the characters inside brackets
            // into the hint
            // therefore they shouldn't be an _ underscore

            hint += msg[i];
        } else {
            // if we're not in brackets
            // the character is neither of(or)
            // and the character isn't in charsToIgnore
            // it must be turned into an _

            hint += "_";
        }
    }

    return hint;
}

// msg: String
function makeNormalHint(msg) {
    var hint = "";
    var myMsg = msg.toArray();

    var i = 0;

    var insideBrackets = false;

    while (true) {
        try {
            if (charsToIgnore.includes(msg[i])) {
                hint += msg[i];
            } else {
                if (msg[i] === "(") {
                    insideBrackets = true;
                    hint += msg[i]
                } else if (msg[i] == ")") {
                    insideBrackets = false;
                    hint += msg[i];
                } else if (insideBrackets === true) {
                    hint += msg[i];
                } else {
                    if (msg[i] === 0 || msg[i - 1] === " ") {
                        hint == msg[i];
                    } else { hint += "_"; }
                }
            }
            i++;
        } catch (RangeError) {
            break;
        }
    }

    return hint;
}

// msg: String
function makeEasyHint(msg) {
    var hint = "";
    var myMsg = toArray(msg);

    var i = 0;
    var insideBrackets = false;

    while (true) {
        try {
            if (charsToIgnore.includes(msg[i])) {
                insideBrackets = true;
                hint += msg[i];
            } else {
                if (msg[i] === "(") {
                    insideBrackets = true;
                    hint += msg[i];
                } else if (insideBrackets === true) {
                    hint += msg[i];
                } else if (msg[i] === ")") {
                    insideBrackets = false;
                    hint += msg[i];
                } else {
                    if (i === 0 || msg[i - 1] === " ") {
                        hint += msg[i];
                    } else if (msg[i - 2] === " " || i == 1) {
                        hint += msg[i];
                    } else if (msg[i - 3] === " " || i == 2) {
                        hint += msg[i];
                    } else { hint += "_"; }
                }
            }
        } catch (RangeError) {
            break;
        }
    }

    return hint;
}

function sleep(ms = 0) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function clearScreen() {
    console.log('\x1b[2J');
}

// cardSet: Object
// difficulty: String
async function quiz(cardSet, difficulty) {
    var correctAnswers = {};
    var roundNum = 0; // will be incremented on the first pass, so there won't be a round 0

    const maxLeftLength = Math.max(...Object.keys(cardSet).map(left => left.length));

    var quizCounter = new Streakcounter();

    const RESULTS_FILE_PATH = "./results.txt";

    fs.appendFileSync(RESULTS_FILE_PATH, `cards from: ${process.argv[2]}`);

    while (cardSet.length !== 0) {
        roundNum++;

        var numCorrect = 0;
        var numAnswered = 0;
        var numIncorrect = 0;
        var numRemaining = cardSet.length;
        const NUM_TERMS = cardSet.length;
        const THEORETICAL_MAX_STREAK = NUM_TERMS;

        fs.appendFileSync(RESULTS_FILE_PATH, `Round num: ${roundNum}`);

        for (let key of Object.keys(cardSet)) {
            let answer = cardSet[key];

            var hint;
            switch (difficulty) {
                case "--easy":
                    hint = makeEasyHint(answer);
                    break;
                case "--normal":
                    hint = makeNormalHint(answer);
                    break;
                case "--hard":
                    hint = makeHardHint(answer);
                    break;
                case "--vary-hard":
                    hint = makeVeryHardHint(answer);
                    break;
                default:
                    console.log("Error while switching on difficulty in quiz procedure")
            }

            var currentPercentCorrect;
            if (numAnswered > 0) {
                currentPercentCorrect = Math.round((numCorrect / numAnswered), 2) * 100;
            } else { currentPercentCorrect = 0.0; }

            var progress;
            if (numAnswered > 0) {
                progress = round((numAnswered / NUM_TERMS), 2);
            } else { progress = 0.0 }

            console.log(`Remaining: ${numRemaining}`);
            console.log(`Correct: ${numCorrect} (${currentPercentCorrect})`);
            console.log(`Incorrect: ${numIncorrect}`);
            console.log(`Progress: ${progress}`);
            console.log(`Streak: ${quizCounter.getCurrentStreak()} (${quizCounter.getMaxStreak()})`);
            console.log(`What's the answer to ${userInput}?`);
            console.log(`Hint: ${hint}`);

            var userResponse = prompt("> ").trim(); // remove trailing and leading white space from answers
            // if the user hasn't supplied an input at all
            if (!userResponse) {
                console.log("Don't know? Copy out the answer so you remember it!");
                quizCounter.resetStreak();

                while (true) {
                    userResponse = prompt(`Copy the answer below ↓\n- ${answer}\n> `);
                    if (userResponse.toLowerCase() === answer.toLowerCase()) {
                        console.log("Next question.");
                        await sleep(500);
                        clearScreen();
                        break;
                    } else {
                        console.log("Try again.");
                    }
                }
                fs.appendFileSync(RESULTS_FILE_PATH, `✗ ${userInput.padEnd(maxLeftLength)} ${answer}\n`);
                numIncorrect++;
            } else {
                if (userResponse === answer) {
                    console.log("Correct. Well done!");

                    quizCounter.incrementStreak();
                    numCorrect++;

                    await sleep(500);
                    clearScreen();

                    fs.appendFileSync(RESULTS_FILE_PATH, `✓ ${userInput.padEnd(maxLeftLength)} ${answer}\n`);

                    var keyToCopy = key;
                    if (cardSet.includes(keyToCopy)) {
                        correctAnswers[keyToCopy] = cardSet[keyToCopy];
                    }

                } else if (userResponse.toLowerCase() === answer.toLowerCase()) {
                    console.log("Correct");
                    quizCounter.incrementStreak();
                    numCorrect++;

                    sleep(500);
                    clearScreen();

                    fs.appendFileSync(RESULTS_FILE_PATH, `✓ ${userInput.padEnd(maxLeftLength)} ${answer}\n`);

                    var keyToCopy = key;
                    if (cardSet.includes(keyToCopy)) {
                        correctAnswers[keyToCopy] = cardSet[keyToCopy];
                    }
                }
            }
        }





    }

}

function renderCards(filePath) {
    let renderedCards = {};

    const contents = fs.readFileSync(filePath, 'utf8');
    const lines = contents.split('\n');

    for (const line of lines) {
        if (line.trim() !== '') {
            const [key, value] = line.trim().split('|');
            renderedCards[key.trim()] = value.trim();
        }
    }

    return renderedCards;
}

function main() {
    let filePath = process.argv[2];

    console.log(filePath);

    let cards = renderCards(filePath);

    console.log(cards);
    quiz(cards);
}

main();
