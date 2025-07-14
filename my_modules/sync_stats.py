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
        print("Error while reading and processing directory/file names. Aborting operations.")
        print(e)
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
            print("Error while opening session files and counting correct and incorrect figures. Aborting operations.")
            print(e)
            return False
    except Exception as e:
        print("Error while opening session files and counting correct and incorrect figures. Aborting operations.")
        print(e)
        return False
    
    try:
        # try to retroactively build session.json files in record directories that don't have one
        print("test")
    except Exception as e:
        print("Error while trying to retroactively build session.json files in record directories that don't have one.")
        print(e)
        return False

    return result


sync()
