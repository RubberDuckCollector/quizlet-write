def flip_flash_card_file(filepath: str) -> str:
    """
    procedure: implement an optional command line argument
    where the program switches the position of the term and
    answer on each line of a flash card file, edits the file itself
    MAYBE USE `render_cards()`
    """

    result = "Swap term and definition of all cards completed successfully."
    try:
        card_dict = {}
        with open(filepath, "r") as f:
            for line in f:
                """split each line on |, the content on the left side of | is the value and the content on the right side is the key"""
                data = f.readline().split()
                print(data)
                return ""
        for key, value in card_dict.items():
            key, value = value, key

        output_filepath = f"{filepath}_output.txt"
    except Exception as e:
        result = f"Error: {e}"
    return result


def main():
    print(flip_flash_card_file())


if __name__ == "__main__":
    main()
