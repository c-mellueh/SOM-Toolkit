from desiteRuleCreator.main_window import main as run_main
from desiteRuleCreator.Filehandling import open_file
from SOMcreator import classes
def test():
    proj = classes.Project("Test")
    path = "C:/Users/ChristophMellueh/Desktop/excel_test.xlsx"
    proj.import_excel(path)

    for aggreg in classes.Aggregation:
        if not aggreg.is_root:
            print(f"{aggreg.name} -> {aggreg.parent.name}: {aggreg.parent_connection}")
        else:
            print(f"{aggreg.name} -> root")


def main():
    print("PYTHON CODE STARTING")
    run_main()
    # test()
if __name__ == '__main__':
    main()
