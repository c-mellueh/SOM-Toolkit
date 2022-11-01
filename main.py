from desiteRuleCreator.main_window import main as run_main
from desiteRuleCreator.Filehandling import open_file
from SOMcreator import classes
def test():
    proj = classes.Project("Test")
    path = "C:/Users/ChristophMellueh/Desktop/excel_test.xlsx"
    proj.import_excel(path)

    for obj in classes.Object:
        print(obj)


def main():
    print("PYTHON CODE STARTING")
    run_main()

if __name__ == '__main__':
    main()
