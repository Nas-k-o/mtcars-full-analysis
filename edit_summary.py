# For this part we will be using pandas
import pandas as pd
import os

def list_csv_files(directory="data"):
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    for idx, file in enumerate(files, start=1):
        print(f"[{idx}] - {file}")
    return files

def select_csv():
    files = list_csv_files()
    choice = int(input("Select File: "))
    if 1 <= choice <= len(files):
        route = os.path.join("data", files[choice - 1])
        print(load_r_summary_csv(route))
    else:
        print("Invalid selection.")

# Using this method we will transform the summaries into a beautiful table
def load_r_summary_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_data = []
    row_labels = ["Min.", "1st Qu.", "Median", "Mean", "3rd Qu.", "Max."]

    for i, line in enumerate(lines[1:]):
        parts = line.strip().split('","')
        label = row_labels[i] if i < len(row_labels) else f"Row{i + 1}"

        values = []
        # skip the initial empty string
        for p in parts[1:]:
            clean = p.replace('"', '').split(":")[-1].strip()
            try:
                values.append(float(clean))
            except:
                values.append(None)

        cleaned_data.append((label, values))

    # Extract column names from the second line (without summary labels)
    raw_header = lines[0].strip().split('","')[1:]
    columns = [h.replace('"', '').strip() for h in raw_header]

    df = pd.DataFrame({col: [v[i] for _, v in cleaned_data] for i, col in enumerate(columns)})
    df.insert(0, "Stat", [label for label, _ in cleaned_data])
    return df

list_csv_files()
select_csv()