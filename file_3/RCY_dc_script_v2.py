import os
import pandas as pd

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
F18_DECAY = 109.77

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_file(file_path):
    df = pd.read_csv(file_path)

    df["Time_corrected_activity, MBq"] = (
        df["Recorded activity, MBq"] *
        (2 ** (df["Time correction, Min"] / F18_DECAY))
    )

    start = df.loc[3, "Time_corrected_activity, MBq"]
    end = df.loc[10, "Time_corrected_activity, MBq"]

    rcy = (end / start) * 100
    return df, round(rcy, 1)


def main():
    results = []

    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".csv"):
            input_path = os.path.join(INPUT_FOLDER, filename)

            try:
                df, result = process_file(input_path)

                # Save processed CSV
                output_filename = filename.replace(".csv", "_calculated.csv")
                df.to_csv(os.path.join(OUTPUT_FOLDER, output_filename), index=False)

                # Store result
                results.append({
                    "file": filename,
                    "RCY_%": result
                })

                print(f"{filename} → RCY: {result}%")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Save summary CSV
    summary_path = os.path.join(OUTPUT_FOLDER, "RCY_summary.csv")
    pd.DataFrame(results).to_csv(summary_path, index=False)


if __name__ == "__main__":
    main()