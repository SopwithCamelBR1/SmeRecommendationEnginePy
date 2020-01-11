'''
# Create dataset
'''
import csv
import random
import Mysql_functions as c_mysql
import pandas as pd


#input files
NAMESFILE = 'data/NAMES.csv'
USERSFILE = 'data/users.csv'
TECHFILE = 'data/technologies.csv'
PRELOADED_SMESFILE = 'data/pre-loaded-smes.csv'
#output files
NAME_TECH_MATRIX_FILE = 'data/user-tech_rating_matrix.csv'
NAME_SME_MATRIX_FILE = 'data/user-sme_rating_matrix.csv'
SME_TECH_MATRIX_FILE = 'data/user-tech_rating_matrix.csv'
COMBINED_FILE = 'data/combined_rating_matrix.csv'

'''Random data creation functions
*
'''
#rand role
def random_role():
  role = random.choice(['Architect', 'Project Manager', 'Software Tester', 'Product Manager', 'Software Engineer', 'Software Engineer', 'Software Engineer'])
  
  return role
#rand desk
def random_desk():
  desk = "Desk "
  num = random.randint(1,255)
  desk = desk + str(num)
  
  return desk
#rand area
def random_area():
  floor = random.randint(1,4)
  sect = random.randint(1,4)
  area = "@Phoenix " + str(floor) + "." + str(sect) + " - " + random_desk()
  #print(area)
  
  return area
#rand tele 
def random_tele():
  tele = "555 "
  ext = random.randint(12000,17000)
  tele = tele + str(ext)
  #print(tele)
  
  return tele
#rand email
def create_email(name):
  email = str(name[0]) + "." + str(name[1]) + "@capgemini.com"
  
  return email
#rand custom group
def rand_group():
  group = random.choice(['A','B','C','D'])
  
  return group


  
'''Take the preloaded NAMES.csv and turn it into fully popuated csv/table
*
'''
def create_users_csv(names, outfile, debug=1):
  with open(outfile, 'w', newline='') as csvfile:
    if debug >= 2:
        print("names: ", names)
    datawriter = csv.writer(csvfile)
    headers = ['firstname', 'surname', 'userRole', 'userLocation', 'userDeskLocation', 'email', 'phone', 'CustomGroup']
    datawriter.writerow(headers)
    for name in names:
      if debug >= 2:
        print("name: ", name)
        print("name type: ", type(name))        
      #create row
      row=[]
      row.extend(name)
      if debug >= 2:
        print("row: ", row)
      row.append(random_role())
      row.append("UK-TEF-TELFORD")
      row.append(random_area())
      row.append(create_email(name))
      row.append(random_tele())
      row.append(rand_group())
      #write row
      datawriter.writerow(row)

  print("FILE CREATED")
  
  return None

'''Add pre-loaded smes to end of users csv
*
'''
def add_sme_csv(smefile, outfile, debug=1):
  with open(outfile,'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile)
    with open(smefile) as smecsvfile:
      datareader = csv.reader(smecsvfile)
      headers = next(datareader)
      for row in datareader:
        datawriter.writerow(row)

  print("FILE CREATED")
  
  return None  

''' GET a list of names from csv file
# TODO: need to catch empty row in csv
'''
def get_list_names(namefile, debug=1):
  #create empty list
  names=[]
  #open csv file
  with open(namefile) as csvfile:
    namereader = csv.reader(csvfile)
    #skip header
    next(namereader)
    #iterate through rows in csv file
    for row in namereader:
      #check if full row
      if len(row) >= 8:
         #debug
        if debug >= 2:
          print("Row: ", row)
          print("Row type: ", type(row))
          print("Row len: ", len(row))
          print("Row[5] (email): ", row[5])
          print("Row[7] (group): ", row[7])
        #append first item in row to list
        names.append([row[5],row[7]])
      # otherwise just use first item (pulling from NAMES.csv)
      else:
         #debug
        if debug >= 2:
          print("Row: ", row)
          print("Row type: ", type(row))
          print("Row len: ", len(row))
          print("Row[0] (Name): ", row[0])
          print("Row[0] type: ", type(row[0]))
        #append first item in row to list
        name = row[0].split()
        if debug >= 2:
          print("name: ", name)
        names.append(name)
  #debug
  if debug >= 2:
    print("Names: ", names)
    print("names type: ", type(names))
  
  return names

''' GET a list of technologies from csv file
# TODO: need to catch empty row in csv
'''
def get_list_techs(techfile, debug=1):
  #create empty list
  techs=[]
  #open csv file
  with open(techfile) as csvfile:
    techreader = csv.reader(csvfile)
    #skip header
    next(techreader)
    #iterate through rows in csv file
    for row in techreader:
      #debug
      if debug >= 2:
        print("Row: ", row)
        print("Row type: ", type(row))
        print("Row[0] (Tech): ", row[0])
        print("Row[0] type: ", type(row[0]))
      #append first item in row to list
      techs.append([row[0],row[3]])
  #debug
  if debug >= 2:
    print("Techs: ", techs)
    print("Techs type: ", type(techs))
  
  return techs



''' Create a rating for each technology given a particular role
'''
def create_rating(x_item, y_item, debug=1):
  if debug >= 2:
    print("Create_rating:")
    print("x_item: ", x_item)
    print("y_item: ", y_item)
  #check if roles are same
  if x_item[1] == y_item[1]:
    if debug >= 2:
      print("Same group")
    rating = random.choice([3,4,4,4,5,''])
  else:
    if debug >= 2:
      print("different group") 
    rating = random.choice([1,2,2,2,3,''])
  #debug
  if debug >= 2:
    print("rating: ", rating)
    
  return rating

''' Create a rating for each technology for a name
*
'''  
def create_ratings_list(x_item, y_list, debug=1):
  if debug >=2:
    print("Create_rating_list:")
    print("x_item: ", x_item)
    print("y_list: ", y_list)
  #intialise string and list
  ratings_str = x_item[0]
  ratings_ls = [ratings_str]
  #append rating for each tech to string and list
  for i in y_list:
    if debug >=2:
      print("Create_rating_list for loop:")
      print("x_item: ", x_item)
      print("i: ", i)
    rating = create_rating(x_item, i, debug=debug)
    ratings_str += ", " + str(rating)
    ratings_ls.append(rating)
  #debug
  if debug >= 2:
    print("ratings_str: ", ratings_str)
    print("ratings_ls: ", ratings_ls)
  return ratings_str, ratings_ls


''' Create matrix and save to csv file
# 
'''
def create_matrix(x_title, x_list, y_list, outfile, debug=1):
  with open(outfile, 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile)
    #create header row list
    header_ls = [x_title]
    for j in y_list:
      header_ls.append(j[0])
    #debug header_ls
    if debug >= 2:
      print("header_ls: ", header_ls)
    # write header to file
    datawriter.writerow(header_ls)
    # write data
    for i in x_list:
      nn, d_row = create_ratings_list(i, y_list, debug=debug)
      #debug d_row
      if debug >= 2:
        print("d_row: ", d_row)
      datawriter.writerow(d_row)
      
''' Ingest Data
#
'''
def combine_csv(file1, file2, mergeColumn, outfile, debug=1):
  names = []
  headers = []
  ratings_str = []
  ratings_int = []
  #open file1
  file1_dat = pd.read_csv(file1, sep=',')
  if debug >= 2:
    print(file1_dat.head())
    print(file1_dat.tail())
    print(len(file1_dat))
    print("")
  #import file2
  file2_dat = pd.read_csv(file2, sep=',')
  if debug >= 2:
    print(file2_dat.head())
    print(file2_dat.tail())
    print(len(file2_dat))
    print("")
  merged_dat = file1_dat.merge(file2_dat, on=mergeColumn)
  if debug >= 2:
    print(merged_dat.head())
    print("")
  merged_dat.to_csv(outfile, index=False)
  
  print("CSVs combined")
  
  return None
      
 
''' Run Code
#
'''
#create names csv
# Create smes.csv
names = get_list_names(NAMESFILE)
create_users_csv(names, USERSFILE)
add_sme_csv(PRELOADED_SMESFILE, USERSFILE)
# get name, tech, and sme lists
names_ls = get_list_names(USERSFILE)
tech_ls = get_list_techs(TECHFILE)
sme_ls = get_list_names(PRELOADED_SMESFILE)
#create csv's
create_matrix('Names', names_ls, tech_ls, NAME_TECH_MATRIX_FILE)
create_matrix('Names', names_ls, sme_ls, NAME_SME_MATRIX_FILE)
combine_csv(NAME_TECH_MATRIX_FILE, NAME_SME_MATRIX_FILE, 'Names', COMBINED_FILE)

