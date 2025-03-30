import pandas as pd
import matplotlib.pyplot as plt

def avg_data(year):
    """Calculate the daily average PM2.5 for a given year."""
    average = []
    file_path = f'Data/AQI/aqi{year}.csv'
    
    # Read the file in chunks of 24 rows (representing 24 hours)
    for rows in pd.read_csv(file_path, chunksize=24):
        df = pd.DataFrame(rows)
        
        # Convert PM2.5 values to numeric, coerce errors to NaN
        df["PM2.5"] = pd.to_numeric(df["PM2.5"], errors='coerce')

        # Compute daily average, ignoring NaN values
        avg = df["PM2.5"].mean()
        average.append(avg)
    
    return average

if __name__ == "__main__":
    years = [2013, 2014, 2015, 2016]  # Add more years if needed
    data = {year: avg_data(year) for year in years}
    
    # Plotting the data
    for year in years:
        plt.plot(range(len(data[year])), data[year], label=f"{year} data")

    plt.xlabel('Day')
    plt.ylabel('PM 2.5')
    plt.legend(loc='upper right')
    plt.show()
