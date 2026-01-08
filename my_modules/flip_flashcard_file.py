import os
import my_modules

def flip_flashcard_file(file_path: str) -> str:
    """
    procedure: implement an optional command line argument
    where the program switches the position of the term and
    answer on each line of a flash card file, edits the file itself
    MAYBE USE `render_cards()`
    NEED `os.path.basename()` which gets the file name
        path to the file specified by os.path.basename() which is where the "FILENAME_output" goes (the same dir)
    """

    if not my_modules.validate.validate_file(file_path):
        raise ValueError("Cards are not correctly formatted. See above message to fix.")

    output_file_path = f"{os.getcwd()}/output/{os.path.basename(file_path)}_flipped.txt"
    result = f"Swap term and definition of all cards completed successfully at destination {output_file_path}"
    try:
        data = []
        with open(file_path, "r") as f:
            for _ in f:
                """split each line on |, the content on the left side of | is the value and the content on the right side is the key"""
                data = f.read().split("\n")
                data = list(filter(None, data)) # removes any elements that are only empty strings
        data = [i.split("|") for i in data]  # every element is a string. splits each string on the | and each half is its own element in a sublist

        # write to output file, swapping the questions and answers
        with open(output_file_path, "w") as f:
            for i in data:
                f.write(f"{i[1]}|{i[0]}\n")

    except Exception as e:
        result = f"Error: {e}"
    return result
