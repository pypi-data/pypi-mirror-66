"""This module contains a function that will print the items individually from the list irrespective of its nested depth."""
def print_list(num_list , level = 0):
    """start of the function,A second argument called “level" is used to insert tab-stops when a nested list is encountered."""
    for each in num_list:
        if isinstance(each,list):
            print_list(each,level+1)
        else:
            for tab_stop in range(level):
                print("\t", end = '')
            print(each)




