import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv
from Plot_AQI import avg_data  # Importing the optimized function

def met_data(month, year):
    """Extract meteorological data from HTML files."""
    file_path = f'Data/Html_Data/{year}/{month}.html'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'rb') as file_html:
        plain_text = file_html.read()
    
    soup = BeautifulSoup(plain_text, "lxml")
    tempD, finalD = [], []

    for table in soup.find_all('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                tempD.append(tr.get_text())
    
    # Reshape into 15-column rows
    rows = len(tempD) // 15
    finalD = [tempD[i * 15:(i + 1) * 15] for i in range(rows)]
    
    if finalD:
        finalD.pop(-1)  # Remove last row
        finalD.pop(0)   # Remove header row
    
        # Remove unnecessary columns
        for row in finalD:
            for index in [6, 13, 12, 11, 10, 9, 0]:
                del row[index]
    
    return finalD

def data_combine(year, chunk_size=600):
    """Combine real data from CSV files."""
    data = []
    file_path = f'Data/Real-Data/real_{year}.csv'
    if os.path.exists(file_path):
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            data.extend(chunk.values.tolist())
    return data

if __name__ == "__main__":
    os.makedirs("Data/Real-Data", exist_ok=True)
    
    for year in range(2013, 2017):
        final_data = []
        
        with open(f'Data/Real-Data/real_{year}.csv', 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM2.5'])
        
        for month in range(1, 13):
            final_data.extend(met_data(month, year))
        
        pm_values = avg_data(year)
        # if len(pm_values) == 364:
        #     pm_values.insert(364, '-')
        while len(pm_values) < len(final_data):
            pm_values.append('-')
        
        for i in range(len(final_data)):
            final_data[i].append(pm_values[i])
        
        with open(f'Data/Real-Data/real_{year}.csv', 'a', newline='') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerows([row for row in final_data if '-' not in row and "" not in row])
    
    # Combine all years
    total_data = sum([data_combine(year) for year in range(2013, 2017)], [])
    
    with open('Data/Real-Data/Real_Combine.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM2.5'])
        wr.writerows(total_data)
    
    df = pd.read_csv('Data/Real-Data/Real_Combine.csv')
