import pandas as pd
import os
import matplotlib.pyplot as plt

folder_path = input("Enter folder path: ")
for file_name in os.listdir(folder_path):
    if file_name.endswith(".dat"):
        dat_file_path = os.path.join(folder_path, file_name)
        base_name = os.path.splitext(file_name)[0]
        try:
            df_data = pd.read_csv(dat_file_path, delimiter="\t", encoding='Latin-1', skiprows=182)
            df_data = df_data.drop(index=0)
            df_data = df_data[["Load", "Strain(1)"]]
            for index, row in df_data.iterrows():
                if row["Load"] < 0:
                    df_data = df_data.drop(index)
                else:
                    break
            df_data = df_data.iloc[:-2]
            df_data = df_data.reset_index(drop=True)

            df_para = pd.read_csv(dat_file_path, delimiter=";", encoding='Latin-1', nrows=15)
            dicke = float(df_para.iloc[9, 3])
            breite = float(df_para.iloc[10, 3])
            df_data["Stress"] = df_data["Load"]/(dicke*breite)
            l0 = df_data.iloc[0, 1]
            df_data["Strain"] = (df_data["Strain(1)"]-l0)/l0*100

            csv_file_path = os.path.join(folder_path, base_name + ".csv")
            df_data.to_csv(csv_file_path, index=False)

            plt.plot(df_data["Strain"], df_data["Stress"], label=base_name)
            plt.xlabel('Strain')
            plt.ylabel('Stress')
            plt.title(f'{base_name}')
            plt.legend()
            plt.axis([0, 3.75, 0, 800])
            output_file = os.path.join(folder_path, f'{base_name}.png')
            plt.savefig(output_file)
            plt.close()

            print(f"{base_name}.csv done")
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    else: print(f"{file_name} skip")

print("Conversion complete!")
