const fs = require('fs');

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

// hint: String
function makeVeryHardHint(hint) {
    return "No hints!";
}

// hint: String
function makeHardHint(hint) {
    return hint.length;
}

// card_set: Object
// difficulty: String
function quiz(cardSet: object, difficulty: string) {
    var correctAnswers = {};
    var roundNum = 0; // will be incremented on the first pass, so there won't be a round 0

    const maxLeftLength = Math.max(...Object.keys(cardSet).map(left => left.length));

}

function renderCards(filepath) {
    var renderedCards = {};

    try {
        const data = fs.readFileSync(filepath, 'utf8');

        // Split the file content into lines
        const lines = data.split('\n');

        // Process each line
        lines.forEach(line => {
            // Trim the line and split it by '|'
            const [key, value] = line.trim().split('|');

            // Ensure both key and value are present
            if (key && value) {
                renderedCards[key.trim()] = value.trim();
            } else {
                throw new Error("Error while checking for both key and value presence. I think there's a problem with the cards I'm trying to parse");
            }
        });

    } catch (err) {
        console.error('Error reading the file:', err);
    }

    return renderedCards;
}

function main() {
    let filePath = process.argv[2];

    console.log(filePath);

    let cards = renderCards(filePath);

    // quiz(cards);
}

main();

