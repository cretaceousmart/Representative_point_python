from matplotlib import pyplot as plt

def plot_power_normal(N,d):
  plt.plot(N,d[0],label = "RP Chi-square")
  plt.plot(N,d[1],label = "Fisher Chi-square")
  plt.plot(N,d[2],label = "KS Test")
  plt.plot(N,d[3],label = "CV Test")
  plt.plot(N,d[4],label = "SW Test")
  plt.legend()

def plot_power_unnormal(N,d):
  plt.plot(N,d[0],label = "RP Chi-square")
  plt.plot(N,d[1],label = "Fisher Chi-square")
  plt.plot(N,d[2],label = "KS Test")
  plt.plot(N,d[3],label = "CV Test")
  plt.legend()


