import pandas as pd

input_file = "Excel/MOLT.xlsx"
output_file = "molt.txt"

df = pd.read_excel(input_file, header=[1,2])
df.columns = df.columns.get_level_values(0)

bodies = []
constraints = []

for i in range(len(df)):
    if pd.isna(df.loc[i, "Name"]):
        continue

    body = {}
    body["name"] = df.loc[i, "Name"]

    if not pd.isna(df.loc[i, "Parent"]):
        body["parent"] = df.loc[i, "Parent"]

    if not pd.isna(df.loc[i, "POS"]):
        body["pos"] = str(df.loc[i, "POS"])

    if not pd.isna(df.iloc[i, 3]):
        body["joint"] = {}

        if not pd.isna(df.iloc[i, 3]):
            body["joint"]["type"] = df.iloc[i, 3]

        if not pd.isna(df.iloc[i, 4]):
            body["joint"]["axis"] = str(df.iloc[i, 4])

        if not pd.isna(df.iloc[i, 5]):
            body["joint"]["damping"] = str(df.iloc[i, 5])

    if not pd.isna(df.iloc[i, 6]):
        body["geom"] = {}
        body["geom"]["type"] = df.iloc[i, 6]

        if df.iloc[i, 6] == "capsule":
            if not pd.isna(df.iloc[i, 7]):
                body["geom"]["fromto"] = str(df.iloc[i, 7])
        else:
            if not pd.isna(df.iloc[i, 7]):
                body["geom"]["size"] = str(df.iloc[i, 7])

        if not pd.isna(df.iloc[i, 8]):
            body["geom"]["mass"] = str(df.iloc[i, 8])

        if not pd.isna(df.iloc[i, 9]):
            body["geom"]["friction"] = str(df.iloc[i, 9])

    if not pd.isna(df.iloc[i, 10]):
        body["site"] = {
            "name": df.iloc[i, 10]
        }

        if not pd.isna(df.iloc[i, 11]):
            body["site"]["pos"] = str(df.iloc[i, 11])

    bodies.append(body)

df_constraint = pd.read_excel(input_file, header=1, usecols="O:Q")
constraints = []

for i in range(len(df_constraint)):
    if pd.isna(df_constraint.loc[i, "Type"]):
        continue

    constraint = {
        "type": df_constraint.loc[i, "Type"]
    }

    if not pd.isna(df_constraint.loc[i, "Site1"]):
        constraint["site1"] = df_constraint.loc[i, "Site1"]

    if not pd.isna(df_constraint.loc[i, "Site2"]):
        constraint["site2"] = df_constraint.loc[i, "Site2"]

    constraints.append(constraint)

with open(output_file, "w") as f:

    f.write("bodies = [\n")

    for b in bodies:
        f.write("    {\n")

        for key, value in b.items():

            if isinstance(value, dict):
                f.write(f"        '{key}': {{\n")
                for k2, v2 in value.items():
                    f.write(f"            '{k2}': '{v2}',\n")
                f.write("        },\n")
            else:
                f.write(f"        '{key}': '{value}',\n")

        f.write("    },\n")

    f.write("]\n\n")

    f.write("constraints = [\n")
    for c in constraints:
        f.write("    {\n")
        for k, v in c.items():
            f.write(f"        '{k}': '{v}',\n")
        f.write("    },\n")
    f.write("]\n")

print("Đã tạo file:", output_file)