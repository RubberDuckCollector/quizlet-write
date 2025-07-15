import os
import json
import pathlib

def sync() -> bool:
    # TODO: maybe try to scan before asking to sync

    # will change to True when correct behavior is completed, at the end of the function returns this variable
    # function returns False if there's an error
    result: bool = False 

    # returns False if unsuccessful
    try:
        # get list of directories in PROJECT_ROOT/stats/records
        dir_names = [f"{pathlib.Path(__file__).parents[1]}/stats/records/" + dir_name for dir_name in os.listdir(f"{pathlib.Path(__file__).parents[1]}/stats/records/")]
        for i in dir_names:
            if ".md" in i:
                dir_names.pop(dir_names.index(i))
    except Exception as e:
        print(e)
        print("Error while reading and processing directory/file names for counting correct/incorrect totals. Aborting operations.")
        return False

    try:
        # read from the files inside the dirs that `dir_names` contains
        correct_count = 0
        incorrect_count = 0
        for i in dir_names:
            with open(f"{i}/session.txt", "r") as f:
                data = f.readlines()
                for j in data:
                    if "✓" == j[0]:
                        correct_count += 1
                    elif "✗" == j[0]:
                        incorrect_count += 1
        try:
            # overwrite data in PROJECT_ROOT/stats/lifetime_stats.json
            with open(f"{pathlib.Path(__file__).parents[1]}/stats/lifetime_stats.json", "r") as f:
                data = json.load(f)

            with open(f"{pathlib.Path(__file__).parents[1]}/stats/lifetime_stats.json", "w") as f:
                data["lifetime_correct_answers"] = correct_count
                data["lifetime_incorrect_answers"] = incorrect_count
                json.dump(data, f, indent=4)
                result = True
        except Exception as e:
            print(e)
            print("Error while opening session files and counting correct and incorrect figures. Aborting operations.")
            return False
    except Exception as e:
        print(e)
        print("Error while opening session files and counting correct and incorrect figures. Aborting operations.")
        return False
    
    # returns False if unsuccessful
    # try:
    #     """
    #     1. get all session dir names
    #     go into each directory in dir_names
    #     get a list of all the files in the directory
    #     if session.json is present, pop that directory from dir_names
    #     dir_names will be left with only the names of directories that DON'T have session.json in them
    #     """

    #     # get list of directories in PROJECT_ROOT/stats/records
    #     # remaking dir_names list as defensive design as i can put code above this try block in the future and not have this try block depend on any other "module" of code within this file
    #     dir_names = [f"{pathlib.Path(__file__).parents[1]}/stats/records/" + dir_name for dir_name in os.listdir(f"{pathlib.Path(__file__).parents[1]}/stats/records/")]
    #     for i in dir_names:
    #         if ".md" in i:
    #             dir_names.pop(dir_names.index(i))

    #     for i in dir_names:
    #         files = os.listdir(i)
    #         if "session.json" in files:
    #             dir_names.pop(dir_names.index(i))
    #         else:
    #             pass
    #     # print(dir_names)
    #     # TODO: look into session.txt in each directory that dir_names contains
    #     # TODO: read the bottom lines of the file
    #     # TODO: transfer that data to the session.json format (put it in a python dict)
    #     # TODO: dump that dict with json lib into session.json
    #     # TODO: make assumptions as not all session.txt data has every field as it does now
    #     for i in dir_names:
    #         with open(f"{i}/session.txt", "r") as f:
    #             # look at all lines below the last blank line
    #             lines = f.readlines()

    #             # get all lines below last blank line
    #             # count backwards until you see a list element with just "\n" in it
    #             stop_index = 0
    #             for i in reversed(range(len(lines))):
    #                 if lines[i].strip() == "":
    #                     stop_index = i
    #                     break
    #             lines = lines[stop_index+1:]
    #             for i in lines:
    #                 # the flags start with a "-" in old versions so you have to remove them
    #                 if i[0] == "-":
    #                     i.removeprefix("-")
    #             return False
    # except Exception as e:
    #     print(e)
    #     print("Error while reading and processing directory/file names for creating session.json for old sessions. Aborting operations.")
    #     return False

    # try:
    #     # try to retroactively build session.json files in record directories that don't have one
    #     ...
    # except Exception as e:
    #     print(e)
    #     print("Error while trying to retroactively build session.json files in record directories that don't have one.")
    #     return False

    return result


sync()
