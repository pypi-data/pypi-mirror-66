



 
 
import statistics
import pandas as pd
import numpy as np
import random


def missing(input_file):
    dataset=pd.read_csv(input_file)
   
    column_count=dataset.shape[1]
    column_type=dataset.dtypes
    print(dataset.head(10))
   

    for i in range(0,column_count) :
       
        if(column_type[i]=='object'):
               
                if(dataset.iloc[:,i].isnull().sum()):
                
                    list1=dataset.iloc[:,i].value_counts()
                    
                    if(len(set(list1))!=1):
                        
                        mode=statistics.mode(dataset.iloc[:,i])
                       
                        dataset.iloc[:,i]=dataset.iloc[:,i].fillna(mode)
                  
                    else:
                        
                        data_list = list(dataset.iloc[:,i])
                        
                        data_list = [x for x in data_list if pd.notnull(x)]
                        random_value=random.choice(data_list)
                        
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