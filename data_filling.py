import numpy as np
import os
import pandas as pd

def find_missing_rows(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    time_diffs = df['Date'].diff()
    one_minute = pd.Timedelta(minutes=1)
    missing_rows = []

    i = 1
    while i < len(time_diffs):
        time_diff = time_diffs.iloc[i]
        if time_diff != one_minute:
            missing_minutes = int(time_diff.total_seconds() // 60) - 1
            start_time = df['Date'].iloc[i - 1] + one_minute
            start_index = i + len(missing_rows)
            num_missing = missing_minutes

            missing_rows.append({
                'start_index': start_index,
                'start_time': start_time,
                'num_missing': num_missing
            })

            i += 1  
        else:
            i += 1  
    if missing_rows:
        print(missing_rows)

    return missing_rows

def fill_missing_values(df, missing_rows):

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
  
    for missing_row in missing_rows:
        start_index = missing_row['start_index']
        start_time = missing_row['start_time']
        num_missing = missing_row['num_missing']
        

        missing_times = [start_time + pd.Timedelta(minutes=m) for m in range(num_missing)]
        

        missing_data = pd.DataFrame({
            'Date': missing_times,
            'Open': [np.nan]*num_missing,
            'High': [np.nan]*num_missing,
            'Low': [np.nan]*num_missing,
            'Close': [np.nan]*num_missing,
            'Volume': [np.nan]*num_missing
        })
        

        df = pd.concat([df.iloc[:start_index], missing_data, df.iloc[start_index:]]).reset_index(drop=True)
    

    df = df.sort_values('Date').reset_index(drop=True)
    

    df['Open'] = df['Open'].astype(float)
    df['Open'] = df['Open'].ffill()
    df['Open'] = df['Open'].bfill().interpolate()
    

    df['Close'] = df['Close'].astype(float)
    df['Close'] = df['Close'].bfill()
    df['Close'] = df['Close'].ffill().interpolate()
    
  
    df['High'] = df['High'].astype(float).interpolate()
    df['Low'] = df['Low'].astype(float).interpolate()
    
    
    df['High'] = df[['High', 'Open', 'Close']].max(axis=1)
    df['Low'] = df[['Low', 'Open', 'Close']].min(axis=1)
    

    df['Price_Range'] = df['High'] - df['Low']
    valid = df['Volume'].notna() & df['Price_Range'].notna() & (df['Price_Range'] > 0)
    avg_volume_per_range = (df.loc[valid, 'Volume'] / df.loc[valid, 'Price_Range']).mean()
    
    for i in df[df['Volume'].isna()].index:
        price_range = df.at[i, 'Price_Range']
        if not np.isnan(price_range) and price_range > 0:
            df.at[i, 'Volume'] = avg_volume_per_range * price_range
        else:
            df.at[i, 'Volume'] = df['Volume'].mean()
    
    df.drop(columns='Price_Range', inplace=True)
    
    return df

def process_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            missing_rows = find_missing_rows(df)
            df = fill_missing_values(df, missing_rows)
            df.to_csv(file_path, index=False)

folder_path = r"C:\informer\Informer2020\data\TaiwanFutures"
process_files(folder_path) 
