def find_errors_in_cards(filepath: str) -> dict:
    rendered_cards = {}

    with open(filepath, "r") as f:
        line_num = 1
        for line in f:
            if line[0] == "#":
                pass
            else:
                try:
                    key, value = line.strip().split("|")
                    rendered_cards[key.strip()] = value.strip()
                except ValueError:
                    print(f"Erorr parsing flash cards at line {line_num}")
            line_num += 1

    return rendered_cards

find_errors_in_cards("/Users/luna/flash-cards/languages/spanish/aqa/master-set.txt")
