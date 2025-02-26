# import pandas as pd

# data = pd.read_csv(r"C:\Users\ADMIN\Desktop\ADY data\Crawler.index\data\raw\Core_Inlation.csv", dtype=str)

# print(data.iloc[0])

#================================================================================
# fileLink = r"C:\Users\ADMIN\Desktop\ADY data\Crawler.index\data\raw\Brent1.csv"

# data = open(fileLink, "r").readlines()
# for i in range(len(data)): 
#     data[i] = data[i][1:-2] + '\n'

# with open(fileLink, "w", encoding="utf-8") as file:
#     file.writelines(data) 
#================================================================================


fileLink = r"C:\Users\ADMIN\Desktop\ADY data\Crawler.index\data\raw\USD_VND.csv"
# output = r"C:\Users\ADMIN\Desktop\ADY data\Crawler.index\data\raw\Brent.csv"

data = open(fileLink, "r", encoding="utf-8").readlines()
print(data[0])

for i in range(len(data)):
    data[i] = data[i].split(',')
    for j in range(len(data[i])):
        data[i][j] = data[i][j][1:-1]
        if j == len(data[i]) - 1: data[i][j] = data[i][j][:-1]

for i in range(len(data)): 
    # print(','.join(data[i]))
    data[i] = ','.join(data[i])

with open(fileLink, "w", encoding="utf-8") as file:
    file.writelines('\n'.join(data)) 



# for i in range(len(data)): 
    # data[i] = data[i][1:-2] + '\n'

# for x in range(10): print(data)

# with open(fileLink, "w", encoding="utf-8") as file:
#     file.writelines(data) 