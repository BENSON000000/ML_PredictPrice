import os
import pandas as pd


data_dir = r'C:\informer\Informer2020\data\TaiwanFutures'
df_list = []

for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)
        df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)


combined_df['Date'] = pd.to_datetime(combined_df['Date'])
combined_df = combined_df.sort_values('Date').reset_index(drop=True)


total_len = len(combined_df)
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

train_end = int(total_len * train_ratio)
val_end = train_end + int(total_len * val_ratio)

train_df = combined_df.iloc[:train_end]
val_df = combined_df.iloc[train_end:val_end]
test_df = combined_df.iloc[val_end:]


output_dir = r'C:\informer\Informer2020\data\TaiwanFutures_Split'
os.makedirs(output_dir, exist_ok=True)

train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
val_df.to_csv(os.path.join(output_dir, 'val.csv'), index=False)
test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)
