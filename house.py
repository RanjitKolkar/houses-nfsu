import pandas as pd
import os

DATA_FOLDER = "NFSU DATA"
OUTPUT_FILE = "students_with_houses1.xlsx"
HOUSES = ["A", "B", "C", "D"]

def clean_columns(cols):
    return (
        cols.astype(str)
        .str.strip()
        .str.replace("\xa0", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )

def load_all_excels():
    all_data = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".xlsx"):
            path = os.path.join(DATA_FOLDER, file)
            df = pd.read_excel(path, header=2)
            df.columns = clean_columns(df.columns)

            if "Stream" in df.columns:
                df["Program"] = df["Stream"]
            else:
                df["Program"] = os.path.splitext(file)[0]

            df["Gender"] = df["Gender"].astype(str).str.upper().str.strip()
            all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

def assign_houses(df):
    df = df.copy()
    df["House"] = None

    # Ensure Semester exists
    if "Semester" not in df.columns:
        raise Exception("Semester column not found in data")

    for program in df["Program"].dropna().unique():
        prog_df = df[df["Program"] == program]

        for semester in prog_df["Semester"].dropna().unique():
            sem_df = prog_df[prog_df["Semester"] == semester]

            for gender in sem_df["Gender"].dropna().unique():
                group = sem_df[sem_df["Gender"] == gender]

                for i, idx in enumerate(group.index):
                    df.loc[idx, "House"] = HOUSES[i % len(HOUSES)]

    return df


def main():
    df = load_all_excels()
    df = assign_houses(df)

    if df["House"].isna().any():
        raise Exception("Some students were not assigned houses!")

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ House assignment complete. File saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
