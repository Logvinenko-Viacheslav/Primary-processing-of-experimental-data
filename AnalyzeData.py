import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import re
import math
import numpy as np
from scipy.stats import shapiro


def main():
    #read data from file
    data = readFileData("10.TXT")
    #buildHistogram(data, tmpName, i)
    #print(data)
    
    #Sample average
    sa1 = sampleAverage(data, 1);
    sa2 = sampleAverage(data, 2);
    print("Sample average: "+str(sa1)+"    "+str(sa2))
    
    #Sample variance
    sv1 = sampleVariance(data, 1, sa1);
    sv2 = sampleVariance(data, 2, sa2);
    print("Sample variance: "+str(sv1)+"    "+str(sv2))
    
    #point estimate of the standard deviation
    peosd1 = pointEstimateOfStandardDeviation(sv1)
    peosd2 = pointEstimateOfStandardDeviation(sv2)
    print("Point estimate SD: "+str(peosd1)+"    "+str(peosd2))

    #standard deviation of the measurement result
    sdmr1 = standardDeviationOfMeasurementResult(data, peosd1)
    sdmr2 = standardDeviationOfMeasurementResult(data, peosd2)
    print("Standart deviation: "+str(sdmr1)+"    "+str(sdmr2))
    
    rotatedData = rotate2dArray(data)
    buildHistogram(rotatedData, "data1", "name", 1, sa1, peosd1)

def rotate2dArray(data):
    res = []
    for i in range(0, len(data[0])):
        tmp = []
        for row in data:
            tmp.append(row[i])
        res.append(tmp)
    return res

def readFileData(fileName):
    res = []
    with open(fileName) as file:
        reader = csv.reader(file)
        file.seek(0)
        for row in reader:
            tmp = "".join(row).strip()
            tmp = re.sub(' +', ' ', tmp)      
            tmp = tmp.split(" ")
            arrStrToFloat(tmp)
            res.append(tmp)
    return res        

def sampleAverage(data, columnIndex):
    res=0.0;
    if len(data)!=0 and columnIndex>=0 and columnIndex<len(data[0]):
        for row in data:
            res+= row[columnIndex];
        res/=len(data);
    return res;

def sampleVariance(data, columnIndex, sampleAverage):
    res=0.0;
    if len(data)!=0 and columnIndex>=0 and columnIndex<len(data[0]):
        for row in data:
            res+=pow(row[columnIndex]-sampleAverage, 2);
        res/=len(data)-1;
    return res;

def pointEstimateOfStandardDeviation(sampleVariance):
    return math.sqrt(sampleVariance)

def standardDeviationOfMeasurementResult(data, pointEstimateOfStandardDeviation):
    return pointEstimateOfStandardDeviation/math.sqrt(len(data));

def arrStrToFloat(array):
    for i in range(0, len(array)):
        array[i]=float(array[i])

def buildHistogram(data, parameter_name, hystogram_name, columnIndex, sampleAverage, pointEstimateOfStandardDeviation):
    #print("paramente:"+parameter_name+" data:"+str(data))
    desired_data = data[columnIndex]
    print(str(min(desired_data))+"  "+str(max(desired_data)))
    mrange = (min(desired_data), max(desired_data))
    bins=50
    desired_data1=[3,4]
    plt.hist(desired_data, bins, mrange, density=True, color = 'blue', histtype = 'bar', rwidth = 0.8)
    plt.xlabel(parameter_name)
    #plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel('Number of measurements')
    plt.title("Project #"+str(hystogram_name)+" "+parameter_name+" metric hystogram")
    x = np.linspace(min(desired_data), max(desired_data), 100)
    y = []
    for i in range(0, len(x)):
        y.append(probabilityDensities(x[i], sampleAverage, pointEstimateOfStandardDeviation))
    plt.plot(x, y, color="red", linewidth=2)
    
    #Shapiro-Wilk
    statistic, p_value = shapiro(desired_data)
    print(f"Shapiro-Wilk Statistic: {statistic}, P-value: {p_value}")
    
    plt.savefig(str(hystogram_name)+parameter_name+".png")
    #plt.clear()
    plt.clf()
  
def probabilityDensities(x, sampleAverage, pointEstimateOfStandardDeviation):
    res=0.0
    res+=1/(pointEstimateOfStandardDeviation*math.sqrt(2*math.pi))*math.exp(-1*(pow(x-sampleAverage, 2)/(2*pow(pointEstimateOfStandardDeviation, 2))))
    return res

if __name__ == '__main__':
    main()
