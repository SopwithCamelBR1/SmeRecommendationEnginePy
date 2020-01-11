''' Load data into SQL
*
'''
import csv
import pymysql
import warnings
warnings.filterwarnings('ignore')

DATAFILE="smes.csv"

''' Connect to Database
*
'''
def mysql_connect(h, p, u, pw, d_b, ct='utf8mb4', debug=1):  
  conn = pymysql.connect(
            host=h,
            port=int(p),
            user=u,
            passwd=pw,
            db=d_b,
            charset=ct)
  print("Connected.") 
  
  return conn 
  
  return conn
''' Close Connection to Database
*
'''  
def mysql_close(conn, debug=1):  
  conn.close() 
  print("Connection Closed.") 

  return None
  
'''get_table
*
'''
def get_table(conn, table, debug=1):
  cursor = conn.cursor()
  sql = "SELECT * FROM " + table
  number_of_rows = cursor.execute(sql) 
  rows = cursor.fetchall()
  if debug >= 2:
    print("number results: ", number_of_rows)
    for i in range (number_of_rows):
      print (rows[i])
      
  return rows

'''get_column
*
'''
def get_column(conn, table, column, debug=1):
  cursor = conn.cursor()
  sql = "SELECT " + column + " FROM " + table
  number_of_rows = cursor.execute(sql) 
  rows = cursor.fetchall()
  if debug >= 2:
    print("number results: ", number_of_rows)
    for i in range (number_of_rows):
      print (rows[i])
      
  return rows

'''get_row
*
'''
def get_rows(conn, table, id_column, id, debug=1):
  cursor = conn.cursor()
  sql = "SELECT * FROM " + table + " WHERE " + id_column + " ='" + id + "'"
  number_of_rows = cursor.execute(sql) 
  rows = cursor.fetchall()
  if debug >= 2:
    print("number results: ", number_of_rows)
    for i in range (number_of_rows):
      print (rows[i])
      
  return rows

'''get_values
*
'''
def get_values(conn, table, value_column, id_column, id, debug=1):
  cursor = conn.cursor()
  sql = "SELECT "+ value_column + " FROM " + table + " WHERE " + id_column + " ='" + id + "'"
  number_of_rows = cursor.execute(sql) 
  rows = cursor.fetchall()
  if debug >= 2:
    print("number results: ", number_of_rows)
    for i in range (number_of_rows):
      print (rows[i], "; type: ", type(rows[i]))
      
      
  return rows

'''insert_row
*
'''
def insert_row(conn, table, headers, row, debug=1):
  #check headers and rows are as long as each other
  if len(headers) != len(row):
    print("ERROR - headers and row must be same length")
    exit()
  else:
    cursor = conn.cursor()
    #create sql string
    sql = "INSERT INTO " + table + " ("
    #headers
    if debug >= 2:
      print(headers)
    for i in range(len(headers)):
      if i == len(headers)-1:
        sql = sql + headers[i] + ") VALUES ("
      else: 
        sql = sql + headers[i] + ", " 
      if debug >= 2:
        print(sql)
    #rows
    if debug >= 2:
      print(row)
    for i in range(len(row)):
      if i == len(row)-1:
        sql = sql + "'"  + row[i] + "');"
      else: 
        sql = sql + "'"  + row[i] + "', "
      if debug >= 2:
        print(sql)
    #debug
    if debug >=2:    
      print("sql: ", sql)
    #execute sql
    cursor.execute(sql)
    conn.commit()
  
  if debug >=2:
    print("Row Inserted")
    
  return None

'''insert_from_csv
*
'''
def insert_from_csv(datafile, conn, table, debug=1):
  #open csvfile
  with open(datafile) as csvfile:
    rowreader = csv.reader(csvfile)
    #get headers
    headers = next(rowreader, None)
    if debug >= 2:
      print("headers: ", headers)
      print("headers length: ", len(headers))  
    #iterate through rows in csv file
    for row in rowreader:
      if debug >= 2:
        print("row: ", row)
        print("row length: ", len(row))
      insert_row(conn, table, headers, row)
  
  if debug >=1:
    print("Rows Inserted!")
  
  return None
  
'''delete_row
*
'''
def delete_row(conn, table, id_column, id, debug=1):
  cursor = conn.cursor()
  #create sql string
  sql = "DELETE FROM " + table + " WHERE " + id_column + " ='" + id + "'" 
  #debug
  if debug >=2:    
    print("sql: ", sql)
  #execute sql
  cursor.execute(sql)
  conn.commit()
  
  print("Row Deleted")
  
  return None

'''delete_all_rows
*
'''
def delete_all_rows(conn, table, reset_aut_inc=0, debug=1):
  cursor = conn.cursor()
  sql = "DELETE FROM " + table
  cursor.execute(sql) 
  #debug
  if debug >= 1:
    print("All Rows Deleted from ", table)
  if reset_aut_inc == 1:
    reset_sql = "ALTER TABLE " + table + " AUTO_INCREMENT = 1"
    cursor.execute(reset_sql)
    if debug >= 1:
      print("Auto-incrementer set to 1 ", table)
  
  conn.commit()
    
  return None
  
  



'''download_table_to_csv
*
'''
def download_table_to_csv(conn, table, outfile, debug=1):
  cursor = conn.cursor()
  sql = "SELECT * FROM " + table
  cursor.execute(sql) 
  if debug >= 2:
    print(cursor)
  with open(outfile, "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) # write headers
    csv_writer.writerows(cursor)
  
  print("CSV CREATED")
  
  return None