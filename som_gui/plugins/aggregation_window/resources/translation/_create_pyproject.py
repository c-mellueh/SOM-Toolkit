import os


def list_files_in_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if (
                    file.endswith(".py")
                    or file.endswith(".ts")
                    or file.endswith(".qrc")
                    or file.endswith(".ui")
            ):
                if dirpath.endswith("\\qt") and file.endswith(".py"):
                    continue
                path = os.path.join(dirpath, file)
                output_dict["files"].append(path)


# Example usage:
output_dict = {"files": []}
root_directory = "..\\.."
list_files_in_directory(root_directory)
import json

with open("aggregation_window.pyproject", "w") as file:
    json.dump(output_dict, file, indent=4)

# call pyside6-project lupdate .
# call pyside6-project build .
