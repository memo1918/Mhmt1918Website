from mmap import ACCESS_DEFAULT
import pandas as pd
import numpy as np
import re,os

# import matplotlib.pyplot as plt
# plt.switch_backend('agg')

class Analyzer():
    def __init__(self,filename,uploadFolder):
        self.filename = filename
        self.uploadFolder = uploadFolder


    def fileOpener(self,data = None):
        allWords = []
        file = self.uploadFolder+self.filename
        if self.filename.endswith('.txt'):
            with open(file,"r",encoding="utf-8") as data:
                tempdata = data.read().lower().strip("\n").strip('.,()"?!:;"').lstrip('.,()"?!:;"').rstrip('.,()?!:;"').replace(".", "").replace(",", "").split()
                 
                for j in tempdata:
                    if len(j) > 2:
                        allWords.append(j)
        else:
            data =pd.read_csv(file)['data'].to_list() 
            for i in data:
                value = i.lower().strip("\n")
                value = re.sub(r"^\w"," ",value,flags=re.ASCII).split()  
                for j in value:
                    j = j.strip('.,()"?!:;"').lstrip('.,()"?!:;"').rstrip('.,()?!:;"')
                    if len(j) > 2:
                        allWords.append(j)      
        
        if os.path.exists(file):
            os.remove(file)
        return np.array(allWords)

    
    def wordCounter(self,):
        allWords = self.fileOpener()
        df = pd.DataFrame({'Words': allWords, 'Count': np.ones(len(allWords))})
        gb = df.groupby(["Words"]).sum().sort_values(['Count'],ascending=False)
        gb.drop(gb[gb['Count'] < 2].index,inplace=True)


        return gb.head(20)

    
    # def graph(self,):
        
    #     wordCounts = self.wordCounter()

    #     explode = list(map(lambda x : 0.2,wordCounts.index))
    #     plot = wordCounts.plot.pie(y='Count',autopct='%1.1f%%',legend= False,explode=explode,ylabel="")

    #     fig = plot.get_figure()
    #     fig.savefig(self.uploadFolder+'pieChart.png')
