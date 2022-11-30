import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from sklearn import linear_model as ln
import IOIwrote as io

class PopulationPredict():

    def __init__(self,csvSourceFilePath:str):
        #Save .csv file and csvSrc:
        self.csvSrc=pd.read_csv(csvSourceFilePath)

        #Change the value of Administrative district if the value is None:
        self.csvSrc["Administrative district"]=self.csvSrc["Administrative district"].replace([None],"None")

        #Getting the country or states available:
        self.cntry:list=self.csvSrc["Country/State"].drop_duplicates().to_list()

    def GetAdmnDstrct(self,cntryName:str)->list:
        #Get all datas for the given country or state:
        self.dataSrc=self.csvSrc.loc[self.csvSrc["Country/State"]==cntryName]

        #Getting the administrative district for the given country:
        admnDstrct:list=self.dataSrc["Administrative district"].drop_duplicates().to_list()

        return admnDstrct

    def GetDatas(self,admnstrtName:str):
        #Get all datas for the given administative district:

        self.dataSrc=self.csvSrc.loc[self.csvSrc["Administrative district"]==admnstrtName]

        #Get all datas by gender:
        self.mlDtFrmSrc=self.dataSrc.loc[self.dataSrc["Sex"]=="Male"]
        self.fmlDtFrmSrc=self.dataSrc.loc[self.dataSrc["Sex"]=="Female"]

        #Drop all useless info:
        self.mlDtFrmSrc=self.mlDtFrmSrc.drop(["Country/State","Administrative district","Sex"],axis=1)
        self.fmlDtFrmSrc=self.fmlDtFrmSrc.drop(["Country/State", "Administrative district", "Sex"], axis=1)

        #Convert dataframe to numpy array:
        self.mlX=self.mlDtFrmSrc.iloc[:,0].values.reshape(-1,1)
        self.mlY=self.mlDtFrmSrc.iloc[:,1].values.reshape(-1,1)

        self.fmlX=self.fmlDtFrmSrc.iloc[:,0].values.reshape(-1,1)
        self.fmlY=self.fmlDtFrmSrc.iloc[:,1].values.reshape(-1,1)

        self.ttlX=np.array(self.mlX)    #Create numpy array to store the year for total population.
        self.ttlY=np.array([])  ##Create an empty numpy array to store the total population.

        #Get the number of total population (male+female) for each year:
        for i in range(len(self.mlY)):
            self.ttlY=np.append(self.ttlY,self.mlY[i]+self.fmlY[i])

    def MakePrediction(self,predictYear:int=2000):
        self.mlModel=ln.LinearRegression().fit(self.mlX,self.mlY)
        self.fmlModel=ln.LinearRegression().fit(self.fmlX,self.fmlY)
        self.ttlModel=ln.LinearRegression().fit(self.ttlX,self.ttlY)

        mlPredict:float=float(self.mlModel.predict([[predictYear]]))
        fmlPredict:float=float(self.fmlModel.predict([[predictYear]]))
        ttlPredict:float=float(self.ttlModel.predict([[predictYear]]))

        return mlPredict,fmlPredict,ttlPredict

def ConsoleUI():

    repeat:bool=True
    srcFilePath:str=""
    fileValid:bool=False
    mlPrdt:int=0
    fmlPrdt:int=0
    ttlPrdt:int=0

    #Choose .csv file:
    while fileValid==False:
        srcFilePath=input("Enter the file path for the .csv file: ")

        if os.path.exists(srcFilePath)==True:

            fileValid=True

            if srcFilePath.endswith(".csv") == False:
                fileValid = False
                print("Wrong file type!")

        else:
            print("File not exist!")

    #Pass the .csv file path:
    p0=PopulationPredict(srcFilePath)

    while repeat==True:

        #Input country or state:
        print(f"Countries or states in \"{srcFilePath:^20}\":")

        for i in range(len(p0.cntry)):
            print(f"Index: {i:^3}|   Country or state: {p0.cntry[i]:^16}")

        cntryIndex:int=io.ReadInt(qstStr="Choose a country or state (Index): ",inMin=0,inMax=len(p0.cntry))

        #Pass the country or state:
        admnstrt:list=p0.GetAdmnDstrct(cntryName=p0.cntry[cntryIndex])

        #Input administrative district:
        print(f"Administrative districts in {p0.cntry[cntryIndex]}:")

        for i in range(len(admnstrt)):
            print(f"Index: {i:^3}|  Administrative district: {admnstrt[i]}")

        admnstrtIndex:int=io.ReadInt(qstStr="Choose an administrative district (Index): ",inMin=0,inMax=len(admnstrt))

        #Pass the administrative district:
        p0.GetDatas(admnstrtName=admnstrt[admnstrtIndex])

        yrPrdt:int=io.ReadInt(qstStr="Year to predict: ",inMin=1000,inMax=10000)
        mlPrdt,fmlPrdt,ttlPrdt=p0.MakePrediction(yrPrdt)

        #Results:
        print(f"Population prediction for year {yrPrdt:^4}:")
        print(f"Male population ('000): {mlPrdt:^8}")
        print(f"Female population ('000): {fmlPrdt:^8}")
        print(f"Total population ('000): {ttlPrdt:^8}")

        repeat=io.YNDecision(decisionStr="Repeat? (Y/N)\n")

if __name__=="__main__":
    ConsoleUI()