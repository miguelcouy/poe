from posh_data import *
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as lg
from scipy.linalg import sqrtm, inv
from IPython.display import clear_output
from sklearn.decomposition import FastICA

from sympy import * 



class Calcular:
    def __init__(self):
        self.bindDataFrame = pd.DataFrame()
        self.funFuncao = []
        self.funIntegral = []
        self.results = []


    def PolinomioCotaVolume(self, fromThisDataFrame):
        x = symbols('x')

        for i in range(len(fromThisDataFrame)):
            iRow = fromThisDataFrame.iloc[i]   
            a = float(iRow['PCV(4)'].replace(",","."))
            b = float(iRow['PCV(3)'].replace(",","."))
            c = float(iRow['PCV(2)'].replace(",","."))
            d = float(iRow['PCV(1)'].replace(",","."))
            e = float(iRow['PCV(0)'].replace(",","."))

            expressaoIntegral = (
                (a/5) * x**5 
            +   (b/4) * x**4 
            +   (c/3) * x**3 
            +   (d/2) * x**2
            +      e  * x
            )

            expressaoFuncao = (
                a * x**4 
            +   b * x**3
            +   c * x**2
            +   d * x**1
            +   e
            )
            
            lambdaIntegral = lambdify(x, expressaoIntegral)
            lambdaFuncao = lambdify(x, expressaoFuncao)
            
            self.funFuncao.append(lambdaFuncao)
            self.funIntegral.append(lambdaIntegral)
        
        self.bindDataFrame.insert(0, "Funcao PCV", self.funFuncao)
        self.bindDataFrame.insert(1, "Integral PCV", self.funIntegral)
        
        return self.bindDataFrame
    
    def Produtibilidade(self, 
        mainDataFrame, mainDataFramePCV, 
        mainDataFrameVU):

        for i in range(len(mainDataFrame)):
            typeReservatorio = mainDataFrame.loc[i, 'Reg']

            if typeReservatorio in ['D', 'S']:
                volReservatorio = mainDataFrame.loc[i,'Vol.Ref.']
                varCotaMedia = mainDataFramePCV.loc[i, 'Funcao PCV'](volReservatorio)

                if mainDataFrame.loc[i, 'Tipo Perdas(1=%/2=M/3=K)'] == 2:
                    calcProdutibilidade = (
                          varCotaMedia 
                        - mainDataFrame.loc[i,'Valor Perdas']
                        - mainDataFrame.loc[i,'Canal Fuga Médio(m)']
                        )

                else:
                    calcProdutibilidade = (
                          (varCotaMedia - mainDataFrame.loc[i,'Canal Fuga Médio(m)'])
                        * (1-(mainDataFrame.loc[i,'Valor Perdas']/100))
                        )
                
            else:
                if type(mainDataFrameVU) == str and mainDataFrame == "Default": volUtil = 0.6
                else: volUtil = float(mainDataFrameVU.loc[i, 'Vol.Util'].replace(",","."))
                
                volMin = float(mainDataFrame.loc[i, 'Vol.min.(hm3)'].replace(",","."))
                volMax = float(mainDataFrame.loc[i, 'Vol.Máx.(hm3)'].replace(",","."))
                
                vol = (volMax - volMin) * volUtil + volMin

                calcIntegral= (
                    (
                    (
                      float(mainDataFramePCV.loc[i, 'Integral PCV'](vol).replace(",", "."))
                    - float(mainDataFramePCV.loc[i, 'Integral PCV'](volMin).replace(",", "."))
                    )
                    / (vol - volMin)
                    )
                    - float(mainDataFrame.loc[i, 'Canal Fuga Médio(m)'].replace(",", "."))
                    )

                if mainDataFrame.loc[i,'Tipo Perdas(1=%/2=M/3=K)'] == 2:
                    calcProdutibilidade = calcIntegral - float(mainDataFrame.loc[i,'Valor Perdas'].replace(",", "."))
                else:
                    calcProdutibilidade = calcIntegral * (1-(mainDataFrame.loc[i,'Valor Perdas']/100))

            
            resultProbabilidade = calcProdutibilidade * mainDataFrame.loc[i,'Prod.Esp.(MW/m3/s/m)']
            self.results.append(resultProbabilidade)
        
        mainDataFramePCV.insert(2, "Produtibilidade", self.funIntegral)
        
        return mainDataFramePCV



