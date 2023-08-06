# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 08:43:36 2020

@author: HP
"""

#dataFrameName[column_name].dtype
 
 
import statistics
import pandas as pd
import numpy as np
import random
#dataset=pd.read_csv(r"C:\Users\HP\Desktop\pp.csv")

def missing(input_file):
    dataset=pd.read_csv(input_file)
    #row_count=dataset.shape[0]
    column_count=dataset.shape[1]
    column_type=dataset.dtypes
    print(dataset.head(10))
    #print(column_type)

    for i in range(0,column_count) :
        # Check if the dataset has object type column
        if(column_type[i]=='object'):
                #Check if the values in the dataset are overall Null or not
                if(dataset.iloc[:,i].isnull().sum()):
                
                    list1=dataset.iloc[:,i].value_counts()
                    #print("list having frequency count")
                    #print(list1)
                    #Cg=heck if the freq count list has a mode 
                    if(len(set(list1))!=1):
                        
                        mode=statistics.mode(dataset.iloc[:,i])
                        #df1['weight'] = df1['weight'].fillna(0)
                        dataset.iloc[:,i]=dataset.iloc[:,i].fillna(mode)
                    #If the freq count has no mode then place a random value
                    else:
                        
                        #data_listt=pd.notnull(dataset.iloc[:,i])
                        #try to get the list for non null values
                        data_list = list(dataset.iloc[:,i])
                        #print(data_list)
                        data_list = [x for x in data_list if pd.notnull(x)]
                        random_value=random.choice(data_list)
                        #print(data_list)
                        #print(random_value)
                        dataset.iloc[:,i]=dataset.iloc[:,i].fillna(random_value)
    
                
        else:
            
            mean=np.mean(dataset.iloc[:,i])
            dataset.iloc[:,i]=dataset.iloc[:,i].fillna(mean)
            dataset.iloc[:,i]=round(dataset.iloc[:,i],1)
    print(dataset.head(10))
    print("missing data has been settled")
        
import sys 

def main():
    dataset=pd.read_csv(sys.argv[1]).values
    missing(dataset)

if __name__=="__main__":
     main()