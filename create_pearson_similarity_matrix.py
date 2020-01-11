import numpy as np
print("numpy imported")
import pandas as pd
print("pandas imported")
import scipy.stats
print("scipy imported")
#import tensorflow as tf
#print("tensorflow imported")
import csv
print("csv imported")

'''
* Example data
*
* ten users: A-J, five technologies: L-P, four smes: W-Z
* Rating: 0-5
*
*   L, M, N, O, P, Q
*A, 5, 4, 0, 1, 3
*B, 0, 0, 1, 0, 5
*C, 1, 0, 4, 5, 0
*D, 0, 1, 2, 2, 5
*E, 4, 5, 0, 1, 4, 5
*F, 1, 2, 0, 0, 5
*G, 0, 2, 5, 4, 1
*H, 3, 5, 1, 0, 2
*I, 4, 4, 0, 1, 0, 4
*J, 1, 1, 3, 5, 2
*
'''

debug = 1

DATA_FILE = 'data/combined_rating_matrix.csv'
#SME_RATING_FILE = 'data/user-sme_rating_matrix.csv'
OUT_FILE = 'data/user-user_pearson_similarity_matrix.csv'


'''map to int including empty string
#
'''
def int_mine(n):
  if n == '':
    m = ''
  else:
    m = int(n)
  
  return m

''' Ingest Data
#
'''
def ingest_data(filename):
  names = []
  headers = []
  ratings_str = []
  ratings_int = []
  #open csv file
  with open(filename) as csvfile:
    datareader = csv.reader(csvfile)
    #create tech lsit
    headers = next(datareader) # get first row
    headers.pop(0) # remove first item ('Names')
    #create name and ratings list
    for row in datareader: #iterate through rest of file
      names.append(row[0]) # append first column to names list
      ratings_str.append(row[1:]) # append rest of row to ratings list
  #convert string to integer for ratings matrix - easier whay to do this???
  for x in ratings_str:
    ratings_int.append(list(map(int_mine, x)))
  #debug
  if debug >= 2:
    print("Names is: ", names)
    print("Names type is: ", type(names))
    print("headers is: ", headers)
    print("headers type is: ", type(headers))
    print("Ratings_str is: ", ratings_str)
    print("Ratings_str type is: ", type(ratings_str))
    print("Ratings_str is: ", ratings_int)
    print("Ratings_str type is: ", type(ratings_int))
    print("")
  
  return names, headers, ratings_int, ratings_str

'''omit missing data
#
'''
def omit_missing(vec_a, vec_b):
  if debug >= 2:
    print("(omit_missing) vec_a is: ", vec_a)
    print("(omit_missing) vec_a type is: ", type(vec_a))
    print("(omit_missing) vec_b is: ", vec_b)
    print("(omit_missing) vec_b type is: ", type(vec_b))
    print("")
  #check if vectors are same length
  if len(vec_a) != len(vec_b):
    print("Error omit_missing(): vectors must be same length")
  else:
    vec_a_o = vec_a
    vec_b_o = vec_b
    i = 0
    #loop through array
    while i < len(vec_a_o): 
      #debug
      if debug  >= 2:
        print(i, ": len = ", len(vec_a_o))
      #if index in vec_a_o is empty, drop index from both vectors
      if vec_a_o[i] == '':
        if debug >= 2:
          print("Omit_missing loop: ", i, " - start - vec_a_o is: ", vec_a_o, "len:", len(vec_a_o))
          print("(Omit_missing loop: ", i, " - start - vec_b_o is: ", vec_b_o, "len:", len(vec_b_o))
        del vec_a_o[i]
        #debug
        if debug >= 2:
          print("Omit_missing loop: ", i, " - del from a - vec_a_o is: ", vec_a_o, "len:", len(vec_a_o))
          print("(Omit_missing loop: ", i, " - del from a - vec_b_o is: ", vec_b_o, "len:", len(vec_b_o))
        del vec_b_o[i]
        #debug
        if debug >= 2:
          print("Omit_missing loop: ", i, " - del from b - vec_a_o is: ", vec_a_o, "len:", len(vec_a_o))
          print("(Omit_missing loop: ", i, " - del from b - vec_b_o is: ", vec_b_o, "len:", len(vec_b_o))
          print("")
      #if index in vec_b_o is empty, drop index from both vectors
      elif vec_b_o[i] == '':
        if debug >= 2:
          print("Omit_missing loop: ", i, " - start - vec_a_o is: ", vec_a_o, "len:", len(vec_a_o))
          print("(Omit_missing loop: ", i, " - start - vec_b_o is: ", vec_b_o, "len:", len(vec_b_o))
        del vec_a_o[i]
        #debug
        if debug >= 2:
          print("Omit_missing loop: ", i, " - del from a - vec_a_o is: ", vec_a_o, "len:", len(vec_a_o))
          print("(Omit_missing loop: ", i, " - del from a - vec_b_o is: ", vec_b_o, "len:", len(vec_b_o))
        del vec_b_o[i]
        #debug
        if debug >= 2:
          print("Omit_missing loop: ", i, " - del from b - vec_a_o is: ", vec_a_o, "len:", len(vec_a_o))
          print("(Omit_missing loop: ", i, " - del from b - vec_b_o is: ", vec_b_o, "len:", len(vec_b_o))
          print("")
      else:
        i += 1  
  #debug
  if debug >= 2:
    print("vec_a_o is: ", vec_a_o)
    print("vec_a_o type is: ", type(vec_a_o))
    print("vec_b_o is: ", vec_b_o)
    print("vec_b_o type is: ", type(vec_b_o))
    print("")
  
  return vec_a_o, vec_b_o

''' calculate Pearson co-efficient between two vectors
# returns 2d vector - first item i coefficient, second is p value????
'''
def pearson_correlation(vec_a, vec_b):
  #debug
  if debug >= 2:
    print("(pearson_correlation) vec_a is: ", vec_a)
    print("(pearson_correlation) vec_a type is: ", type(vec_a))
    print("(pearson_correlation) vec_b is: ", vec_b)
    print("(pearson_correlation) vec_b type is: ", type(vec_b))
    print("")
  #check if vectors are same length
  if len(vec_a) != len(vec_b):
    print("Error pearson_similarity(): vectors must be same length")
    print("vec_a is: ", vec_a)
    print("vec_a len is: ", len(vec_a))
    print("vec_b is: ", vec_b)
    print("vec_b len is: ", len(vec_b))
    exit()
  else:
    #omit missing values from arrays
    vec_a_o, vec_b_o = omit_missing(vec_a, vec_b)
    #calc similarity between the two vectors
    sim = scipy.stats.pearsonr(vec_a_o, vec_b_o)
    #debug
    if debug >= 2:
      print("sim is: ", sim)
      print("sim type is: ", type(sim))
      print("")
  
  return sim

''' Create matrix of user similarities based on ratings
# return 3d matrix:
#   1st dim: index == index of person A
#   2nd dim: index == index of person B
#   3rd dim: [[[person_a index, person_b index, pearson correlation, pearson p value]...]...]
'''
def calc_simlarities(matrix):
  x = len(matrix)
  sims = np.zeros((x,x,4))
  #iterate through matrix
  for i in range(x):
    for j in range(x):
      if debug >= 2:
        print("matrix[i] is: ", matrix[i])
        print("matrix[i] type is: ", type(matrix[i]))
        print("matrix[j] is: ", matrix[j])
        print("matrix[j] type is: ", type(matrix[j]))
        print("")
      #define new arrays - if reference matrix directly it causes issues
      vec_a = matrix[i][:]
      vec_b = matrix[j][:]
      #calc similarity
      sim = pearson_correlation(vec_a, vec_b)
      #debug
      if debug >= 2:
        print("sim ", i, "/", j, ": ", sim)
        print("sim type: ", type(sim))
        print("")
      #update sims matrix
      sims[i][j] = [int(i), int(j), sim[0], sim[1]]   
  #debug
  if debug >= 2:
        print("sims ", sims)
        print("sims type: ", type(sims))
        print("")
  
  return sims

''' Save sims to CSV file
# 
'''
def save_sims_to_csv(sims_matrix, people_list, filename):
  x = len(sims_matrix)
  y = len(sims_matrix[0])
  #open csv writer
  with open(filename, 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile)
    #create header row
    header = ['Names']
    for i in people_list:
      header.append(i)
    #debug header
    if debug >= 2:
      print("header: ", header)
    #write header row
    datawriter.writerow(header)
    for n in range(x):
      if debug >= 1:
        print("n: ", n)
      new_row = [people_list[n]]
      for m in range(y):
        if debug >= 2:
          print("m: ", m)
          print("sims_matrix[n][m][2]: ", sims_matrix[n][m][2])
        new_row.append(sims_matrix[n][m][2])
      datawriter.writerow(new_row)
  
  return 'FILE SAVED'


''' find the similarity between two people
#
'''  
def find_sim(sim_matrix, people_list, person_a, person_b):
  p_i_a = people_list.index(person_a)
  p_i_b = people_list.index(person_b)
  sim = sim_matrix[p_i_a][p_i_b]
  #debug
  if debug >= 2:
        print("sim ", a, "/", b, ": ", sim)
        print("sim type: ", type(sim))
        print("")
  
  return sim

''' Run functions
#
'''
names, headers, user_tech_ratings, user_tech_ratings_str = ingest_data(DATA_FILE)

sims_matrix = calc_simlarities(user_tech_ratings)

success = save_sims_to_csv(sims_matrix, names, OUT_FILE)
print(success)
