import os
import inspect
import sys
import som_gui.tool

def get_class_methods_and_params(cls, file):
    methods = inspect.getmembers(cls, predicate=inspect.ismethod)

    for name, method in methods:
        sig = inspect.signature(method)
        params = [p.name for p in sig.parameters.values()]
        file.write(f"    def {name}(self, {', '.join(params)}): pass\n\n")


def main(file):
    path = f"som_gui.tool"
    for c_name, cls in inspect.getmembers(sys.modules[path], inspect.isclass):
        file.write(f"\nclass {c_name}:\n")
        get_class_methods_and_params(cls, file)


if __name__ == "__main__":
    file_path = "som_gui/core/tool.py"
    with open(file_path, "w") as f:
        main(f)
    print("Done")