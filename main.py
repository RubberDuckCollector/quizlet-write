import os
import sys
import time
import json
import random
import readline
import platform
from datetime import datetime
from constants import chars_to_ignore


# static analyser might say readline is unused
# but it attaches to the builtin input() func


class Color:
    Reset = "\033[0m"
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


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_round_breakdown(
    filename: str,
    target_string: str,
    num_correct: int,
    num_answered: int
):
    found = False
    with open(filename, 'r') as file:
        for line in file:
            if found:
                # print the line in green if there's a tick in it
                if '✓' in line:
                    print("\x1b[32m" + line.strip() + "\x1b[0m")
                elif '✗' in line:
                    # print the line in red if there's a cross in it
                    print("\x1b[31m" + line.strip() + "\x1b[0m")
                else:
                    # otherwise don't colour the line and print it
                    print(line.strip())
            elif target_string in line:
                found = True
                # don't print the line containing "Round <num>:"
                pass
    if not found:
        print("Target string not found in the file.")

    # print the sore the user got along with their percentage
    print(f"Score: {num_correct}/{num_answered} ({num_correct / num_answered * 100}%)")
    with open(filename, "a") as f:
        # this should never have division by 0 errors, bc cannot have a card set of 0 cards
        f.write(f"Score: {num_correct}/{num_answered} ({num_correct / num_answered * 100}%)\n\n")
        f.flush()

    print()


def make_very_hard_hint():
    return "No hints!"


def make_hard_hint(msg: str) -> str:
    hint = ""

    inside_brackets = False

    for i in range(len(msg)):
        if msg[i] in chars_to_ignore:
            # if char should be preserved when hint is being built
            hint += msg[i]
        elif msg[i] == '(':
            # if we're currently looking at a (
            # inside_brackets will be assigned True
            # add the ( to the hint
            hint += '('
            inside_brackets = True
        elif msg[i] == ')':
            # if we're at the end of the bracket
            # add the ) to the hint
            # inside_brackets becomes False
            hint += ')'
            inside_brackets = False
        elif inside_brackets is True:
            # add the character stright to the hint
            # we want to preserve the characters inside brackets
            # into the hint
            # therefore they shouldn't be an _ underscore
            hint += msg[i]
        else:
            # if we're not in brackets
            # the character is neither of ( or )
            # and the character isn't in chars_to_ignore
            # it must be turned into an _
            hint += '_'

    return hint


def make_normal_hint(msg: str) -> str:
    hint = ""
    msg = list(msg)  # turn the string into a list of chars

    i = 0
    # iterating through the list with a while loop
    # incrementing the iterating variable manually

    inside_brackets = False

    while True:
        try:
            if msg[i] in chars_to_ignore:
                hint += msg[i]
            else:
                if msg[i] == '(':
                    # if we're currently looking at a (
                    # inside_brackets will be assigned True
                    # add the ( to the hint
                    inside_brackets = True
                    hint += msg[i]
                elif msg[i] == ')':
                    # if we're at the end of the bracket
                    # add the ) to the hint
                    # inside_brackets becomes False
                    inside_brackets = False
                    hint += msg[i]
                elif inside_brackets:
                    # add the character stright to the hint
                    # we want to preserve the characters inside brackets
                    # into the hint
                    # therefore they shouldn't be an _ underscore
                    hint += msg[i]
                else:
                    # if all above conditions haven't been met,
                    # if we're not inside_brackets
                    # add the letter to the hint if i == 0,
                    # or the previous letter is a space
                    # otherwise add a '_'
                    hint += msg[i] if i == 0 or msg[i - 1].isspace() else "_"

            i += 1  # increment i, ready for the next element of the list

        except IndexError:
            # if we try to access an index that's not in the list
            # it must mean we're at the end of the list
            # and therefore built up the whole hint
            # it's safe to break out of the while True
            break

    return hint


def make_easy_hint(msg: str) -> str:
    hint = ""
    msg = list(msg)

    i = 0
    inside_brackets = False

    while True:
        try:
            if msg[i] in chars_to_ignore:
                hint += msg[i]
            else:
                if msg[i] == '(':
                    inside_brackets = True
                    hint += msg[i]  # add the open bracket to the hint
                elif inside_brackets:
                    # we want to preserve the char, and put it in the hint
                    # to give the user leniency
                    # they don't have to memorise what's in the ()
                    # they'll only have to type it out
                    hint += msg[i]
                elif msg[i] == ')':
                    inside_brackets = False
                    hint += msg[i]  # add the close bracket to the hint
                else:
                    if i == 0 or msg[i - 1].isspace():
                        hint += msg[i]  # Keep the first character of the word
                    elif msg[i - 2].isspace() or i == 1:
                        hint += msg[i]  # Keep the second character of the word
                    elif msg[i - 3].isspace() or i == 2:
                        hint += msg[i]  # Keep the third character of the word
                    else:
                        hint += "_"  # Replace other characters with underscore

            i += 1
        except IndexError:
            break

    return hint


def dump_results_to_records_file(p_start_time):
    # when the session ends, find out when that is to put it in the session's file name
    end_time = str(datetime.now())
    # this copies the data in results.txt to the records file specific to that session
    with open("results.txt", 'r') as results_f, open(f"stats/records/{p_start_time} to {end_time}.txt", 'a') as record_f:
        for line in results_f:
            record_f.write(line)


def write_terms_per_day(obj_to_be_written: str):
    file_path = "stats/terms-per-day.json"
    with open(file_path, 'w') as f:
        # comes in as a str, to turn it into a valid json obj
        # this turns any ' into ", which fixes the problem
        # to_be_written = json.dumps(obj_to_be_written)
        # f.write(to_be_written)

        json.dump(obj_to_be_written, f, indent=4)


class StreakCounter:
    def __init__(self):
        self.current_streak = 0
        self.highest_streak = 0

    def increment_streak(self):
        # increment the current streak by one
        self.current_streak += 1
        # if the current streak then exceeds the max, it must mean there's a new highest
        # therefore reassign highest_streak to current_streak
        if self.current_streak > self.highest_streak:
            self.highest_streak = self.current_streak

    def reset_streak(self):
        self.current_streak = 0

    # might not use these two that much
    def get_current_streak(self):
        return self.current_streak

    def get_highest_streak(self):
        return self.highest_streak


def quiz(card_set: dict, difficulty: str, sys_args: list):

    # when the session starts, find out when that is so it can be added to the session's file name
    start_time = str(datetime.now())

    correct_answers = {}
    round_num = 0

    # find the length of the longest term on the left
    max_left_length = max(len(left) for left in card_set.keys())

    quiz_counter = StreakCounter()

    # calculate the distance to the next tab stop
    # tab_stop = 8
    # tab_distance = tab_stop - (max_left_length % tab_stop)

    # print the aligned terms
    # for left, right in card_set.items():
    #     print(left.ljust(max_left_length),
    #           right.rjust(len(right) + tab_distance))

    NUM_TERMS = len(card_set)  # is only different between card sets of differing lengths

    """THIS WILL BE LATER REFERENCED WHEN THE WHOLE SESSION FINISHES"""

    with open("stats/terms-per-day.json", 'r') as f:
        # terms_done_dict = json.loads(f.readline())
        terms_done_dict = json.load(f)

    # show the user the previous terms done today
    # and the new terms done today figure after the end of the session
    new_terms_completed = 0

    # at the end of the round, update the current day's terms done total
    today = datetime.today().strftime('%Y-%m-%d')
    if today in terms_done_dict:
        # need to look at the int stored at the date key, then add NUM_TERMS to it
        terms_done_dict[today] += NUM_TERMS
        new_terms_completed = terms_done_dict[today]
    else:
        # not in there, can safely write new day
        terms_done_dict[today] = NUM_TERMS

        # fixes the bug where new_terms_completed is negative on a day with 0 previously completed terms
        new_terms_completed += NUM_TERMS

    THEORETICAL_MAX_STREAK = NUM_TERMS

    with open("results.txt", "a") as f:
        f.write(f"cards from: {sys.argv[1]}\n")
        while len(card_set) != 0:
            round_num += 1

            # num_correct and num_answered are for % of correct answers
            num_correct = 0
            num_answered = 0
            num_incorrect = 0
            num_remaining = len(card_set)
            # NUM_TERMS = len(card_set)  # is only different between card sets of differing lengths

            f.write(f"Round {round_num}:\n")
            f.flush()

            # declaring hint to maintain the scope
            hint = ""

            for prompt, answer in card_set.items():

                match difficulty:
                    case "-easy":
                        hint = make_easy_hint(answer)
                    case "-normal":
                        hint = make_normal_hint(answer)
                    case "-hard":
                        hint = make_hard_hint(answer)
                    case "-very-hard":
                        hint = make_very_hard_hint()
                    case _:
                        print("Error while trying to make hint")

                # print(i) -> print the first side of the card
                # print(prompt) -> print the first side of the card
                # print(card_set[i]) -> print the answer/other side of the card
                # print(answer) -> print the answer/other side of the card
                # print(hint) -> print the hint for the answer

                current_percent_correct = round((num_correct / num_answered), 2) * 100 if num_answered > 0 else 0.0

                # this is the percentage completed in the current set
                progress = round(num_answered / NUM_TERMS, 2) * 100 if num_answered > 0 else 0.0

                print(f"Working from file {Color.Dim}{os.path.basename(sys_args[1])}{Color.Reset}")
                print(f"Remaining: {num_remaining}")
                print(f"Correct: {Color.Green}{num_correct}{Color.Reset} ({current_percent_correct}%)")
                print(f"Incorrect: {Color.Red}{num_incorrect}{Color.Reset}")
                print(f"Progress: {Color.LightBlue}{progress}{Color.Reset}%")
                print(f"Streak: {Color.LightMagenta}{quiz_counter.get_current_streak()}{Color.Reset} ({Color.LightMagenta}{quiz_counter.get_highest_streak()}{Color.Reset})")
                # print(f"DEBUG: THEORETICAL_MAX_STREAK: {THEORETICAL_MAX_STREAK}")
                print(f"What's the answer to '{Color.Bold}{prompt}{Color.Reset}'?")
                print(f"Hint: {Color.Dim}{hint}{Color.Reset}")
                user_response = input("> ").strip()

                # print num_remaining, num_correct, num_incorrect
                # print(f"Remaining: {num_remaining}\nCorrect: {num_correct}\nIncorrect: {num_incorrect}")

                # if the user input is falsy
                # i.e there were only spaces and strip() has removed them
                # to leave an empty string
                if not user_response:
                    print("Don't know? Copy out the answer so you remember it!")
                    quiz_counter.reset_streak()
                    while True:
                        user_response = input(f"Copy the answer below ↓\n- {answer}\n> ")
                        if user_response.lower() == answer.lower():
                            print(f"{Color.Cyan}Next question.{Color.Reset}")
                            time.sleep(0.5)
                            clear_screen()
                            break
                        else:
                            print("Try again.")
                    # mark as incorrect as the user doesn't know the answer
                    f.write(f"✗ {prompt.ljust(max_left_length)} {answer}\n")
                    f.flush()  # essential to prevent a file error

                    num_incorrect += 1

                else:
                    # the user gets a special message if capitalisation matches perfectly
                    if user_response == answer:
                        print(f"{Color.Green}Correct. Well done!{Color.Reset}")

                        quiz_counter.increment_streak()
                        num_correct += 1

                        time.sleep(0.5)
                        clear_screen()

                        f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                        f.flush()

                        key_to_copy = prompt
                        if key_to_copy in card_set:
                            correct_answers[key_to_copy] = card_set[key_to_copy]

                    # otherwise just a normal message
                    elif user_response.lower() == answer.lower():
                        print(f"{Color.Green}Correct{Color.Reset}")

                        quiz_counter.increment_streak()
                        num_correct += 1

                        time.sleep(0.5)
                        clear_screen()

                        f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                        f.flush()

                        key_to_copy = prompt
                        if key_to_copy in card_set:
                            correct_answers[key_to_copy] = card_set[key_to_copy]

                    else:
                        # ask for override
                        print(f"{Color.Red}Incorrect.{Color.Reset} Answer: {Color.LightYellow}{answer}{Color.Reset}")

                        override = input("Override as correct? (empty answer = don't override) ")

                        # if override has something in it
                        if override:
                            # mark as correct as the user wishes
                            print(f"Overridden as {Color.Green}Correct{Color.Reset}.")

                            quiz_counter.increment_streak()
                            num_correct += 1

                            f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                            f.flush()

                            time.sleep(0.5)
                            clear_screen()

                            key_to_copy = prompt
                            if key_to_copy in card_set:
                                correct_answers[key_to_copy] = card_set[key_to_copy]
                        else:
                            print(f"{Color.Yellow}Not overridden.{Color.Reset}")
                            # mark as incorrect
                            f.write(f"✗ {prompt.ljust(max_left_length)} {answer}\n")
                            f.flush()

                            quiz_counter.reset_streak()
                            num_incorrect += 1

                            time.sleep(0.5)
                            clear_screen()
                num_answered += 1
                num_remaining -= 1

            # now delete all the cards that the user got right
            # this is to make sure only the things they got wrong are left
            # meaning that on the next iteration, the dict will only have
            # terms that the user got wrong
            keys_to_remove = []

            # iterate over the keys of the new dictionary
            for key, _ in correct_answers.items():
                # check if the key exists in the original dictionary
                if key in card_set:
                    # if it does, add that key to keys_to_remove list
                    keys_to_remove.append(key)

            # remove keys from original_dict
            for key in keys_to_remove:
                card_set.pop(key)

            # a new line will separate each round to the user
            print("\n")

            # replace this with the round breakdown
            # if the last round has passed, do the session breakdown
            # print(f"END OF ROUND {round_num}")

            print(f"Round {round_num} breakdown:")

            # here the proc will look for the line in the file containing "Round"
            # and the number of the current round with a : right after it
            print_round_breakdown("results.txt", f"Round {round_num}:", num_correct, num_answered)
            
            # randomise now if rand flag is set to --rand-every-round
            if sys_args[3] == "--rand-every-round":
                items = list(card_set.items())
                random.shuffle(items)
                card_set = dict(items)
            else:
                pass


        # write the round list to results.txt
        f.write(f"No. terms in the card set = {NUM_TERMS}\n")
        f.write(f"highest_streak = {quiz_counter.get_highest_streak()}\n")
        f.write(f"perfect_streak = {quiz_counter.get_highest_streak() == THEORETICAL_MAX_STREAK}")  # this should resolve to True or False

    dump_results_to_records_file(start_time)

    # after the record file is done, print the session breakdown to the user

    print(f"{Color.Bold}Session breakdown:{Color.Reset}")

    with open("results.txt", 'r') as f:
        for line in f:
            # print the line without leading/trailing whitespaces
            if '✓' in line:  # check for tick
                print("\x1b[32m" + line.strip() + "\x1b[0m")  # print in green
            elif '✗' in line:  # check for cross
                print("\x1b[31m" + line.strip() + "\x1b[0m")  # print in red
            else:
                print(line.strip())  # otherwise don't colour the line


    write_terms_per_day(terms_done_dict)

    # show the user the increase in terms done today
    print(f"Terms done today: {new_terms_completed - NUM_TERMS} {Color.LightGreen}->{Color.Reset} {new_terms_completed}")


def render_cards(filepath: str) -> dict:
    rendered_cards = {}

    with open(filepath, "r") as f:
        for line in f:
            key, value = line.strip().split("|")
            rendered_cards[key.strip()] = value.strip()

    # return this as the dictionary of terms and definitions
    # e.g: "hello": "hola",
    # the key is on the left, its corresponding value is on the right
    return rendered_cards


# main() handles command line arguments
# needed for value checking and presence checking of the command line args
def main():

    if len(sys.argv) != 5:
        print("Command line argument order: card set, difficulty, randomise, flip question and answer")
        return

    # order of arguments:
    # file path to file containing questions,
    # easy difficulty,
    # randomise terms,
    # switch question and answer

    file_path = sys.argv[1]

    difficulty = sys.argv[2]

    valid_difficulties = {"-easy", "-normal", "-hard", "-very-hard"}

    if difficulty in valid_difficulties:
        pass
    else:
        print("Error: difficulty selection can only be one of: -easy | -normal | -hard | -very-hard")
        return

    randomise = sys.argv[3]
    cards = render_cards(file_path)

    # will be handled in quiz()
    match randomise:
        case "-rand-once":
            # randomise only at the start of the session
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
        case "-rand-every-round":
            # randomise after the end of every round 
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
            pass
        case "-no-rand":
            # don't randomise, pass as the cards can be used as-is
            pass
        case _:
            print("Error: randomise setting can only be one of: -rand-once | -no-rand | -rand-every-round")
            return

    flip_terms = sys.argv[4]
    match flip_terms:
        case "-flip":
            # switch terms and definitions
            cards = {v: k for k, v in cards.items()}
        case "-no-flip":
            # good to go, use cards as-is
            pass
        case _:
            print("Error: flip setting can only be one of: -flip | -no-flip")
            return

    # prepare results.txt by wiping it
    # the file contents of the previous session will remain in the file,
    # if program aborted with an uncaught error
    # e.g KeyboardInterrupt or KeyError
    with open("results.txt", "w") as f:
        f.write("")

    clear_screen()
    quiz(cards, difficulty, sys.argv)


if __name__ == '__main__':
    main()
