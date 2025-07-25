print("Loading...")
import progressbar
bar = progressbar.ProgressBar(maxval=11, term_width=40)
bar.start()
# external library code
import os
bar.update(1)
import sys
bar.update(1)
import time
bar.update(1)
import json
bar.update(1)
import random
bar.update(1)
import pathlib
bar.update(1)
import argparse
bar.update(1)
import readline
bar.update(1)
# import platform
from datetime import datetime
bar.update(1)
# print("importing matplotlib (the biggest library)")
import matplotlib.pyplot as plt  # type: ignore
bar.update(1)
# my own library code below
import my_modules
bar.update(1)
bar.finish()


"""
IMPORT GUIDE (examples of how you would use my library code)

`my_modules.constants` refers to `my_modules/constants.py`
`my_modules.help` refers to `my_modules/help.py`
`my_modules.color` refers to `my_modules/color.py`

`my_modules.constants.chars_to_ignore[i]`  # access the value at index `i` in the chars_to_ignore list
`my_modules.color.Color.Blue(/Magenta/Bold/Reset)`  # access the specific color from the Color class

Example:
`my_modules.help.help_command()`  # call the help_command() procedure
To explain it in a sentence (2 ways):
1. "call the help command from the file `help`, which is in the folder/directory `my_modules`."
2. "go to the folder/directory `my_modules`, go to the file `help`, call the help command."
"""


# static analyser might say readline is unused
# but it attaches to the builtin input() func


"""
CONVENTIONS:

a variable starting with `p_...` denotes a parameter, not a pointer
"term" or "question" refers to just the question on the flash card.
    - "definition" or "answer" refers to the answer on the flash card
    - "term" and "question" are interchangeable
    - "definition" and "answer" are interchangeable.
A "session" is one completion of all the flash cards from a file.
    A completed session means you've answered all the cards correctly once.

File paths in help text are written in Light Magenta
Commands in help text are written in Cyan
"""


def initialize_stats():
    if not os.path.exists("stats/lifetime_stats.json"):
        initial_data = {
            "initialized": True,
            "lifetime_correct_answers": 0,
            "lifetime_incorrect_answers": 0,
            "sessions_per_day": {},
            "cards_per_day": {}
        }
        with open("stats/lifetime_stats.json", "w") as f:
             json.dump(initial_data, f, indent=4)


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
                    print(f"{my_modules.color.Color.Green}{line.strip()}{my_modules.color.Color.Reset}")
                elif '✗' in line:
                    # print the line in red if there's a cross in it
                    print(f"{my_modules.color.Color.Red}{line.strip()}{my_modules.color.Color.Reset}")
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


def dump_results_to_records_file(p_start_time, p_this_sessions_temp_results_file: str) -> str:
    # when the session ends, find out when that is to put it in the session's file name
    end_time = str(datetime.now())
    # this copies the data in this_sessions_temp_results_file to the records file for that session
    session_dir = f"stats/records/Session {p_start_time} to {end_time}"
    os.mkdir(session_dir)
    with open(p_this_sessions_temp_results_file, 'r') as results_f, open(f"{session_dir}/session.txt", 'a') as record_f:
        for line in results_f:
            record_f.write(line)
    
    return session_dir


class StreakCounter:
    def __init__(self):
        self.current_streak = 0
        self.highest_streak = 0

    def increment_streak(self):
        # increment the current streak by one
        self.current_streak += 1
        # if the current streak then exceeds the current highest, it must mean there's a new highest
        # therefore reassign highest_streak to current_streak
        if self.current_streak > self.highest_streak:
            self.highest_streak = self.current_streak

    def decrement_streak(self):
        if self.current_streak < 0:
            self.current_streak = 0
        elif self.current_streak == 0:
            pass
        else:
            self.current_streak -= 1

    def reset_streak(self):
        self.current_streak = 0

    # might not use these 4 that much

    def set_current_streak(self, p_current_streak):
        self.current_streak = p_current_streak

    def set_highest_streak(self, p_highest_streak):
        self.highest_streak = p_highest_streak

    def get_current_streak(self):
        return self.current_streak

    def get_highest_streak(self):
        return self.highest_streak


def quiz(card_set: dict, p_args, p_start_time: str):

    correct_answers = {}
    round_num = 0

    # find the length of the longest term on the left
    max_left_length = max(len(left) for left in card_set.keys())

    quiz_counter = StreakCounter()

    # calculate the distance to the next tab stop
    # tab_stop = 8
    # tab_distance = tab_stop - (max_left_length % tab_stop)

    # print the aligned cards
    # for left, right in card_set.items():
    #     print(left.ljust(max_left_length),
    #           right.rjust(len(right) + tab_distance))

    NUM_TERMS = len(card_set)  # is only different between card sets of differing lengths

    x_axes = []  # cards completed
    y_axes = []  # % correct

    THEORETICAL_MAX_STREAK = NUM_TERMS

    # each session will have a temporary results file. this allows more than one instance of
    # the program to be running at a time, because in the old model with only one results file,
    # if the user created a new session while an old one was happening, `results.txt` would be
    # overwritten with data from the new session, which removes data integrity from my records system.
    # this is passed to `quiz()` as a parameter with the type str.
    # it's deleted at the end of the session as it's only job is to temporarily store data until
    # the user completes the session. this is how i've implemented atomicity.
    # either the user completes the whole flash card set, and i write their results to a file,
    # or they don't complete it and nothing gets written. this is my methodolgy because it's very clear-cut and simple in my eyes

    # i chose to format the temp results files this way using date and time
    # as it's the most reliable way to not have a clash if sessions start close to each other
    # e.g: if you spam create sessions, they probably won't fall on the same exact time
    # because datetime keeps time accuracy up to 6 decimal places

    #TODO: implement saving feature
    # create a temp dir for each session with temp results
    # when the program detects a KeyboardInterrupt ask if the user wants to save the session
    # the dir will not be deleted
    # the user can specify a --resume command line argument
    # the user is put into an interactive mode (blessed library?)
    # resume the flash card revision from where the user left off
    # start_time = datetime.now()
    # TODO: find out how to save the exact cards answered correctly and incorrectly and remaining cards
        # pass those as parameters in `quiz()`
        # pass start time as a parameter
        # also need to keep track of the session data when saving and resuming a session
    # `correct_answers` dict may help
    # `card_set` (parameter) may help
        # -rand-every-round is present
    this_sessions_temp_dir_name = f"temp/temp_dir_for_session_{p_start_time}"
    os.mkdir(this_sessions_temp_dir_name)
    this_sessions_temp_results_file = f"{this_sessions_temp_dir_name}/temp_results_for_session_{p_start_time}.txt"
    
    test_indicator = ""
    if p_args.test:
        test_indicator = " TEST MODE - NO STATS SAVED"

    # user interaction will start in this try block
    # it's here to catch a keyboard interrupt such as ctrl-c
    # if it catches one, this_sessions_temp_results_file will still be deleted, which is good
    # because it's a temp file and all actions are aborted if the session finishes early
    try:
        with open(this_sessions_temp_results_file, "a") as f:
            f.write(f"cards from: {sys.argv[1]}\n")

            # used to add to lifetime stats
            total_correct_in_session = 0
            total_incorrect_in_session = 0

            while len(card_set) != 0:
                round_num += 1

                # num_correct and num_answered are for % of correct answers
                num_correct = 0
                num_answered = 0
                num_incorrect = 0
                num_remaining = len(card_set)

                this_rounds_x_axis = []
                this_rounds_y_axis = []


                f.write(f"Round {round_num}:\n")
                f.flush()

                # declaring hint to maintain the scope
                hint = ""

                for prompt, answer in card_set.items():

                    if p_args.difficulty == my_modules.hint_system.VALID_DIFFICULTIES[0]:
                        hint = my_modules.hint_system.make_easy_hint(answer)
                    elif p_args.difficulty == my_modules.hint_system.VALID_DIFFICULTIES[1]:
                        hint = my_modules.hint_system.make_normal_hint(answer)
                    elif p_args.difficulty == my_modules.hint_system.VALID_DIFFICULTIES[2]:
                        hint = my_modules.hint_system.make_hard_hint(answer)
                    elif p_args.difficulty == my_modules.hint_system.VALID_DIFFICULTIES[3]:
                        hint = my_modules.hint_system.make_very_hard_hint()

                    # match difficulty:
                    #     case "-easy":
                    #         hint = my_modules.hint_system.make_easy_hint(answer)
                    #     case "-normal":
                    #         hint = my_modules.hint_system.make_normal_hint(answer)
                    #     case "-hard":
                    #         hint = my_modules.hint_system.make_hard_hint(answer)
                    #     case "-very-hard":
                    #         hint = my_modules.hint_system.make_very_hard_hint()
                    #     case _:
                    #         print("Error while trying to make hint")

                    # print(i) -> print the first side of the card
                    # print(prompt) -> print the first side of the card
                    # print(card_set[i]) -> print the answer/other side of the card
                    # print(answer) -> print the answer/other side of the card
                    # print(hint) -> print the hint for the answer

                    current_percent_correct = round((num_correct / num_answered), 2) * 100 if num_answered > 0 else 0.0

                    # this is the percentage completed in the current set
                    progress = round(num_answered / NUM_TERMS * 100, 2) if num_answered > 0 else 0.0

                    print(f"Working from file {my_modules.color.Color.Dim}{os.path.basename(p_args.flash_card_file_path)}{my_modules.color.Color.Reset}{test_indicator}")
                    print(f"Remaining: {num_remaining}")
                    print(f"Correct: {my_modules.color.Color.Green}{num_correct}{my_modules.color.Color.Reset} ({current_percent_correct}%)")
                    print(f"Incorrect: {my_modules.color.Color.Red}{num_incorrect}{my_modules.color.Color.Reset}")
                    print(f"Progress: {my_modules.color.Color.LightBlue}{progress}{my_modules.color.Color.Reset}%")
                    print(f"Streak: {my_modules.color.Color.LightMagenta}{quiz_counter.get_current_streak()}{my_modules.color.Color.Reset} ({my_modules.color.Color.LightMagenta}{quiz_counter.get_highest_streak()}{my_modules.color.Color.Reset})")
                    # print(f"DEBUG: THEORETICAL_MAX_STREAK: {THEORETICAL_MAX_STREAK}")
                    # print(f"DEBUG: sys_args: {sys_args}")
                    print(f"What's the answer to {my_modules.color.Color.LightCyan}{prompt}{my_modules.color.Color.Reset}?")
                    print(f"Hint: {my_modules.color.Color.Dim}{hint}{my_modules.color.Color.Reset}\n> ", end='')
                    # user_response = sys.stdin.readline().strip()
                    # user_response = input("> ").strip()  # OUTDATED
                    user_response = input().strip()

                    # print num_remaining, num_correct, num_incorrect
                    # print(f"Remaining: {num_remaining}\nCorrect: {num_correct}\nIncorrect: {num_incorrect}")

                    # if the user input is falsy
                    # i.e there were only spaces and strip() has removed them to leave an empty string
                    if not user_response:
                        print("Don't know? Copy out the answer so you remember it!")
                        quiz_counter.reset_streak()
                        while True:
                            print(f"Copy the answer below ↓\n- {answer}\n> ", end='')
                            # user_response = sys.stdin.readline().strip()
                            user_response = input().strip()
                            if user_response.lower() == answer.lower():
                                print(f"{my_modules.color.Color.Cyan}Next question.{my_modules.color.Color.Reset}")
                                time.sleep(0.5)
                                my_modules.clear_screen.clear_screen()
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
                            print(f"{my_modules.color.Color.Green}Correct. Well done!{my_modules.color.Color.Reset}")

                            quiz_counter.increment_streak()
                            num_correct += 1

                            time.sleep(0.5)
                            my_modules.clear_screen.clear_screen()

                            f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                            f.flush()

                            key_to_copy = prompt
                            if key_to_copy in card_set:
                                correct_answers[key_to_copy] = card_set[key_to_copy]


                        # otherwise just a normal message
                        elif user_response.lower() == answer.lower():
                            print(f"{my_modules.color.Color.Green}Correct{my_modules.color.Color.Reset}")

                            quiz_counter.increment_streak()
                            num_correct += 1

                            time.sleep(0.5)
                            my_modules.clear_screen.clear_screen()

                            f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                            f.flush()

                            key_to_copy = prompt
                            if key_to_copy in card_set:
                                correct_answers[key_to_copy] = card_set[key_to_copy]

                        else:
                            # ask for override
                            print(f"{my_modules.color.Color.Red}Incorrect.{my_modules.color.Color.Reset} Answer: {my_modules.color.Color.LightYellow}{answer}{my_modules.color.Color.Reset}")

                            override = input("Override as correct? (empty answer = don't override) ")

                            # if override has something in it
                            if override:
                                # mark as correct as the user wishes
                                print(f"Overridden as {my_modules.color.Color.Green}Correct{my_modules.color.Color.Reset}.")

                                quiz_counter.increment_streak()
                                num_correct += 1

                                f.write(f"✓ {prompt.ljust(max_left_length)} {answer}\n")
                                f.flush()

                                time.sleep(0.5)
                                my_modules.clear_screen.clear_screen()

                                key_to_copy = prompt
                                if key_to_copy in card_set:
                                    correct_answers[key_to_copy] = card_set[key_to_copy]
                            else:
                                print(f"{my_modules.color.Color.Yellow}Not overridden.{my_modules.color.Color.Reset}")
                                # mark as incorrect
                                f.write(f"✗ {prompt.ljust(max_left_length)} {answer}\n")
                                f.flush()

                                quiz_counter.reset_streak()
                                num_incorrect += 1

                                time.sleep(0.5)
                                my_modules.clear_screen.clear_screen()

                    # if this is the first question answered,
                    # need to plot % on the graph early before
                    # num_answered and num_remaining are incremented
                    # because otherwise it would plot 0% at question 1
                    if num_answered == 0: 
                        current_percent_correct = round((num_correct / num_answered), 2) * 100 if num_answered > 0 else 0.0
                        # this is for adding data to the graph
                        this_rounds_x_axis.append(num_answered)
                        this_rounds_y_axis.append(current_percent_correct)

                    num_answered += 1
                    num_remaining -= 1

                    current_percent_correct = round((num_correct / num_answered), 2) * 100 if num_answered > 0 else 0.0
                    # this is for adding data to the graph
                    this_rounds_x_axis.append(num_answered)
                    this_rounds_y_axis.append(current_percent_correct)

                # now delete all the cards that the user got right
                # this is to make sure only the things they got wrong are left
                # meaning that on the next iteration, the dict will only have
                # cards that the user got wrong
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
                print_round_breakdown(this_sessions_temp_results_file, f"Round {round_num}:", num_correct, num_answered)
                
                # randomize now if rand flag is set to --rand-every-round
                if p_args.randomize == "-rand-every-round":
                    items = list(card_set.items())
                    random.shuffle(items)
                    card_set = dict(items)
                else:
                    pass

                # this ensures that the null response isn't plotted
                # which would skew the results of the data set and make the graph less readable
                this_rounds_x_axis.pop(0)
                this_rounds_y_axis.pop(0)

                x_axes.append(this_rounds_x_axis)
                y_axes.append(this_rounds_y_axis)

                this_rounds_x_axis = []
                this_rounds_y_axis = []

                total_correct_in_session += num_correct
                total_incorrect_in_session += num_incorrect

            # write the round list to this_sessions_temp_results_file
            f.write(f"{p_args.difficulty}\n")
            f.write(f"{p_args.randomize}\n")
            f.write(f"{p_args.flip_cards}\n")
            f.write(f"No. cards in the card set = {NUM_TERMS}\n")
            f.write(f"highest_streak = {quiz_counter.get_highest_streak()}\n")
            f.write(f"perfect_streak = {quiz_counter.get_highest_streak() == THEORETICAL_MAX_STREAK}\n")  # this should resolve to True or False
            f.write("If you want to compute this data and you're not in test mode, there will be a session.json file in the session's folder.")

        session_data = {
            "file_path_to_cards": sys.argv[1],
            "difficulty": p_args.difficulty,
            "randomize": p_args.randomize,
            "flip": p_args.flip_cards,
            "num_cards_in_set": str(NUM_TERMS),
            "highest_streak": str(quiz_counter.get_highest_streak()),
            "is_perfect_streak": str(quiz_counter.get_highest_streak() == THEORETICAL_MAX_STREAK)
        }


        new_sessions_completed = 0
        new_cards_completed = 0

        if not p_args.test:
            this_sessions_dir = dump_results_to_records_file(p_start_time, this_sessions_temp_results_file)
            width_per_label = 0.3

            # finds the smallest and biggest numbers in `y_axes`
            min_each_round = min([min(i) for i in y_axes])
            max_each_round = max([max(i) for i in y_axes])


            # defining the x ticks i need here so i can use the variable to set `plt.xticks()`
            # and also calculate the graph's width based on the number of ticks, hence `len(my_x_ticks)` ...
            # ... (which are 2 different things)
            my_x_ticks = [i for i in range(1, NUM_TERMS + 1)]
            
            # Calculate the figure width based on the number of x-axis labels
            fig_width = max(8, width_per_label * len(my_x_ticks))  # Ensure minimum width

            # fig_height = width_per_label * 101  # 0.3 width per label multiplied by 101 y ticks from 0-100 inclusive

            # sets the height of the figure according to the range of percentages achieved by the user.
            fig_height = width_per_label * (max_each_round - min_each_round + 1)  

            # Set up figure with calculated width
            plt.figure(figsize=(fig_width, fig_height))


            # the graph is plotted and saved here at the end of the session to maintain the atomicity of the program.
            # either the session is completed in its entirity, or everything is aborted and it's like nothing happened at all

            # plot each y-axis data series with its corresponding x-axis values
            my_modules.plotting.plotting_graph()
            for i, (x_data, y_data) in enumerate(zip(x_axes, y_axes)):
                plt.plot(x_data, y_data, label=f'Round {i + 1}', marker='o')  # i think the dots make it more readable across a larger graph

            plt.grid(color = 'grey', linestyle = '-', linewidth = 0.3)

            # plt.plot(x_axes, y_axes)
            plt.title(f"Consistency line graph for session starting at {p_start_time}\nPath to cards: {sys.argv[1]}")
            plt.xlabel("# Cards answered")
            plt.ylabel("% Accuracy")
            # plt.ylim(0, 100)  # y axis goes from 0 to 100
            if min_each_round == max_each_round:
                min_each_round -= 2
            plt.ylim(min_each_round, max_each_round)  # y axis graduates from min percentage achieved to highest percentage achieved
            plt.legend(loc="upper left")  # force the key to appear on the graph, "best" means that matplotlib will put it in the least obtrusive area using its own judgement
            plt.xticks([i for i in range(1, NUM_TERMS + 1, 2)])
            # plt.yticks([i for i in range(0, 101, 1)])  # full y axis
            plt.yticks(range(int(min_each_round), int(max_each_round) + 2, 2))  # only the relevant parts of the graph
            plt.gca().xaxis.set_ticks_position('both')  # puts the x and y axes on the right and top of the graphs, increases readablilty for long graphs
            plt.gca().tick_params(axis='x', labeltop=True, rotation=90)  # enable x axis numbers on the right side of the graph as well as the left, also rotates those numbers by 90 degrees to make them readable
            plt.gca().yaxis.set_ticks_position('both')
            plt.gca().tick_params(axis='y', labelright=True)  # enable y axis numbers on the top of the graph as well as the bottom
            my_modules.plotting.saving_graph()
            # bbox_inches = "tight" removes the bug of the title going offscreen if it's too long
            # https://stackoverflow.com/a/59372013
            plt.savefig(f"{this_sessions_dir}/line-graph.pdf", bbox_inches = "tight")


            # after the record file is done, print the session breakdown to the user

            print(f"{my_modules.color.Color.Bold}Session breakdown:{my_modules.color.Color.Reset}")

            with open(this_sessions_temp_results_file, 'r') as f:
                for line in f:
                    # print the line without leading/trailing whitespaces
                    if '✓' in line:  # check for tick
                        print(f"{my_modules.color.Color.Green}{line.strip()}{my_modules.color.Color.Reset}")
                    elif '✗' in line:  # check for cross
                        print(f"{my_modules.color.Color.Red}{line.strip()}{my_modules.color.Color.Reset}")
                    else:
                        print(line.strip())  # otherwise don't colour the line
            try:  # START OF STATS COLLECTION
                # putting this code here instead of at the top of `quiz()` fixes the bug,
                # where only one session would add to the cards done count for that day
                # instead of a second session
                # disclaimer: bug only found with two concurrent sessions

                # write the x axis data and the y axis data to special files in `this_sessions_dir`
                # this allows the graph to be reproduced
                with open(f"{this_sessions_dir}/x-axis-data.txt", "w") as f:
                    f.write(f"{x_axes}")

                with open(f"{this_sessions_dir}/y-axis-data.txt", "w") as f:
                    f.write(f"{y_axes}")

                with open(f"{this_sessions_dir}/session.json", "w") as f:
                    json.dump(session_data, f, indent=4)

                lifetime_stats_file_path = "stats/lifetime_stats.json"
                with open(lifetime_stats_file_path, 'r') as lifetime_f:
                    data = json.load(lifetime_f)

                # FUNCTIONALITY FOR THE USER:
                # show the user the previous cards done today
                # and the new cards done today figure after the end of the session

                # at the end of the round, update the current day's cards done total
                today = datetime.today().strftime('%Y-%m-%d')
                if today in data["cards_per_day"]:
                    # need to look at the int stored at the date key inside the `cards_per_day` field, then add NUM_TERMS to it
                    data["cards_per_day"][today] += NUM_TERMS
                    new_cards_completed = data["cards_per_day"][today]
                else:
                    # not in there, can safely write the new day into the data
                    data["cards_per_day"][today] = NUM_TERMS

                    # fixes the bug where new_cards_completed is negative on a day with 0 previously completed cards
                    new_cards_completed += NUM_TERMS

                # show the user the increase in cards done today
                print(f"Cards done today: {new_cards_completed - NUM_TERMS} {my_modules.color.Color.LightGreen}->{my_modules.color.Color.Reset} {new_cards_completed}")

                # current date and time not assigned again so we can have the same date for both the session and the cards count
                # i.e date cannot progress in between that code and this code and have an effect on the code's function, this makes the program's inner workings more simple and straight forward for the user and the developer

                # sessions that end on a particular day will contribute to the cards and sessions done per day counts
                if today in data["sessions_per_day"]:
                    data["sessions_per_day"][today] += 1
                    new_sessions_completed = data["sessions_per_day"][today]
                else:
                    # not in there, can safely write new day
                    data["sessions_per_day"][today] = 1

                    # fixes the bug where new_sessions_completed is negative on a day with 0 previously completed sessions
                    new_sessions_completed += 1

                # WILL DELETE IF CHANGES AFTER d930c92 WORK
                # write_sessions_per_day(data["sessions_per_day"])

                # show the user the increase in sessions done today
                print(f"Sessions done today: {new_sessions_completed - 1} {my_modules.color.Color.LightGreen}->{my_modules.color.Color.Reset} {new_sessions_completed}")

                # update lifetime correct and incorrect answers
                lifetime_correct_before_change = data["lifetime_correct_answers"]
                lifetime_incorrect_before_change = data["lifetime_incorrect_answers"]

                data["lifetime_correct_answers"] += total_correct_in_session
                data["lifetime_incorrect_answers"] += total_incorrect_in_session

                print(f"Lifetime correct answers: {lifetime_correct_before_change} -> {data["lifetime_correct_answers"]}")
                print(f"Lifetime incorrect answers: {lifetime_incorrect_before_change} -> {data["lifetime_incorrect_answers"]}")

                # write all the changed data back to the lifetime stats file
                with open(lifetime_stats_file_path, "w") as lifetime_f:
                    json.dump(data, lifetime_f, indent=4)

            except Exception as e:
                print("Error while saving data.")
                print(e)
        # delete the temp file as it has served its purpose
        os.remove(this_sessions_temp_results_file)
        os.rmdir(this_sessions_temp_dir_name)

    except (KeyboardInterrupt, EOFError, Exception) as e:
        # if the user stops the program with ctrl c or ctrl d, also delete the file
        # to make it like nothing ever happened
        # print("An error has occurred.")
        print(e)
        os.remove(this_sessions_temp_results_file)
        os.rmdir(this_sessions_temp_dir_name)


def render_cards(file_path: str) -> dict:
    rendered_cards = {}

    if my_modules.validate.validate_file(file_path):
        with open(file_path, "r") as f:
            for line in f:
                if line.strip() == "" or line[0] == "#":
                    pass
                else:
                    key, value = line.strip().split("|")
                    rendered_cards[key.strip()] = value.strip()

        # return this as the dictionary of terms and definitions
        # e.g: "hello": "hola",
        # the key is on the left, its corresponding value is on the right
        return rendered_cards  # this is a dict
    else:
        raise ValueError("Cards are not correctly formatted. See above message to fix.")


# main() handles command line arguments
# needed for value checking and presence checking of the command line args
def main():

    initialize_stats()

    # order of arguments:
    # help/main.py/bar-chart
    # file path to file containing questions,
    # difficulty,
    # randomize cards,
    # switch question and answer

    parser = argparse.ArgumentParser(prog="main.py",
                                     description="Quizlet Write my version <https://github.com/RubberDuckCollector/quizlet-write> (name may change)",
                                     epilog="Made for flash card revision. Recommended for short answers, but works with any text-based question and answer. Remember to not change the file path to the flash cards while the program is running.")
    # add optional arguments
    parser.add_argument("--explain_app_usage", action="store_true", help="Gives a walkthrough of the average user's interactions with the program")
    parser.add_argument("--technical_explanation", action="store_true", help="Gives a walkthrough of how the program works")
    # bar charts
    parser.add_argument("--make", choices=["session_bar_chart", "flash_card_bar_chart"], help="Generates a bar chart of the sessions OR flash cards done on each day")
    parser.add_argument("--test", action="store_true", help="Enabling this will make the stat collection functionality NOT work, But the program will still function as normal")
    parser.add_argument("--flip", type=pathlib.Path, help="Swaps the questions and answers in a file and outputs it in a new file")
    parser.add_argument("--sync", action="store_true", help="Collects data in PROJECT_ROOT/stats/records/ and makes overwrites that data to PROJECT_ROOT/stats/lifetime_stats.json to fix parity issues")

    """
    `nargs="?"`: makes the positional argument optional.
    usually positional arguments are required but sometimes they have to change to
    accommodate the optional arguments.
    PREVIOUS ERROR: argparse didn't let the optional arguments because it was expecting
    positional arguments before even considering optional ones.

    `default=None`: if the user doesn't provide an argument in that place, it wil default to None.
    this is used to better keep track of what's going on with the positional arguments.
    since None is different to emtpy string/0 value it gives me more immediate information about
    how the program is behaving
    """
    # add positional arguments
    # nargs="?" overrides their default behaviour and makes them optional
    # they will only be optional temporarily, and will be handled (manually) as usual later
    parser.add_argument("flash_card_file_path", nargs="?", default=None, help="This is a relative or absolute file path to a text file containing the flash cards you want to use", type=str)
    parser.add_argument("difficulty", nargs="?", default=None, help="Difficulty of the quiz", type=str)
    parser.add_argument("randomize", nargs="?", default=None, help="How you want to randomise the flash cards in the quiz", type=str)
    parser.add_argument("flip_cards", nargs="?", default=None, help="Wether or not you want to 'flip the cards over' and answer with the question", type=str)

    # if sys.argv only contains `main.py`
    # print help and halt program execution
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_intermixed_args()

    if args.explain_app_usage:
        print("explain app usage - import commands.py (write long things in there)")
        sys.exit(0)
    elif args.technical_explanation:
        print("technical explanation - commands.py")
        sys.exit(0)
    elif args.make == "session_bar_chart":
        print(my_modules.plotting.make_session_bar_chart())
        sys.exit(0)
    elif args.make == "flash_card_bar_chart":
        print(my_modules.plotting.make_flash_card_bar_chart())
        sys.exit(0)
    elif args.flip:
        print(my_modules.flip_flash_card_file.flip_flash_card_file(args.flip))
        sys.exit(0)
    elif args.sync:
        if my_modules.sync_stats.sync():  # this runs the function and evaluates its output (it has a bool output)
            print(f"Stats synced to {os.getcwd()}/stats/lifetime_stats.json successfully.")
        sys.exit(0)

    required_args = {
        'flash_card_file_path': args.flash_card_file_path,
        'difficulty': args.difficulty,
        'randomize': args.randomize,
        'flip_cards': args.flip_cards
    }

    # makes a list of all missing arguments
    # uses the fact that if they aren't present, the list comp looks for None associated with its name
    missing_required_args = [arg_name for arg_name, value in required_args.items() if value is None]

    if missing_required_args:
        parser.error(f"Missig required positional argument(s): {missing_required_args}")

    if args.difficulty in my_modules.hint_system.VALID_DIFFICULTIES:
        pass
    else:
        print("Error: difficulty selection can only be one of: easy | normal | hard | very-hard")
        return

    print("Rendering cards...")
    cards = render_cards(args.flash_card_file_path)

    # will be handled in quiz()
    match args.randomize:
        case "rand-once":
            # randomize only at the start of the session
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
        case "rand-every-round":
            # randomize after the end of every round 
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
            pass
        case "no-rand":
            # don't randomize, pass as the cards can be used as-is
            pass
        case _:
            print("Error: randomize setting can only be one of: rand-once | no-rand | rand-every-round")
            return

    match args.flip_cards:
        case "flip":
            # switch terms and definitions
            cards = {v: k for k, v in cards.items()}
            args.flip_cards = True  # change the value from a string to a bool for easier processing in session stats collection later
        case "no-flip":
            # good to go, use cards as-is
            args.flip_cards = False
            pass
        case _:
            print("Error: flip setting can only be one of: flip | no-flip")
            return

    my_modules.clear_screen.clear_screen()
    # just before the session starts, find out when that is so it can be added to the session's file name
    start_time = str(datetime.now())
    quiz(cards, args, start_time)


if __name__ == '__main__':
    main()
