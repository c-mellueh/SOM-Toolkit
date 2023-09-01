# __main__.py
from som_gui import main_window

def main(initial_file:str|None = None):
    main_window.main(initial_file)

if __name__ == "__main__":
    main()