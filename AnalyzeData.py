import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def main():
    file = open("10.TXT", "r")
    number_of_projects = int(file.readline())
    file.close()
    for i in range(1, number_of_projects+1):
        with open(str(i)+"class.csv") as csvfile:
            csv_reader = csv.reader(csvfile)
            metric_list=[["cbo",-1], ["fanin",-1], ["fanout", -1], ["wmc", -1], ["rfc", -1], ["noc", -1], ["totalMethodsQty", -1], ["totalFieldsQty", -1]]
            for j in range(0, len(metric_list)):
                csvfile.seek(0)
                tmpName = metric_list[j][0]
                first=True
                tmp = []
                for row in csv_reader:
                    if first:
                        metric_list[j][1]=getIndexOfColumn(row, tmpName)
                        first=False
                    elif(row[metric_list[j][1]].isdigit()):
                        tmp.append(row[metric_list[j][1]])
                buildHistogram(tmp, tmpName, i)
            #if not tmp:
            #    pass
            #else:
            #    buildHistogram(tmp, "cbo", i)

def getIndexOfColumn(row, name):
    res=-1
    i=0
    for x in row:
        if(x==name):
            res=i
            break
        i+=1
    return res

def buildHistogram(data, parameter_name, hystogram_name):
    #print("paramente:"+parameter_name+" data:"+str(data))
    desired_data = [int(numeric_string) for numeric_string in data]
    range = (min(desired_data), max(desired_data))
    bins=20
    plt.hist(desired_data, bins, range, color = 'blue', histtype = 'bar', rwidth = 0.8)
    plt.xlabel(parameter_name)
    #plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel('Number of measurements')
    plt.title("Project #"+str(hystogram_name)+" "+parameter_name+" metric hystogram")
    plt.savefig(str(hystogram_name)+parameter_name+".png")
    #plt.clear()
    plt.clf()

if __name__ == '__main__':
    main()
