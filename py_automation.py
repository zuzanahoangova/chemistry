# import pandas as pd
# # pd.set_option('display.max_columns', None) # displays all columns
#
# # extracting tables from websites
# sunscreens = pd.read_html('https://en.wikipedia.org/wiki/Sunscreen') # this website gives weird tables
# print(len(sunscreens))
#
# simpsons = pd.read_html('https://en.wikipedia.org/wiki/List_of_The_Simpsons_episodes')
# print(simpsons[1])
#
# # extracting .csv from websites
# football = pd.read_csv('https://www.football-data.co.uk/mmz4281/2425/E0.csv')
#
# # extracting tables from pdf
# # packages tk, ghostscript and camelot-py needed
# import camelot
#
# tables = camelot.read_pdf('foo.pdf', pages='1', flavor='lattice')
# print(tables)
#
# tables.export('foo.csv', f='csv', compress=True)
# tables[0].to_csv('foo.csv')  # to a csv file
# print(tables[0].df_data)  # to a df
#
#
# # file manipulation
# with open('z41_1.dat', 'r') as file:
#     data = file.read()
#     data = data.replace(';', '\t')
#
# with open('z41_1.dat', 'w') as file:
#     file.write(data)
#
# ###
# import pandas as pd
# import matplotlib.pyplot as plt
#
# with open('z41_1.dat', 'r') as file:
#     data = file.readlines()
#
# with open('z41_1_para.dat', 'w') as file:
#     file.writelines(data[:182])
#
# with open('z41_1_data.dat', 'w') as file:
#     file.writelines(data[182:])
#
# df_para = pd.read_csv('z41_1_para.dat', sep=';', encoding='Latin-1')
# dicke = df_para.iloc[9, 3]
# breite = df_para.iloc[10, 3]
#
# df_data = pd.read_csv('z41_1_data.dat', sep='\t', encoding='Latin-1')
# df_data = df_data[["Load", "Strain(1)"]]

###
import pandas as pd
import matplotlib.pyplot as plt

df_data = pd.read_csv('zh4_1.dat', delimiter="\t", encoding='Latin-1', skiprows=182)
df_data = df_data.drop(index=0)
df_data = df_data[["Load", "Strain(1)"]]
for index, row in df_data.iterrows():
    if row["Load"] < 0:
        df_data = df_data.drop(index)
    else:
        break
df_data = df_data.iloc[:-2]
df_data = df_data.reset_index(drop=True)

df_para = pd.read_csv('zh4_1.dat', delimiter=";", encoding='Latin-1', nrows=15)
dicke = float(df_para.iloc[9, 3])
breite = float(df_para.iloc[10, 3])
df_data["Stress"] = df_data["Load"] / (dicke * breite)
l0 = df_data.iloc[0, 1]
df_data["Strain"] = (df_data["Strain(1)"] - l0) / df_data["Strain(1)"]*100

plt.plot(df_data["Strain"], df_data["Stress"], label='zh4_1')
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.title('zh4_1')
plt.legend()
plt.axis([0, 3.75, 0, 800])
output_file = 'zh4_1.png'
plt.savefig(output_file)
plt.close()
