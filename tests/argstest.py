import argparse


parser = argparse.ArgumentParser()

parser.add_argument("flash_card_file_path", help="This is a relative or absolute file path to a text file containing the flash cards you want to use", type=str)
parser.add_argument("difficulty", help="Difficulty of the quiz", type=str)
parser.add_argument("randomise", help="How you want to randomise the flash cards in the quiz", type=str)
parser.add_argument("flip_terms", help="Wether or not you want to flip the cards over and answer with the question", type=str)
args = parser.parse_args()

print(args)
print(args.flash_card_file_path)
