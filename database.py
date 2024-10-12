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
csv_file_path = 'synthetic_water_quality_data_bengaluru.csv'

# Read CSV file into DataFrame
df = pd.read_csv(csv_file_path)

# Connect to the MySQL database
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Create table (modify the SQL according to your CSV file structure)
create_table_sql = "CREATE TABLE IF NOT EXISTS raw_data (serial_num int(10),stn_code int(10),location varchar(200),dissolved_o2 float(20), ph float(20),conductivity float(20),bod float(20), f_level float(20), b_level float(20),ca_level float(20), phosp_level float(20),na_level float(20), nh3_level float(20), carb float(20), bicarb float(20),cod float(20), turbidity float(20),useful float(20), clean int(2));"
cursor.execute(create_table_sql)

# Insert DataFrame into MySQL table
for index, row in df.iterrows():
    # print(row)
    # quit()
    L = list(tuple(row))
    # print(L)
    # Construct SQL query (adjust the query to match your table schema)
    insert_sql = f'INSERT INTO raw_data (serial_num, stn_code, location,dissolved_o2,ph,conductivity,bod,f_level,b_level,ca_level,phosp_level,na_level,nh3_level,carb,bicarb,cod,turbidity,useful,clean) VALUES ({L[0]}, {L[1]}, "{L[2]}",{L[3]},{L[4]},{L[5]},{L[6]},{L[7]},{L[8]},{L[9]},{L[10]},{L[11]},{L[12]},{L[13]},{L[14]},{L[15]},{L[16]},{L[17]},{L[18]});'
    # Execute the query
    cursor.execute(insert_sql)

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("Data inserted successfully!")