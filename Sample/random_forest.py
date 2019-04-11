import decision_tree as dt
import pandas as pd
import random as rnd

rows = pd.read_csv("sample_dataset.csv")
DATASET_HEADERS = rows.columns

class Forest:
    '''Class that represents the random forest. Contains an array of decision trees.'''
    def __init__(self):
        self.trees = []


def build_forest(rows):
    '''Builds the forest. 

    Creates deciosion node classes and appentds
    them into an array defined int Forest class.'''
    btset, out = buil_bootstrapped_dataset(rows)
    subset = get_subset(btset, [0])
    print(subset)

def get_subset(rows, columns = []):
    '''Get a subset of columns from a dataset.

    Parameter columns represents an array of integers. 
    This ints are indexes of columns in the original dataset
    that will be put in the new subset.'''

    sub_columns = [] #Empty array of columns
    for col in columns: 
        sub_columns.append(rows[[DATASET_HEADERS[col]]]) #Append defined columns to the sub_columns array
    sub_columns.append(rows[[DATASET_HEADERS[-1]]]) #Append the label column to the sub_columns array
    subset = pd.concat(sub_columns, axis=1) #Form a datafreme from all the extracted columns

    return subset #Return the dataframe

def buil_bootstrapped_dataset(rows):
    '''Builds a bootstrapped dataset out of dateset passed as the parameter.

    It is built by taking random row from the original dataset and placing them in the bootstrapped dataset.
    The bootstrapped data set has the same number of rows as the original dataset.'''

    orig_dataset = rows.to_dict('indexed') # Covner the dataframe into a dict
    bootdata = {} #Create empty dict to store the randomly selected row from the original dataset
    out_of_bag_samples = {}

    # Creating bootstrapped dateset
    for i in range(len(orig_dataset)):
        rand_index = rnd.randint(0, len(rows.index)-1) #Chose a random int from 0 to the number of rows in the original dataset
        bootdata[i] = orig_dataset[rand_index] #Takes a random row from the original dataset and places it into do bootstraped datset

    #Creating "out of bag dataset"
    index = 0 # Counts next dict key
    for value in orig_dataset.values(): #Interates all values form the original dataset
        if value not in bootdata.values(): # Cheks if the value is in the bootstrapped dataset
            out_of_bag_samples[index] = value # If it is not, then the value is placed in the "out of bag" dataset
            index += 1

    df_bootstrapped = pd.DataFrame.from_dict(bootdata, orient='index') # Converts dict to pd.DataFrame
    df_out_of_bag = pd.DataFrame.from_dict(out_of_bag_samples, orient='index') # Converts dict to pd.DataFrame

    return df_bootstrapped, df_out_of_bag # Return the new datasets