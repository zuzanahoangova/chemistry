import pandas as pd
import os

def rename_tensile():
    try:
        input_file = input("Enter the input CSV file path: ")
        data = pd.read_csv(input_file)

        data = data.replace("zh1", "FeCu", regex=True)
        data = data.replace("zh2", "CrA_0.60C", regex=True)
        data = data.replace("zh5", "CrA_0.65C", regex=True)
        data = data.replace("zh6", "CrA_0.70C", regex=True)
        data = data.replace("zh3", "CrS_0.60C", regex=True)
        data = data.replace("zh7", "CrS_0.65C", regex=True)
        data = data.replace("zh8", "CrS_0.70C", regex=True)
        data = data.replace("zh4", "CrS-MA_1140", regex=True)
        data = data.replace("z41", "CrS-MA_1200", regex=True)
        data = data.replace("z42", "CrS-MA_1250", regex=True)

        base_name, extension = os.path.splitext(input_file)
        output_file = f"{base_name}_renamed{extension}"

        data.to_csv(output_file, index=False)
        print(f"rename for {input_file} complete")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    rename_tensile()