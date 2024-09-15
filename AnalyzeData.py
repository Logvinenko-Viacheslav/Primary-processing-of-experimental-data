import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import re
import math
import numpy as np
from scipy.stats import shapiro
from scipy.stats import anderson

def main():
    #read data from file
    data = readFileData("10.TXT")
    #buildHistogram(data, tmpName, i)
    #print(data)
    
    print("Name                      x1                          x2")
    
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
    
    print("\nFOR x1:")
    processData(rotatedData, "data1", "x1", 1, sa1, peosd1)
    
    print("\nFOR x2:")
    processData(rotatedData, "data2", "x2", 2, sa2, peosd2)

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

def processData(data, parameter_name, hystogram_name, columnIndex, sampleAverage, pointEstimateOfStandardDeviation):
    #print("paramente:"+parameter_name+" data:"+str(data))
    desired_data = data[columnIndex]
    #print(str(min(desired_data))+"  "+str(max(desired_data)))
    mrange = (min(desired_data), max(desired_data))
    bins=50
    plt.hist(desired_data, bins, mrange, density=True, color = 'blue', histtype = 'bar', rwidth = 0.8)
    plt.xlabel(parameter_name)
    #plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel('Number of measurements')
    plt.title(str(hystogram_name)+" hystogram")
    x = np.linspace(min(desired_data), max(desired_data), 100)
    y = []
    for i in range(0, len(x)):
        y.append(probabilityDensities(x[i], sampleAverage, pointEstimateOfStandardDeviation))
    plt.plot(x, y, color="red", linewidth=2)
    
    #Shapiro-Wilk (UserWarning: scipy.stats.shapiro: For N > 5000, computed p-value may not be accurate. Current N is 16426.)
    #statistic, p_value = shapiro(desired_data)
    #print(f"Shapiro-Wilk Statistic: {statistic}, P-value: {p_value}")
    
    #Anderson-Darling
    #'norm' – Gaussian distribution.
    #'expon' – Exponential distribution.
    #'logistic' – Logistic distribution.
    #'gumbel' – Gumbel distribution.
    #'gumbel_r' – Right-skewed Gumbel distribution.
    #'gumbel_l' – Left-skewed Gumbel distribution.
    result = anderson(desired_data, dist='norm')
    print(f"Critical Values: {result.critical_values}")
    print(f"Significance Levels: {result.significance_level}")
    print(f"Anderson-Darling Statistic (Gaussian distribution): {result.statistic}")
    
    result = anderson(desired_data, dist='expon')
    print(f"Anderson-Darling Statistic (Exponential distribution): {result.statistic}")
    
    result = anderson(desired_data, dist='logistic')
    print(f"Anderson-Darling Statistic (Logistic distribution): {result.statistic}")
    
    result = anderson(desired_data, dist='gumbel')
    print(f"Anderson-Darling Statistic (Gumbel distribution): {result.statistic}")
    
    result = anderson(desired_data, dist='gumbel_r')
    print(f"Anderson-Darling Statistic (Right-skewed Gumbel distribution): {result.statistic}")
    
    result = anderson(desired_data, dist='gumbel_l')
    print(f"Anderson-Darling Statistic (Left-skewed Gumbel distribution): {result.statistic}")
    
    #Pearson's criterion
    
    #number of subranges
    m=5*math.log(len(desired_data))
    m=math.ceil(m)
    
    #size of subranges
    deltX=(max(desired_data)-min(desired_data))/m
    xBorders=[]
    
    #borders of subranges
    for i in range(0,m):
        tmp=[]
        tmp.append(min(desired_data)+i*deltX) #border beggin
        tmp.append(min(desired_data)+(i+1)*deltX) #border end
        xBorders.append(tmp)
        
    #theoretical probability for the class and Expected frequencies
    probabilities=[] #sampleAverage / pointEstimateOfStandardDeviation
    expectFrequencies=[]
    for i in range(0, m):
        tmp=probabilityDensities((xBorders[i][1]-sampleAverage)/pointEstimateOfStandardDeviation, sampleAverage, pointEstimateOfStandardDeviation)-probabilityDensities((xBorders[i][0]-sampleAverage)/pointEstimateOfStandardDeviation, sampleAverage, pointEstimateOfStandardDeviation)
        probabilities.append(tmp)
        expectFrequencies.append(tmp*len(desired_data))
        
    #observed frequencies
    observedFrequencies=[0]*len(expectFrequencies)
    for i in range(0, len(desired_data)):
        for j in range(0, m):
            if desired_data[i]>xBorders[j][0] and desired_data[i]<xBorders[j][1]:
                break
        
    #Chi-Squared Test
    xi_s=0.0
    for i in range(0, m):
        xi_s+=math.pow(observedFrequencies[i]-expectFrequencies[i], 2)/expectFrequencies[i]
        
    print("Pearson's criterion: "+str(xi_s))
    #degrees of freedom
    degreesOfFreedom=m-2-1
    print("degrees of freedom: "+str(degreesOfFreedom))
   
    plt.savefig(str(hystogram_name)+parameter_name+".png")
    #plt.clear()
    plt.clf()
  
def probabilityDensities(x, sampleAverage, pointEstimateOfStandardDeviation):
    res=0.0
    res+=1/(pointEstimateOfStandardDeviation*math.sqrt(2*math.pi))*math.exp(-1*(pow(x-sampleAverage, 2)/(2*pow(pointEstimateOfStandardDeviation, 2))))
    return res

if __name__ == '__main__':
    main()
