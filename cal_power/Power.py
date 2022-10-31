from curses import KEY_SAVE
from symbol import and_test
from cgi import print_form
from os import error
import numpy as np
import pandas as pd
from scipy import stats


import importlib

from my_chi2 import rp_chi2, pearson_chi2 
# from pearson_chi2 import pearson_chi2_test
importlib.reload(rp_chi2)
importlib.reload(pearson_chi2)


class power_simulator():
    def __init__(self, RP , test_type):
        self.RP  = RP
        self.test_type = test_type
        self.auto_print_test_type()
    
    def auto_print_test_type(self):
        print("Testing Type: ", self.test_type)
    
    def cal_power(self,**kwarg):
    
      N = kwarg["n"];k = kwarg["k"];m = kwarg["m"]

      if(self.test_type == "Normal_Test"):
          ks_cdf = stats.norm.cdf
          cv_cdf = 'norm'
      elif(self.test_type == "Laplace_Test"):
          ks_cdf = stats.laplace.cdf
          cv_cdf = 'laplace'
      elif(self.test_type == "Logistic_Test"):
          ks_cdf = stats.logistic.cdf
          cv_cdf = 'logistic'  
      else: raise NotImplementedError('You input an unknown test_type!')

      if(self.test_type == "Normal_Test"):
        result = []
        for n in N:
          I_1 = np.zeros(m);I_2 = np.zeros(m);I_3 = np.zeros(m);I_4 = np.zeros(m); I_5 = np.zeros(m)

          for i in range(0,m):
            # sample = np.random.laplace(loc = 0.1,scale = 1,size = n) #need to change!!!
            sample = np.random.logistic(loc = 0.1,scale = 1,size = n)
            # sample = np.random.normal(3,1,n)
            I_1[i] = rp_chi2.rp_chi2_test(sample, self.RP, k,self.test_type)
            I_2[i] = pearson_chi2.pearson_chi2_test(sample,k,self.test_type)
            I_3[i] = ((stats.kstest(sample,ks_cdf).pvalue)<=0.05)
            I_4[i] = ((stats.cramervonmises(sample, cv_cdf).pvalue)<=0.05)
            I_5[i] = (stats.shapiro(sample).pvalue)<=0.05
          result.append([sum(I_1)/m,sum(I_2)/m,sum(I_3)/m,sum(I_4)/m,sum(I_5)/m])
        return result
      else:
        result = []
        for n in N:
          I_1 = np.zeros(m);I_2 = np.zeros(m);I_3 = np.zeros(m);I_4 = np.zeros(m);

          for i in range(0,m):
            sample = np.random.laplace(loc = 0.1,scale = 1,size = n) #need to change!!!
            I_1[i] = rp_chi2.rp_chi2_test(sample, self.RP, k,self.test_type)
            I_2[i] = pearson_chi2.pearson_chi2_test(sample,k,self.test_type)
            I_3[i] = ((stats.kstest(sample,ks_cdf).pvalue)<=0.05)
            I_4[i] = ((stats.cramervonmises(sample, cv_cdf).pvalue)<=0.05)
          result.append([sum(I_1)/m,sum(I_2)/m,sum(I_3)/m,sum(I_4)/m])
        return result

      
