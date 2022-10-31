import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import chi2
from scipy.stats import logistic,laplace

def pearson_chi2_test(sample,k,test_type):
  n = sample.size
  mi = np.zeros(2*k) #2k个区间
  pi = np.zeros(2*k) #2k个区间
  BP = np.zeros(2*k-1) #k-1个分割点, k个区间
  a = [(i+1) * 1/(2*k) for i in range(2*k-1)]

  for i in range(0,2*k-1):
    BP[i] = norm.ppf(a[i], loc=0, scale=1) # for N(0,1)
  

  #the first and last bolck:
  for i in range(n):
      if (sample[i] < BP[0]): mi[0] +=1
      if (sample[i] > BP[2*k-2]): mi[2*k-1] +=1
  
  #other block:
  for j in range(1,2*k-1):
      for i in range(n):
          if((sample[i] >= BP[j-1]) and (sample[i] <= BP[j])): mi[j] += 1

  
  # for pi:
  if(test_type == "Normal_Test"):
    pi[0] = norm.cdf(BP[0], loc=0, scale=1)
    pi[k-1] = norm.cdf(0, loc=0, scale=1) - norm.cdf(BP[k-2], loc=0, scale=1)
    for i in range(1,k-1):
        pi[i] = norm.cdf(BP[i]) - norm.cdf(BP[i-1])
    pi = pi[0:k]
    pi = np.append(pi,pi[::-1])
  elif(test_type == "Logistic_Test"):
    pi[0] = logistic.cdf(BP[0], loc=0, scale=1)
    pi[k-1] = logistic.cdf(0, loc=0, scale=1) - logistic.cdf(BP[k-2], loc=0, scale=1)
    for i in range(1,k-1):
        pi[i] = logistic.cdf(BP[i]) - logistic.cdf(BP[i-1])
    pi = pi[0:k]
    pi = np.append(pi,pi[::-1])
  elif(test_type == "Laplace_Test"):
    pi[0] = laplace.cdf(BP[0], loc=0, scale=1)
    pi[k-1] = laplace.cdf(0, loc=0, scale=1) - laplace.cdf(BP[k-2], loc=0, scale=1)
    for i in range(1,k-1):
        pi[i] = laplace.cdf(BP[i]) - laplace.cdf(BP[i-1])
    pi = pi[0:k]
    pi = np.append(pi,pi[::-1])

  #calculate the chi-square test statistic:
  mse_x_square = 0
  for i in range(0,2*k): mse_x_square += ((mi[i] - n*pi[i])**2)/(n*pi[i])
  #return test result:
  p_value = 1 - chi2.cdf(mse_x_square,df = 2*k-3)
  # return (0 if np.isnan(p_value) else p_value)
  # return p_value
  if(p_value < 0.05):return 1
  else: return 0
  


# # #Example:
# normal_RP = pd.read_csv('/content/drive/MyDrive/RP_project/RP_test/data/Normal.csv') #不同test只是RP不同而已，可以改成class
# normal_RP = np.array(normal_RP)

# rp_chi = pearson_chi2_test

# k = 5
# sample = np.random.normal(0,1,100)

# # rp_chi(sample = sample, RP = normal_RP[1 + 2*(k-2),0:k], k = k)