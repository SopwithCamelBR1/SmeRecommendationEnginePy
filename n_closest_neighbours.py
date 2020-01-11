''' find n closest neighbours
#
# Returns: 
#   name_list - [person, [ratings array ]]
#   index_file - [person_a index, person_b_index, pearson correlation, pearson p value]
'''  
def closest_neighbours(sim_matrix, ratings_matrix, people_list, person, n_neighbours):
  #find index of person in the person list
  p_i = people_list.index(person)
  #create new sorted list - currently ignoring negatvies??
  s_list = sorted(sim_matrix[p_i], key=lambda x:x[2])
  #create new list with only top n_neighbours
  index_list = s_list[n_neighbours:]
  #debug
  if debug >= 1:
    print("Sorted list: ", s_list)
    print("Sorted list type: ", type(s_list))
    print("Top n sorted list: ", index_list)
    print("Top n sorted list type: ", type(index_list))
    print("")
  #convert index_list into an array of peoples names, and the ratings
  name_list = []
  l = len(index_list)
  for i in range(l):
    person_index = int(index_list[i][1])
    name_list.append([people_list[person_index], ratings_matrix[person_index]])
  #debug
  if debug >= 1:
    print("Named list: ", name_list)
    print("")
  
  return name_list, index_list