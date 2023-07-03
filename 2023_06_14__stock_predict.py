

# from zmq.constants import NULL

import pandas as pd
import yfinance as yf
from datetime import datetime

# Mount Google Drive

# Define your stock list
stock_list = [ 'AAPL' , 'GOOGL', 'MSFT']

# csv_path = '/content/drive/MyDrive/stock_predict/stock_data_hist.csv'
csv_path = 'stock_data_hist.csv'


# # Set the start and end dates
# start_date = '2023-04-01'
# end_date = '2023-06-01'

# combined_data = []

# for stock in stock_list:
#   data = []
#   # Retrieve data from Yahoo Finance for the defined time period
#   data = yf.download(stock, start=start_date, end=end_date)

#   # Reset the index to make 'Date' a column
#   data = data.reset_index()

#   # Add the 'Stock' column to identify each stock
#   data['Stock'] = stock

#Print 123

#   # Keep only the required columns
#   data = data[['Stock', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

#   if len(combined_data) == 0:
#     combined_data = data
#   else:
#     combined_data = pd.concat([combined_data, data])

# combined_data.to_csv(csv_path,index=False)

df = pd.read_csv(csv_path, index_col='Date', parse_dates=True)

df = df.reset_index()
df['Date'] = pd.to_datetime(df['Date'])

# # Check the latest date for each stock in the CSV file
latest_dates = df.groupby('Stock')['Date'].max()

df_column_order = df.columns.values

# Retrieve data from Yahoo Finance for each stock from the latest date to the current date
for stock in stock_list:
    latest_date = latest_dates.get(stock, pd.Timestamp(1900, 1, 1))
    latest_date_str = latest_date.strftime('%Y-%m-%d')
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Retrieve the data from Yahoo Finance
    stock_data = yf.download(stock, start=latest_date_str, end=current_date)

    stock_data = stock_data.reset_index()

    # Append the new data to the existing DataFrame
    if not stock_data.empty:
        stock_data['Stock'] = stock

        # print(stock_data.columns.values)
        # print(df_column_order)
        # print(stock_data)
        stock_data = stock_data[['Date','Stock','Open','High','Low','Close','Volume']]
        print(stock_data.head())

        # print(df.append(stock_data))


        df = pd.concat([df, stock_data])
print(df)
# Save the updated DataFrame to the CSV file
df.to_csv(csv_path, index = False)

# csv_path = '/content/drive/MyDrive/stock_predict/stock_data_hist.csv'
# df = pd.read_csv(csv_path, error_bad_lines=False)

# print(df)

