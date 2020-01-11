import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import scipy.stats
import tensorflow as tf
import csv
import warnings
warnings.filterwarnings('ignore')

'''
* Example data
*
'''

debug = 1

DATA_FILE_TECH = 'data/user-tech_rating_matrix.csv'
DATA_FILE_SME = 'data/user-sme_rating_matrix.csv'
OUT_FILE_TECH = 'data/user-tech_RBM_predicted_ratings_matrix.csv'
OUT_FILE_SME = 'data/user-sme_RBM_predicted_ratings_matrix.csv'


def int_mine(n):
  if n == '':
    m = 0.5
  else:
    m = int(n)/5
  
  return m

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

'''Creating training set
#
'''
def create_train_set(ratings_dat, n_percent):
  number = int(len(ratings_dat)*n_percent)
  if debug >= 1:
    print("Using ", number, " datapoints")
  trX = []
  for i in range(number):
    trX.append(ratings_dat[i])
    if debug >= 2:
      print(trX)
      print(len(trX))
    
  return trX

''' Defining RBM model & Training
#
'''
def RBM_model(visible_units, hidden_units, learning_rate):
  #bias & weights
  vb = tf.placeholder('float', [visible_units])
  hb = tf.placeholder('float', [hidden_units])
  w = tf.placeholder('float', [visible_units, hidden_units])
  #Phase 1 - input processing
  v0 = tf.placeholder('float', [None, visible_units])
  _h0 = tf.nn.sigmoid(tf.matmul(v0, w) + hb)
  h0 = tf.nn.relu(tf.sign(_h0 - tf.random_uniform(tf.shape(_h0))))
  #Phase 2 - Reconstruction
  _v1 = tf.nn.sigmoid(tf.matmul(h0, tf.transpose(w)) + vb)
  v1 = tf.nn.relu(tf.sign(_v1 - tf.random_uniform(tf.shape(_v1))))
  h1 = tf.nn.sigmoid(tf.matmul(v1, w) + hb)
  # Create gradients
  w_pos_grad = tf.matmul(tf.transpose(v0), h0)
  w_neg_grad = tf.matmul(tf.transpose(v1), h1)
  # Calculate Contrastive Divergence to maximise
  CD = (w_pos_grad - w_neg_grad) / tf.to_float(tf.shape(v0)[0])
  # Create methods to update the weights and biases
  update_w = w + learning_rate * CD
  update_vb = vb + learning_rate * tf.reduce_mean(v0 - v1, 0)
  update_hb = hb + learning_rate * tf.reduce_mean(h0 - h1, 0)
  # Mean absolute Error Function
  err = v0 - v1
  err_sum = tf.reduce_mean(err * err)
  
  return vb, hb, w, v0, _h0, h0, _v1, v1, h1, CD, update_w, update_vb, update_hb, err_sum

def recommendations(filename, names, ratings, technologies, weights, h_bias, v_bias):
  # check names and ratings smae length
  if len(names) != len(ratings):
    print("Error!")
  else:
    with open(filename, 'w', newline='') as csvfile:
      datawriter = csv.writer(csvfile)
      #create header row
      header = ['Names']
      for i in technologies:
        header.append(i)
      #debug header
      if debug >= 2:
        print("header: ", header)
      #write header row
      datawriter.writerow(header)
      #create recs
      for i in range(len(names)):
        if debug >= 2:
          print("len(names): ", len(names))
          print("creating csv row: ", i)
        new_row = [names[i]]
        if debug >= 2:
          print("new_row: ", new_row)
        #inputUser = [trX[75]]
        hh0 = tf.nn.sigmoid(tf.matmul(v0, w) + hb)
        vv1 = tf.sigmoid(tf.matmul(hh0, tf.transpose(w)) + vb)
        feed = sess.run(hh0, feed_dict={v0: [ratings[i]], w: weights, hb: h_bias})
        rec = sess.run(vv1, feed_dict={hh0: feed, w: weights, vb: v_bias})
        rec_row = rec[0].tolist()
        if debug >= 2:
          print("rec_row: ", rec_row)
        new_row.extend(rec_row)
        if debug >= 2:
          print("new_row after rec: ", new_row)
        datawriter.writerow(new_row)
    
    print("FILE CREATED")



''' RUN FUNCTIONS for TECH predictions
*
'''
#import_data
names, technologies, ratings_int, ratings_str = ingest_data(DATA_FILE_TECH)
trX = create_train_set(ratings_int, 1)

#create model & training algorithms
v_u = len(technologies)
h_u = 10
learning_rate = 0.1
vb, hb, w, v0, _h0, h0, _v1, v1, h1, CD, ud_w, ud_vb, ud_hb, err_sum = RBM_model(v_u, h_u, learning_rate)

#run model
with tf.Session() as sess:
  
  # Intialise starting variable - do this in tensroflow mebbe?
  cur_w = np.zeros([v_u, h_u], np.float32)
  cur_vb = np.zeros([v_u], np.float32)
  cur_hb = np.zeros([h_u], np.float32)
  prev_w = np.zeros([v_u, h_u], np.float32)
  prev_vb = np.zeros([v_u], np.float32)
  prev_hb = np.zeros([h_u], np.float32)
  #intialise tf variables  
  sess.run(tf.global_variables_initializer())
  #run training
  epochs = 5
  batchsize = 100
  errors = []
  print("Training Tech Predictions")
  for i in range(epochs):
    b_n = 0
    for start, end in zip(range(0, len(trX), batchsize), range(batchsize, len(trX), batchsize)):
      if debug >= 2:
        print("start: ", start)
        print("end: ", end)
      batch = trX[start:end]
      if debug >= 2:
        print("len(batch): ", len(batch))
        print("len(batch[0]): ", len(batch[0]))
        print("batch[0][:10]: ", batch[0][:10])
      cur_w = sess.run(ud_w, feed_dict={v0: batch, w: prev_w, vb: prev_vb, hb: prev_hb})
      cur_vb = sess.run(ud_vb, feed_dict={v0: batch, w: prev_w, vb: prev_vb, hb: prev_hb})
      cur_hb = sess.run(ud_hb, feed_dict={v0: batch, w: prev_w, vb: prev_vb, hb: prev_hb})
      prev_w = cur_w
      prev_vb = cur_vb
      prev_hb = cur_hb
      if debug >= 1:
        batch_error = sess.run(err_sum, feed_dict={v0: batch, w: cur_w, vb: cur_vb, hb: cur_hb})
        print("Epoch/Batch: ", i, "/", b_n, " : Error = ", batch_error)
        print
        b_n += 1
    errors.append(batch_error)
  #plot error
  if debug >= 1:
    plt.plot(errors)
    plt.ylabel('Error')
    plt.xlabel('Epoch')
    plt.show()

  
  recommendations(OUT_FILE_TECH, names, ratings_int, technologies, prev_w, prev_hb, prev_vb)


''' Run functions for SME predictions
*
'''
#import_data
names, smes, ratings_int, ratings_str = ingest_data(DATA_FILE_SME)
#create training set
trX = create_train_set(ratings_int, 1)

#create model & training algorithms
v_u = len(smes)
h_u = 10
learning_rate = 0.1
vb, hb, w, v0, _h0, h0, _v1, v1, h1, CD, ud_w, ud_vb, ud_hb, err_sum = RBM_model(v_u, h_u, learning_rate)

#run model
with tf.Session() as sess:
  
  # Intialise starting variable - do this in tensroflow mebbe?
  cur_w = np.zeros([v_u, h_u], np.float32)
  cur_vb = np.zeros([v_u], np.float32)
  cur_hb = np.zeros([h_u], np.float32)
  prev_w = np.zeros([v_u, h_u], np.float32)
  prev_vb = np.zeros([v_u], np.float32)
  prev_hb = np.zeros([h_u], np.float32)
  #intialise tf variables  
  sess.run(tf.global_variables_initializer())
  #run training
  epochs = 5
  batchsize = 100
  errors = []
  print("Training SME Predictions")
  for i in range(epochs):
    b_n = 0
    for start, end in zip(range(0, len(trX), batchsize), range(batchsize, len(trX), batchsize)):
      if debug >= 2:
        print("start: ", start)
        print("end: ", end)
      batch = trX[start:end]
      if debug >= 2:
        print("len(batch): ", len(batch))
        print("len(batch[0]): ", len(batch[0]))
        print("batch[0][:10]: ", batch[0][:10])
      cur_w = sess.run(ud_w, feed_dict={v0: batch, w: prev_w, vb: prev_vb, hb: prev_hb})
      cur_vb = sess.run(ud_vb, feed_dict={v0: batch, w: prev_w, vb: prev_vb, hb: prev_hb})
      cur_hb = sess.run(ud_hb, feed_dict={v0: batch, w: prev_w, vb: prev_vb, hb: prev_hb})
      prev_w = cur_w
      prev_vb = cur_vb
      prev_hb = cur_hb
      if debug >= 1:
        batch_error = sess.run(err_sum, feed_dict={v0: batch, w: cur_w, vb: cur_vb, hb: cur_hb})
        print("Epoch/Batch: ", i, "/", b_n, " : Error = ", batch_error)
        print
        b_n += 1
    errors.append(batch_error)
  #plot error
  if debug >= 1:
    plt.plot(errors)
    plt.ylabel('Error')
    plt.xlabel('Epoch')
    plt.show()

  recommendations(OUT_FILE_SME, names, ratings_int, smes, prev_w, prev_hb, prev_vb)
  




