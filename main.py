print("Loading...")

# external library code
import os
import sys
import time
import json
import random
import argparse
import readline
# import platform
from datetime import datetime
import matplotlib.pyplot as plt  # type: ignore

# my own library code
import my_modules.constants
# import my_modules.help
import my_modules.color
import my_modules.hint_system

"""
IMPORT GUIDE (examples of how you would use my library code)

`my_modules.constants` refers to `my_modules/constants.py`
`my_modules.help` refers to `my_modules/help.py`
`my_modules.color` refers to `my_modules/color.py`

`my_modules.constants.chars_to_ignore[i]`  # access the value at index `i` in the chars_to_ignore list
`my_modules.help.help_command()`  # call the help_command() procedure
`my_modules.color.Color.Blue(/Magenta/Bold/Reset)`  # access the specific color from the Color class

To explain it in a sentence (2 ways):
1. "call the help command from the file `help`, which is in the folder/directory `my_modules`."
2. "go to the folder/directory `my_modules`, go to the file `help`, call the help command."
"""


# static analyser might say readline is unused
# but it attaches to the builtin input() func


"""
a variable starting with `p_...` denotes a parameter, not a pointer
"terms" and "flash cards" are interchangable. 
    "term" refers to both the question and answer on each side of the flash card.
A "session" is one completion of all the flash cards from a file.
    A completed session means you've answered all the cards correctly once.

CONVENTIONS:

File paths in help text are written in Light Magenta
Commands in help text are written in Cyan
"""

parser = argparse.ArgumentParser(prog="main.py",
                                 description="Quizlet Write my version <https://github.com/RubberDuckCollector/quizlet-write> (name may change)",
                                 epilog="Made for flash card revision. Recommended for short answers.")


def plotting_graph():
    print("Plotting graph...")


def saving_graph():
    print("Saving graph...")


def make_session_bar_chart() -> str:
    # accesses stats/sessions-per-day.json to create a bar chart of sessions done per day using matplotlib
    try:
        with open("stats/sessions-per-day.json", "r") as f:
            data = f.read()
            sessions = json.loads(data)

            # DEBUGGING
            # print(sessions)
            # for key, value in sessions.items():
            #     print(f"KEY: {key}, VALUE: {value}")

            width_per_label = 0.3

            # group the values and keys of the dict into tuples.
            # `max()`: look at the tuple with the highest value at index 0 of the tuple
            # [0]: assigning index 0 of the tuple to the max value
            most_sessions_done = max(zip(sessions.values(), sessions.keys()))[0]

            # width per label * number of key-value pairs in the dict
            # we're plotting horizontally, so the sessions done (the dependent variable) go on the x axis, which controls the width of the graph
            fig_width = width_per_label * most_sessions_done

            # we're plotting horizontally, so the dates go on the y axis, which controls the height of the graph
            fig_height = width_per_label * len(sessions)

            # Set up figure with calculated width
            plt.figure(figsize=(fig_width, fig_height))

            plotting_graph()
            for key, value in sessions.items():
                plt.barh(key, value)

            plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
            now = datetime.now()
            plt.title(f"Session bar chart generated at {now}")
            plt.xlabel("# Sessions completed")
            plt.ylabel("Date (YYYY-MM-DD)")
            plt.xticks([i for i in range(0, most_sessions_done + 1, 1)])
            plt.gca().xaxis.set_ticks_position('both')
            plt.gca().tick_params(axis='x', labeltop=True, rotation=90)  # enable the dates on the y axis to be on the top of the graph as well as the bottom, rotates 90 degrees to make them readable
            plt.gca().yaxis.set_ticks_position('both')
            plt.gca().tick_params(axis='y', labelright=True)  # enable the dates on the y axis to be on the top of the graph as well as the bottom

            # bbox_inches = "tight" removes the bug of the title going offscreen if it's too long
            saving_graph()
            plt.savefig(f"stats/session-bar-charts/{now}.pdf", bbox_inches = "tight")


        # if all goes well
        result = f"Session bar chart created successfully in `{my_modules.color.Color.LightMagenta}stats/session-bar-charts/{my_modules.color.Color.Reset}`."
        return result
    except Exception as e:
        result = f"Error: {e}\nTry revising some flash cards first so you have data to use!"
        return result


def make_flash_card_bar_chart() -> str:
    # accesses stats/terms-per-day.json and plots a bar chart of the # terms done on each day
    try:
        file_path = "stats/terms-per-day.json"
        with open(file_path, "r") as f:
            data = f.read()
            terms_per_day = json.loads(data)

            # DEBUGGING
            # print(terms_per_day)
            # for key, value in terms_per_day.items():
            #     print(f"KEY: {key}, VALUE: {value}")

            width_per_label = 0.3

            most_terms_done = max(zip(terms_per_day.values(), terms_per_day.keys()))[0]

            # we're plotting horizontally, so the terms done go on the x axis, which controls the width of the graph
            fig_width = width_per_label * most_terms_done

            # we're plotting horizontally, so the dates go on the y axis, which controls the height of the graph
            fig_height = width_per_label * len(terms_per_day)

            plt.figure(figsize=(fig_width, fig_height))

            plotting_graph()
            for key, value in terms_per_day.items():
                plt.barh(key, value)

            plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
            now = datetime.now()
            plt.title(f"Flash card bar chart generated at {now}")
            plt.xlabel("# Flash cards answered")
            plt.ylabel("Date (YYYY-MM-DD)")
            plt.xticks([i for i in range(0, most_terms_done + 1, 1)])  # this can be as a list or one of Python's range() objects
            plt.gca().xaxis.set_ticks_position('both')
            plt.gca().tick_params(axis='x', labeltop=True, rotation=90)  # enable the dates on the y axis to be on the top of the graph as well as the bottom, rotates 90 degrees to make them readable
            plt.gca().yaxis.set_ticks_position('both')
            plt.gca().tick_params(axis='y', labelright=True)  # enable the dates on the y axis to be on the top of the graph as well as the bottom

            # bbox_inches = "tight" removes the bug of the title going offscreen if it's too long
            saving_graph()
            plt.savefig(f"stats/flash-card-bar-charts/{now}.pdf", bbox_inches = "tight")

        # if all goes well
        result = f"Flash card bar chart created successfully in `{my_modules.color.Color.LightMagenta}stats/flash-card-bar-charts/{my_modules.color.Color.Reset}`."
        return result
    except Exception as e:
        result = f"Error: {e}\nTry revising some flash cards first so you have data to use!"
        return result


def clear_screen():
    # not currently tested on Windows
    # if platform.system() == "Windows":
    #     os.system("cls")
    # else:
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


def dump_results_to_records_file(p_start_time, this_sessions_results_file: str) -> str:
    # when the session ends, find out when that is to put it in the session's file name
    end_time = str(datetime.now())
    # this copies the data in this_sessions_results_file to the records file for that session
    session_dir = f"stats/records/Session {p_start_time} to {end_time}"
    os.mkdir(session_dir)
    with open(this_sessions_results_file, 'r') as results_f, open(f"{session_dir}/session.txt", 'a') as record_f:
        for line in results_f:
            record_f.write(line)
    
    return session_dir


def write_terms_per_day(obj_to_be_written: str):
    file_path = "stats/terms-per-day.json"
    with open(file_path, 'w') as f:
        # comes in as a str, to turn it into a valid json obj
        # this turns any ' into ", which fixes the problem
        # to_be_written = json.dumps(obj_to_be_written)
        # f.write(to_be_written)

        json.dump(obj_to_be_written, f, indent=4)


def write_sessions_per_day(obj_to_be_written: str):
    file_path = "stats/sessions-per-day.json"
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

    x_axes = []  # terms completed
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

    this_sessions_results_file = f"temp-results-for-session-{datetime.now()}.txt"
    
    # user interaction will start in this try block
    # it's here to catch a keyboard interrupt such as ctrl-c
    # if it catches one, this_sessions_results_file will still be deleted, which is good
    # because it's a temp file and all actions are aborted if the session finishes early
    try:
        with open(this_sessions_results_file, "a") as f:
            f.write(f"cards from: {sys.argv[1]}\n")
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

                    if difficulty == my_modules.hint_system.VALID_DIFFICULTIES[0]:
                        hint = my_modules.hint_system.make_easy_hint(answer)
                    elif difficulty == my_modules.hint_system.VALID_DIFFICULTIES[1]:
                        hint = my_modules.hint_system.make_normal_hint(answer)
                    elif difficulty == my_modules.hint_system.VALID_DIFFICULTIES[2]:
                        hint = my_modules.hint_system.make_hard_hint(answer)
                    elif difficulty == my_modules.hint_system.VALID_DIFFICULTIES[3]:
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
                    progress = round(num_answered / NUM_TERMS, 2) * 100 if num_answered > 0 else 0.0

                    print(f"Working from file {my_modules.color.Color.Dim}{os.path.basename(sys_args[1])}{my_modules.color.Color.Reset}")
                    print(f"Remaining: {num_remaining}")
                    print(f"Correct: {my_modules.color.Color.Green}{num_correct}{my_modules.color.Color.Reset} ({current_percent_correct}%)")
                    print(f"Incorrect: {my_modules.color.Color.Red}{num_incorrect}{my_modules.color.Color.Reset}")
                    print(f"Progress: {my_modules.color.Color.LightBlue}{progress}{my_modules.color.Color.Reset}%")
                    print(f"Streak: {my_modules.color.Color.LightMagenta}{quiz_counter.get_current_streak()}{my_modules.color.Color.Reset} ({my_modules.color.Color.LightMagenta}{quiz_counter.get_highest_streak()}{my_modules.color.Color.Reset})")
                    # print(f"DEBUG: THEORETICAL_MAX_STREAK: {THEORETICAL_MAX_STREAK}")
                    # print(f"DEBUG: sys_args: {sys_args}")
                    print(f"What's the answer to {my_modules.color.Color.LightCyan}{prompt}{my_modules.color.Color.Reset}?")
                    print(f"Hint: {my_modules.color.Color.Dim}{hint}{my_modules.color.Color.Reset}")
                    user_response = input("> ").strip()

                    # print num_remaining, num_correct, num_incorrect
                    # print(f"Remaining: {num_remaining}\nCorrect: {num_correct}\nIncorrect: {num_incorrect}")

                    # if the user input is falsy
                    # i.e there were only spaces and strip() has removed them to leave an empty string
                    if not user_response:
                        print("Don't know? Copy out the answer so you remember it!")
                        quiz_counter.reset_streak()
                        while True:
                            user_response = input(f"Copy the answer below ↓\n- {answer}\n> ").strip()
                            if user_response.lower() == answer.lower():
                                print(f"{my_modules.color.Color.Cyan}Next question.{my_modules.color.Color.Reset}")
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
                            print(f"{my_modules.color.Color.Green}Correct. Well done!{my_modules.color.Color.Reset}")

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
                            print(f"{my_modules.color.Color.Green}Correct{my_modules.color.Color.Reset}")

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
                                clear_screen()

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
                                clear_screen()

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
                print_round_breakdown(this_sessions_results_file, f"Round {round_num}:", num_correct, num_answered)
                
                # randomise now if rand flag is set to --rand-every-round
                if sys_args[3] == "-rand-every-round":
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


            # write the round list to this_sessions_results_file
            f.write(f"{sys_args[2]}\n")
            f.write(f"{sys_args[3]}\n")
            f.write(f"{sys_args[4]}\n")
            f.write(f"No. terms in the card set = {NUM_TERMS}\n")
            f.write(f"highest_streak = {quiz_counter.get_highest_streak()}\n")
            f.write(f"perfect_streak = {quiz_counter.get_highest_streak() == THEORETICAL_MAX_STREAK}")  # this should resolve to True or False

        this_sessions_dir = dump_results_to_records_file(start_time, this_sessions_results_file)

        width_per_label = 0.3

        # defining the x ticks i need here so i can use the variable to set `plt.xticks()`
        # and also calculate the graph's width based on the number of ticks, hence `len(my_x_ticks)` ...
        # ... (which are 2 different things)
        my_x_ticks = [i for i in range(1, NUM_TERMS + 1)]
        
        # Calculate the figure width based on the number of x-axis labels
        fig_width = max(8, width_per_label * len(my_x_ticks))  # Ensure minimum width

        fig_height = width_per_label * 101  # 0.3 width per label multiplied by 101 y ticks from 0-100 inclusive

        # Set up figure with calculated width
        plt.figure(figsize=(fig_width, fig_height))


        # the graph is plotted and saved here at the end of the session to maintain the atomicity of the program.
        # either the session is completed in its entirity, or everything is aborted and it's like nothing happened at all

        # plot each y-axis data series with its corresponding x-axis values
        plotting_graph()
        for i, (x_data, y_data) in enumerate(zip(x_axes, y_axes)):
            plt.plot(x_data, y_data, label=f'Round {i + 1}', marker='o')  # i think the dots make it more readable across a larger graph

        plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)

        # plt.plot(x_axes, y_axes)
        plt.title(f"Consistency line graph for session starting at {start_time}\nPath to cards: {sys.argv[1]}")
        plt.xlabel("# Terms answered")
        plt.ylabel("% Accuracy")
        plt.ylim(0, 100)  # y axis goes from 0 to 100
        plt.legend(loc="best")  # force the key to appear on the graph, "best" means that matplotlib will put it in the least obtrusive area using its own judgement
        # plt.yticks([i for i in range(0, 101, 5)])
        plt.xticks([i for i in range(0, NUM_TERMS + 1, 1)])
        plt.yticks([i for i in range(0, 101, 1)])
        plt.gca().xaxis.set_ticks_position('both')  # puts the x and y axes on the right and top of the graphs, increases readablilty for long graphs
        plt.gca().tick_params(axis='x', labeltop=True, rotation=90)  # enable x axis numbers on the right side of the graph as well as the left, also rotates those numbers by 90 degrees to make them readable
        plt.gca().yaxis.set_ticks_position('both')
        plt.gca().tick_params(axis='y', labelright=True)  # enable y axis numbers on the top of the graph as well as the bottom
        saving_graph()
        # bbox_inches = "tight" removes the bug of the title going offscreen if it's too long
        # https://stackoverflow.com/a/59372013
        plt.savefig(f"{this_sessions_dir}/line-graph.pdf", bbox_inches = "tight")

        # write the x axis data and the y axis data to special files in `this_sessions_dir`
        # this allows the graph to be reproduced
        with open(f"{this_sessions_dir}/x-axis-data.txt", "w") as f:
            f.write(f"{x_axes}")

        with open(f"{this_sessions_dir}/y-axis-data.txt", "w") as f:
            f.write(f"{y_axes}")

        # after the record file is done, print the session breakdown to the user

        print(f"{my_modules.color.Color.Bold}Session breakdown:{my_modules.color.Color.Reset}")

        with open(this_sessions_results_file, 'r') as f:
            for line in f:
                # print the line without leading/trailing whitespaces
                if '✓' in line:  # check for tick
                    print(f"{my_modules.color.Color.Green}{line.strip()}{my_modules.color.Color.Reset}")
                elif '✗' in line:  # check for cross
                    print(f"{my_modules.color.Color.Red}{line.strip()}{my_modules.color.Color.Reset}")
                else:
                    print(line.strip())  # otherwise don't colour the line


        try:
            # putting this code here instead of at the top of `quiz()` fixes the bug,
            # where only one session would add to the terms done count for that day
            # instead of a second session
            # disclaimer: bug only found with two concurrent sessions
            terms_per_day_file_path = "stats/terms-per-day.json"
            if not os.path.exists(terms_per_day_file_path):
                # create file if it doesn't exist
                with open(terms_per_day_file_path, 'w') as f:
                    f.write("{}")
            with open(terms_per_day_file_path, 'r') as terms_f:
                # terms_done_dict = json.loads(f.readline())
                terms_done_dict = json.load(terms_f)

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

            write_terms_per_day(terms_done_dict)

            # show the user the increase in terms done today
            print(f"Terms done today: {new_terms_completed - NUM_TERMS} {my_modules.color.Color.LightGreen}->{my_modules.color.Color.Reset} {new_terms_completed}")

            # repeat the same process but for sessions done today
            sessions_per_day_file_path = "stats/sessions-per-day.json"
            if not os.path.exists(sessions_per_day_file_path):
                # create file if it doesn't exist
                with open(sessions_per_day_file_path, 'w') as f:
                    f.write("{}")
            with open(sessions_per_day_file_path, "r") as sessions_f:
                sessions_done_dict = json.load(sessions_f)

            new_sessions_completed = 0
            
            # current date and time not assigned again so we can have the same date for both the session and the terms count
            # i.e date cannot progress in between that code and this code and have an effect on the code's function

            # sessions that end on a particular day will contribute to the terms and sessions done per day counts
            if today in sessions_done_dict:
                sessions_done_dict[today] += 1
                new_sessions_completed = sessions_done_dict[today]
            else:
                # not in there, can safely write new day
                sessions_done_dict[today] = 1

                # fixes the bug where new_sessions_completed is negative on a day with 0 previously completed sessions
                new_sessions_completed += 1

            write_sessions_per_day(sessions_done_dict)

            # show the user the increase in sessions done today
            print(f"Sessions done today: {new_sessions_completed - 1} {my_modules.color.Color.LightGreen}->{my_modules.color.Color.Reset} {new_sessions_completed}")


            # delete the temp file as it has served its purpose
            os.remove(this_sessions_results_file)
        except Exception as e:
            print("error while saving data.")
            print(e)

    except (KeyboardInterrupt, EOFError) as _:
        # if the user stops the program with ctrl c or ctrl d, also delete the file
        # to make it like nothing ever happened
        os.remove(this_sessions_results_file)


def render_cards(filepath: str) -> dict:
    rendered_cards = {}

    # first, check that the cards have no errors in them
    with open(filepath, "r") as f:
        line_num = 1
        for line in f:
            if line.strip() == "" or line[0] == "#":
                continue
            elif "|" not in line:
                # presence check for the | 
                print(f"Error while parsing flash cards from {filepath}: a | character was not found at line {line_num}.")
                sys.exit(0)
            elif line.count("|") > 1:
                # presence check for the | 
                print(f"Error while parsing flash cards from {filepath}: more than one | character not found at line {line_num}.")
                sys.exit(0)
            else:
                left, right = line.split("|", 1)
                if not left.strip():
                    # presence check for the content left of the |
                    print(f"Error while parsing flash cards from {filepath}: term (content on the left of the |) was not found at line {line_num}.")
                    sys.exit(0)
                if not right.strip():
                    # presence check for the content right of the |
                    """
                    .strip() is important here because:
                        - if there is no content on the right side on the line to begin with (e.g: `hello|`)
                        - an empty string will be processed, which is not what we want because the if statement will not trigger, we want the error to trigger.
                    """
                    print(f"Error while parsing flash cards from {filepath}: definition (content on the right of the |) was not found at line {line_num}.")
                    sys.exit(0)
            line_num += 1

    # TODO: make it so the program checks the whole file for #s instead of just the first instance. record the largest line number's length as a string and place the |s after the last digit of the longest line number found, e.g: `1  |, 100|`
    # then, print out the lines that start with hashtags
    hashtag_in_file = False
    with open(filepath, "r") as f:
        for line in f:
            if line[0] == "#":
                hashtag_in_file = True
                break

    if hashtag_in_file is True:
        clear_screen()
        with open(filepath, "r") as f:
            line_num = 1
            print("Comments found in the flash card file:")
            for line in f:
                if line[0] == "#":
                    # for some reason they're printed with two \ns instea of the usual one \n
                    print(f"{line_num}|{line}", end="")
                else:
                    pass
                line_num += 1
            input("Press enter to proceed.")


    # now we can start parsing.
    with open(filepath, "r") as f:
        for line in f:
            if line.strip() == "" or line[0] == "#":
                pass
            else:
                key, value = line.strip().split("|")
                rendered_cards[key.strip()] = value.strip()

    # return this as the dictionary of terms and definitions
    # e.g: "hello": "hola",
    # the key is on the left, its corresponding value is on the right
    return rendered_cards


# main() handles command line arguments
# needed for value checking and presence checking of the command line args
def main():

    # order of arguments:
    # help/main.py/bar-chart
    # file path to file containing questions,
    # difficulty,
    # randomise terms,
    # switch question and answer

    # add optional arguments
    parser.add_argument("--explain_app_usage", action="store_true", help="gives a walkthrough of the average user's interactions with the program")
    parser.add_argument("--technical_explanation", action="store_true", help="gives a walkthrough of the average user's interactions with the program")
    # bar charts
    parser.add_argument("--make_session_bar_chart", action="store_true", help="Generates a bar chart of the sessions done on each day")
    parser.add_argument("--make_flash_card_bar_chart", action="store_true", help="Generates a bar chart of the flash cards done on each day")

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
    parser.add_argument("flash_card_file_path", nargs="?", default=None, help="This is a relative or absolute file path to a text file containing the flash cards you want to use", type=str)
    parser.add_argument("difficulty", nargs="?", default=None,  help="Difficulty of the quiz", type=str)
    parser.add_argument("randomise", nargs="?", default=None,  help="How you want to randomise the flash cards in the quiz", type=str)
    parser.add_argument("flip_terms", nargs="?", default=None,  help="Wether or not you want to flip the cards over and answer with the question", type=str)

    # if sys.argv only contains `main.py`
    # print help and halt program execution
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()  # parse arguments in the order declared in the code

    if args.explain_app_usage:
        print("explain app usage - import commands.py (write long things in there)")
        sys.exit(0)
    elif args.technical_explanation:
        print("technical explanation - commands.py")
        sys.exit(0)
    elif args.make_session_bar_chart:
        print(make_session_bar_chart())
        sys.exit(0)
    elif args.make_flash_card_bar_chart:
        print(make_flash_card_bar_chart())
        sys.exit(0)

    file_path = args.flash_card_file_path

    difficulty = args.difficulty

    if difficulty in my_modules.hint_system.VALID_DIFFICULTIES:
        pass
    else:
        print("Error: difficulty selection can only be one of: easy | normal | hard | very-hard")
        return

    randomise = args.randomise

    print("Rendering cards...")
    cards = render_cards(file_path)

    # will be handled in quiz()
    match randomise:
        case "rand-once":
            # randomise only at the start of the session
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
        case "rand-every-round":
            # randomise after the end of every round 
            items = list(cards.items())
            random.shuffle(items)
            cards = dict(items)
            pass
        case "no-rand":
            # don't randomise, pass as the cards can be used as-is
            pass
        case _:
            print("Error: randomise setting can only be one of: rand-once | no-rand | rand-every-round")
            return

    flip_terms = args.flip_terms
    match flip_terms:
        case "flip":
            # switch terms and definitions
            cards = {v: k for k, v in cards.items()}
        case "no-flip":
            # good to go, use cards as-is
            pass
        case _:
            print("Error: flip setting can only be one of: flip | no-flip")
            return

    clear_screen()
    quiz(cards, difficulty, sys.argv)


if __name__ == '__main__':
    main()
