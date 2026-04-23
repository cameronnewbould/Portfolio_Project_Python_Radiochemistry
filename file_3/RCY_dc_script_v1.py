import os
import pandas as pd

# Constants
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
F18_DECAY = 109.77

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_file(file_path):
    df = pd.read_csv(file_path)

    # Add calculated column
    df["Time_corrected_activity, MBq"] = (
        df["Recorded activity, MBq"] *
        (2 ** (df["Time correction, Min"] / F18_DECAY))
    )

    # Calculate RCY
    start = df.loc[3, "Time_corrected_activity, MBq"]
    end = df.loc[10, "Time_corrected_activity, MBq"]

    rcy = (end / start) * 100
    rounded_rcy_dc = round(rcy, 1)

    return df, rounded_rcy_dc


def main():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".csv"):
            input_path = os.path.join(INPUT_FOLDER, filename)

            try:
                df, result = process_file(input_path)

                # Save output file
                output_filename = filename.replace(".csv", "_calculated.csv")
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                df.to_csv(output_path, index=False)

                print(f"{filename} → RCY: {result}%")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()