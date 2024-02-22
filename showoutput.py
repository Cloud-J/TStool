import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


files = os.listdir('output/')
for file in files:
    data = pd.read_csv('output/' + file, index_col=0).to_numpy()
    plt.plot(data[:,0],data[:,1])
    for i in range(len(data)):
        if data[i,2]==1:
            plt.scatter(data[i,0],data[i,1],color='r')
    plt.show()
    