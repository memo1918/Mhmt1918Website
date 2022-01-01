from mmap import ACCESS_DEFAULT
import pandas as pd
import numpy as np
import re,os


class Analyzer():
    def __init__(self,uploadFolder,lenght,maxOutput,filename = "_"):
        self.filename = filename
        self.uploadFolder = uploadFolder
        self.lenght =lenght
        self.maxOutput=maxOutput

    def fileOpener(self,data = None):
        allWords = []
        file = self.uploadFolder+self.filename
        
        # Uses text from text_area
        if type(data) == str:
            tempdata = data.lower().strip("\n").strip('.,()"?!:;"').lstrip('.,()"?!:;"').rstrip('.,()?!:;"').split()
            for j in tempdata:
                    if len(j) > self.lenght:
                        allWords.append(j)
        
        # If uploaded file is txt
        elif self.filename.endswith('.txt'):
            with open(file,"r",encoding="utf-8") as data:
                tempdata = data.read().lower().strip("\n").strip('.,()"?!:;"').lstrip('.,()"?!:;"').rstrip('.,()?!:;"').split()
                 
                for j in tempdata:
                    if len(j) > self.lenght:
                        allWords.append(j)
       
        # If uploaded file is cvs
        elif self.filename.endswith('.csv'):
            data =pd.read_csv(file)['data'].to_list() 
            for i in data:
                value = i.lower().strip("\n")
                value = re.sub(r"^\w"," ",value,flags=re.ASCII).split()  
                for j in value:
                    j = j.strip('.,()"?!:;"').lstrip('.,()"?!:;"').rstrip('.,()?!:;"')
                    if len(j) > self.lenght:
                        allWords.append(j)      
        
        # Removes the uploaded file
        if os.path.exists(file):
            os.remove(file)
        
        return np.array(allWords)

    
    def wordCounter(self,data = None):
        allWords = self.fileOpener(data)
        
        df = pd.DataFrame({'Words': allWords, 'Count': np.ones(len(allWords))})
        gb = df.groupby(["Words"]).sum().sort_values(['Count'],ascending=False)
        gb.drop(gb[gb['Count'] < 2].index,inplace=True)

        return gb.head(self.maxOutput)
