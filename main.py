import os
import re
import sys
import time
import random
import readline
import platform

# static analyser might say readline is unused but it attaches to the input() func

# my_pattern = re.compile(r'[^.,\s)-]')
my_pattern = re.compile(r'[^(.,\s)-/]')
# my_pattern = re.compile(r'[^A-z().,!\s\-\?{}äëïöüÄËÏÖÜ0-9]', re.IGNORECASE)
# my_pattern = re.compile(r'(\([^)]*\)|[^.,!?()\s-])')
# my_pattern = re.compile(r'[\(\)][^(]*\)')


class Color:
    Red = "\033[031m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[96m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"
    Warn = "\033[93m"
    Underline = "\033[4m"
    Bold = "\033[1m"
    Hidden = "\033[8m"
    Blink = "\033[5m"
    Dim = "\033[2m"
    Reverse = "\033[7m"
    Reset = "\033[0m"


# we can emulate the rounds that quizlet write has by looping over the dict
# keep track of the cards the user has gotten correct by adding it to a seperate dict
# when the user answers the last card, remove the ones they got correct
# that will be the next round
# use a while loop for as long as the dict isn't empty

# session review system:
# most sensible move seems to be to write the rounds to a file as the session progresses
# when the session finishes, print the contents of the file

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_round_summary(filename: str, target_string: str, num_correct: int, num_answered: int):
    found = False
    with open(filename, 'r') as file:
        for line in file:
            if found:
                # print the line without leading/trailing whitespaces
                if '✓' in line:  # check for tick
                    print("\x1b[32m" + line.strip() +
                          "\x1b[0m")  # print in green
                elif '✗' in line:  # check for cross
                    print("\x1b[31m" + line.strip() +
                          "\x1b[0m")  # print in red
                else:
                    print(line.strip())  # otherwise don't colour the line
            elif target_string in line:
                found = True
                # don't print the line containing "Round <num>:"
                pass
    if not found:
        print("Target string not found in the file.")

    print(
        f"Score: {num_correct}/{num_answered} ({num_correct / num_answered * 100}%)")
    with open(filename, "a") as f:
        f.write(
            f"Score: {num_correct}/{num_answered} ({num_correct / num_answered * 100}%)")

    print()


# ORIGINAL FUNCTION, DON'T TOUCH
def make_hint(answer: str, difficulty: str) -> str:
    # if there's a punctuation mark in any of the words of the term, show them
    hint = ""
    match difficulty:
        case "--easy":
            for word in answer.split():
                if len(word) <= 3:
                    hint += word + " "
                else:
                    first_three = word[:3]
                    remaining = re.sub(my_pattern, '_', word[3:])
                    hint += first_three + remaining + " "
        case "--normal":
            for word in answer.split():
                first_letter = word[0]
                remaining = re.sub(my_pattern, '_', word[1:])
                hint += first_letter + remaining + " "
        case "--hard":
            for word in answer.split():
                hint += re.sub(my_pattern, '_', word) + " "
        case "--very-hard":
            hint = "No hints!"

    return hint.strip()


def quiz(card_set: dict, difficulty: str):

    correct_answers = {}
    round_num = 0

    # find the length of the longest term on the left
    max_left_length = max(len(left) for left in card_set.keys())

    # calculate the distance to the next tab stop
    tab_stop = 8
    tab_distance = tab_stop - (max_left_length % tab_stop)

    # print the aligned terms
    # for left, right in card_set.items():
    #     print(left.ljust(max_left_length),
    #           right.rjust(len(right) + tab_distance))

    with open("results.txt", "w") as f:
        while len(card_set) != 0:
            round_num += 1
            num_correct = 0
            num_answered = 0

            f.write(f"Round {round_num}:\n")
            f.flush()

            for prompt, answer in card_set.items():

                # the hint is the result of a call of make_hint()
                hint = make_hint(card_set[prompt], difficulty)

                num_answered += 1

                # print(i) -> print the first side of the card
                # print(card_set[i]) -> print the answer/other side of the card
                # print(hint) -> print the hint for the answer

                user_response = input(
                    f"What's the answer to '{Color.LightMagenta}{prompt}{Color.Reset}'?\nHint: {hint}\n> ").strip()

                # if the user input is falsy
                # i.e there were only spaces and strip() has removed them
                # to leave an empty string
                if not user_response:
                    print("Don't know? Copy out the answer so you remember it!")
                    while True:
                        user_response = input(
                            f"Copy the answer below ↓\n- {answer}\n> ")
                        # if user_response.lower() == card_set[prompt].lower():
                        if user_response.lower() == answer.lower():
                            print(f"{Color.Cyan}Next question{Color.Reset}")
                            time.sleep(0.5)
                            clear_screen()
                            break
                        else:
                            print("Try again")
                    # mark as incorrect as the user doesn't know the answer
                    f.write(
                        f"✗ {prompt.ljust(max_left_length)} {answer}\n")
                    f.flush()
                else:
                    if user_response == answer:
                        print(f"{Color.Green}Correct{Color.Reset}")

                        num_correct += 1

                        time.sleep(0.5)
                        clear_screen()

                        f.write(
                            f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                        f.flush()
                        clear_screen()

                        key_to_copy = prompt
                        if key_to_copy in card_set:
                            correct_answers[key_to_copy] = card_set[key_to_copy]

                    else:
                        # ask for override
                        print(f"{Color.Red}Incorrect.{
                            Color.Reset} Answer: {Color.LightYellow}{card_set[prompt]}{Color.Reset}")

                        override = input(
                            "Override as correct? (empty answer = don't override) ").strip()

                        # if override has something in it
                        if override:
                            # mark as correct as the user wishes
                            print(f"Overridden as {
                                Color.Green}Correct{Color.Reset}.")

                            num_correct += 1

                            f.write(
                                f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                            f.flush()

                            time.sleep(0.5)
                            clear_screen()

                            key_to_copy = prompt
                            if key_to_copy in card_set:
                                correct_answers[key_to_copy] = card_set[key_to_copy]
                        else:
                            print(f"{Color.Yellow}Not overridden.{
                                Color.Reset}")
                            # mark as incorrect
                            f.write(
                                f"✗ {prompt.ljust(max_left_length)} {answer}\n")
                            f.flush()

                            time.sleep(0.5)
                            clear_screen()

            # now delete all the cards that the user got right
            keys_to_remove = []

            # Iterate over the keys and values of the new dictionary
            for key, value in correct_answers.items():
                # check if the key exists in the original dictionary
                if key in card_set:
                    # if it does, add that key to keys_to_remove list
                    keys_to_remove.append(key)

            # Remove keys from original_dict
            for key in keys_to_remove:
                card_set.pop(key)

            # a new line will separate each round to the user
            print("\n")

            # replace this with the round summary
            # if the last round has passed, do the session summary
            # print(f"END OF ROUND {round_num}")

            print(f"Round {round_num} summary:")
            print_round_summary("results.txt", f"Round {
                                round_num}:", num_correct, num_answered)

    print("Session summary:")
    # with open("results.txt", "r") as f:
    #     for line in f:
    #         print(line)

    with open("results.txt", 'r') as f:
        for line in f:
            # print the line without leading/trailing whitespaces
            if '✓' in line:  # check for tick
                print("\x1b[32m" + line.strip() +
                      "\x1b[0m")  # print in green
            elif '✗' in line:  # check for cross
                print("\x1b[31m" + line.strip() +
                      "\x1b[0m")  # print in red
            else:
                print(line.strip())  # otherwise don't colour the line

# separate cards into groups of 10
# order is random within each group
# order of groups is in order
# make it so if the user supplies an empty string as an answer, make them copy out the answer
# if the user gets it wrong with a non-empty answer, allow them to override the game and mark as correct anyway
# must remove answers made up of only spaces


def render_cards(filepath: str) -> dict:
    rendered_cards = {}

    with open(filepath, "r") as f:
        for line in f:
            key, value = line.strip().split("|")
            rendered_cards[key.strip()] = value.strip()
    return rendered_cards


# main() handles command line arguments
def main():

    if len(sys.argv) != 5:
        print(
            "Command line argument order: difficulty, randomise, flip question and answer")
        return

    # order of arguments: file path, easy difficulty, randomise terms, switch question and answer
    file_path = sys.argv[1]

    difficulty = sys.argv[2]
    match difficulty:
        case "--easy":
            # good to go
            pass
        case "--normal":
            # good to go
            pass
        case "--hard":
            # good to go
            pass
        case "--very-hard":
            # good to go
            pass
        case other:
            print(
                "Error: difficulty selection can only be one of: --easy | --normal | --hard | --very-hard")
            return

    randomise = sys.argv[3]
    cards = render_cards(file_path)

    match randomise:
        case "--rand":
            # randomise
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
        case "--norand":
            # don't randomise, pass as the cards can be used as-is
            pass
        case other:
            print("Error: randomise setting can only be one of: --rand | --norand")
            return

    flip_terms = sys.argv[4]
    match flip_terms:
        case "--flip":
            # switch terms and definitions
            cards = {v: k for k, v in cards.items()}
        case "--noflip":
            # good to go, use cards as-is
            pass

    clear_screen()
    quiz(cards, difficulty)


if __name__ == '__main__':
    main()