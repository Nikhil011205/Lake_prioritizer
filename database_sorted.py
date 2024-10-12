import pandas as pd
import pymysql

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'water_conservation'
}

# CSV file path
csv_file_path = 'sorted.csv'

# Read CSV file into DataFrame
df = pd.read_csv(csv_file_path)

# Connect to the MySQL database
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Create table (modify the SQL according to your CSV file structure)
create_table_sql = "CREATE TABLE IF NOT EXISTS sorted_data (serial_num int(10),stn_code int(10),location varchar(200),fatal_index float(20));"
cursor.execute(create_table_sql)

# Insert DataFrame into MySQL table
for index, row in df.iterrows():
    # print(row)
    # quit()
    L = list(tuple(row))
    # print(L)
    # Construct SQL query (adjust the query to match your table schema)
    insert_sql = f'INSERT INTO sorted_data (serial_num, stn_code, location,fatal_index) VALUES ({L[1]}, {L[2]}, "{L[3]}",{L[4]});'
    # Execute the query
    cursor.execute(insert_sql)

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("Data inserted successfully!")