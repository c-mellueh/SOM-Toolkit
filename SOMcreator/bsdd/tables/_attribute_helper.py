import re
import pandas as pd

from SOMcreator.bsdd.bsdd_property import PropertyRelation

with open("allowed_value_table.md", "r", encoding='UTF-8') as file:
    text = file.read()
pattern = r"\|(.+)\|(.+)\|(.+)\|(.+)\|(.+)\|"

# Use the findall function to extract all rows that match the pattern
matches = re.findall(pattern, text)

header = [x.strip() for x in matches[0]]
data = matches[2:]
for index, row in enumerate(data):
    data[index] = [v.strip() for v in row]

# Create a pandas DataFrame using the extracted header and data rows
df = pd.DataFrame(data, columns=header)
dt_series = pd.Series({
    "Text":                     "str",
    "List of text":             "list[str]",
    "DateTime":                 "datetime",
    "Integer":                  "int",
    "List of ClassProperty":    "list[ClassProperty]",
    "List of ClassRelation":    "list[ClassRelation]",
    "List of Class":            "list[Class]",
    "List of Property":         "list[Property]",
    "Boolean":                  "bool",
    "Real":                     "float",
    "List of AllowedValue":     "list[AllowedValue]",
    "List of PropertyRelation": "list[PropertyRelation]",
})
df["python_datatype"] = df["DataType"].map(dt_series)
df.rename(columns={"Requ- ired?": "required"}, inplace=True)
df.loc[df["required"] == "", "required"] = False
df.loc[df["required"] != False, "required"] = True
for row, value in df.iterrows():
    default_text = "" if value["required"] else ", default=None"
    print(f'{value["Field"]}: {value["python_datatype"]} = field(init={value["required"]}{default_text})')
