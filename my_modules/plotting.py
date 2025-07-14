import json
import my_modules.color
from datetime import datetime
import matplotlib.pyplot as plt


def plotting_graph():
    print("Plotting graph...")


def saving_graph():
    print("Saving graph...")


def make_session_bar_chart() -> str:
    # accesses stats/sessions-per-day.json to create a bar chart of sessions done per day using matplotlib
    try:
        with open("stats/lifetime_stats.json", "r") as f:
            data = json.load(f)
            sessions = data["sessions_per_day"]

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

            plt.grid(color = 'grey', linestyle = '-', linewidth = 0.3)

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
    # accesses stats/lifetime_stats.json and plots a bar chart of the # cards done on each day
    try:
        with open("stats/lifetime_stats.json", "r") as f:
            data = json.load(f)
            cards_per_day = data["cards_per_day"]

            # DEBUGGING
            # print(cards_per_day)
            # for key, value in cards_per_day.items():
            #     print(f"KEY: {key}, VALUE: {value}")

            width_per_label = 0.3

            most_cards_done = max(zip(cards_per_day.values(), cards_per_day.keys()))[0]

            # we're plotting horizontally, so the  done go on the x axis, which controls the width of the graph
            fig_width = width_per_label * most_cards_done

            # we're plotting horizontally, so the dates go on the y axis, which controls the height of the graph
            fig_height = width_per_label * len(cards_per_day)

            plt.figure(figsize=(fig_width, fig_height))

            plotting_graph()
            for key, value in cards_per_day.items():
                plt.barh(key, value)

            plt.grid(color = 'grey', linestyle = '-', linewidth = 0.3)

            now = datetime.now()
            plt.title(f"Flash card bar chart generated at {now}")
            plt.xlabel("# Flash cards answered")
            plt.ylabel("Date (YYYY-MM-DD)")
            plt.xticks([i for i in range(0, most_cards_done + 1, 1)])  # this can be as a list or one of Python's range() objects
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
