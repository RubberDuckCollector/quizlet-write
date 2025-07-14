import os
import my_modules.clear_screen


def validate_file(file_path: str) -> bool:
    """
    returns False if invalid, checks for proper formatting of flash card file:
    1. content|more-content
        - if there is missing data either side of |, False is returned
        - if | is missing, False is returned
        - there must be exactly one | on each line of the file that has content.
    2. lines starting with a # are shown to the user
    3. empty lines are ignored
    """

    # first, check that the file is not empty
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"Error while parsing flash cards from {file_path}: File is empty.")
            return False
    except FileNotFoundError as e:
        print("File NOT found.")
        print(e)
        return False

    # then, check that the cards have no errors in them
    with open(file_path, "r") as f:
        line_num = 1
        for line in f:
            if line.strip() == "" or line[0] == "#":
                continue
            elif "|" not in line:
                # presence check for the | 
                print(f"Error while parsing flash cards from {file_path}: a | character was not found at line {line_num}.")
                return False
            elif line.count("|") > 1:
                # presence check for the | 
                print(f"Error while parsing flash cards from {file_path}: more than one | character not found at line {line_num}.")
                return False
            else:
                left, right = line.split("|", 1)
                if not left.strip():
                    # presence check for the content left of the |
                    print(f"Error while parsing flash cards from {file_path}: term (content on the left of the |) was not found at line {line_num}.")
                    return False
                if not right.strip():
                    # presence check for the content right of the |
                    """
                    .strip() is important here because:
                        - if there is no content on the right side on the line to begin with (e.g: `hello|`)
                        - an empty string will be processed, which is not what we want because the if statement will not trigger, we want the error to trigger.
                    """
                    print(f"Error while parsing flash cards from {file_path}: definition (content on the right of the |) was not found at line {line_num}.")
                    return False
            line_num += 1

    # TODO: make it so the program checks the whole file for #s instead of just the first instance. record the largest line number's length as a string and place the |s after the last digit of the longest line number found, e.g: `1  |, 100|`
    # then, print out the lines that start with hashtags
    hashtag_in_file = False
    with open(file_path, "r") as f:
        for line in f:
            if line[0] == "#":
                hashtag_in_file = True
                break

    if hashtag_in_file is True:
        my_modules.clear_screen.clear_screen()
        with open(file_path, "r") as f:
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

    return True
