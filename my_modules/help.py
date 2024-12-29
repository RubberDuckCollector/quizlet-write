import my_modules.color


"""
CONVENTIONS:

File paths in help text are written in Light Magenta
Commands in help text are written in Cyan
"""


def help_command():
    help_statements = {
        f"-make-session-bar-chart": f"creates a bar chart using data from `{my_modules.color.Color.LightMagenta}stats/sessions-per-day.json{my_modules.color.Color.Reset}`",
        f"-make-flash-card-bar-chart": f"creates a bar chart using data from `{my_modules.color.Color.LightMagenta}stats/terms-per-day.json{my_modules.color.Color.Reset}`",
        "-explain-app-usage": "gives a walkthrough of the average user's interactions with the program",
        "-technical-explanation": "gives a technical explanation of the code",
    }

    max_left_length = max(len(i) for i in help_statements.keys())

    print("\nQuizlet Write my version <https://github.com/RubberDuckCollector/quizlet-write> (name may change)")
    for key, value in help_statements.items():
        print(f"  {key.ljust(max_left_length)}\t\t{value}")

