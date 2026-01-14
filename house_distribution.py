import pandas as pd
import os
from collections import defaultdict

DATA_FOLDER = "NFSU DATA"
OUTPUT_FILE = "students_with_houses3.xlsx"
houses = ["M", "U", "T", "L"]

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



def assign_houses(df,houses):
    df = df.copy()
    df["House"] = None

    required_cols = {"Program", "Semester", "Gender"}
    if not required_cols.issubset(df.columns):
        raise Exception(f"Missing required columns: {required_cols - set(df.columns)}")

    # Counters
    gender_counts = defaultdict(lambda: defaultdict(int))
    semester_counts = defaultdict(lambda: defaultdict(int))
    program_counts = defaultdict(lambda: defaultdict(int))

    # Process program-wise for locality
    for program in df["Program"].dropna().unique():
        prog_df = df[df["Program"] == program]

        for semester in prog_df["Semester"].dropna().unique():
            sem_df = prog_df[prog_df["Semester"] == semester]

            for gender in sem_df["Gender"].dropna().unique():
                group = sem_df[sem_df["Gender"] == gender]

                for idx in group.index:
                    # Choose house with minimum usage for this gender
                    house = min(
                        houses,
                        key=lambda h: (
                            gender_counts[gender][h],
                            semester_counts[(program, semester)][h],
                            program_counts[program][h]
                        )
                    )

                    df.loc[idx, "House"] = house

                    # Update counters
                    gender_counts[gender][house] += 1
                    semester_counts[(program, semester)][house] += 1
                    program_counts[program][house] += 1

    return df



def main():
    df = load_all_excels()
    df = assign_houses(df, houses)

    if df["House"].isna().any():
        raise Exception("Some students were not assigned houses!")

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ House assignment complete. File saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
