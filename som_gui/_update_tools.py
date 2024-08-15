import sys
import inspect
import som_gui.tool


def cls_is_toolclass(cls):
    if "__init__" in [x[0] for x in inspect.getmembers(cls, predicate=inspect.isfunction)]:
        return False
    return True


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
    file_path = "core/tool.py"

    with open(file_path, "w") as f:
        main(f)
