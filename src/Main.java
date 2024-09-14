import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world!");
        new Main().run();
    }

    private void run(){
        //read data from file
        List<String[]> rawdata = readFromFile("10.TXT");

        //Process data from string to double
        List<double[]> data = listStringsToDoubles(rawdata);

        //print data
        printList(data);

        //Sample average
        double sa1 = sampleAverage(data, 1);
        double sa2 = sampleAverage(data, 2);
        System.out.println("Sample average: "+sa1+"    "+sa2);

        //Sample variance
        double sv1 = sampleVariance(data, 1, sa1);
        double sv2 = sampleVariance(data, 2, sa2);
        System.out.println("Sample variance: "+sv1+"    "+sv2);

        //point estimate of the standard deviation
        double peosd1 = pointEstimateOfStandardDeviation(sv1);
        double peosd2 = pointEstimateOfStandardDeviation(sv2);
        System.out.println("Sample variance: "+peosd1+"    "+peosd2);

        //standard deviation of the measurement result
        double sdmr1 = standardDeviationOfMeasurementResult(data, peosd1);
        double sdmr2 = standardDeviationOfMeasurementResult(data, peosd2);
        System.out.println("Sample variance: "+sdmr1+"    "+sdmr2);
    }
    private List<String[]> readFromFile(String fileName){
        List<String[]> res = new ArrayList<String[]>();
        try {
            File myObj = new File(fileName);
            Scanner myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                res.add(data.trim().replaceAll(" +", " ").split(" "));
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("File <"+fileName+"> not found.");
            e.printStackTrace();
        }
        return res;
    }

    private void printList(List<double[]> listData){
        for(double[] row:listData){
            System.out.println(Arrays.toString(row)+"\n");
        }
    }

    private List<double[]> listStringsToDoubles(List<String[]> data){
        List<double[]> res = new ArrayList<>();
        for(String[] row:data){
            double[] tmp = new double[row.length];
            for(int i=0; i<row.length; i++){
                tmp[i] = Double.parseDouble(row[i]);
            }
            res.add(tmp);
        }
        return res;
    }

    private double sampleAverage(List<double[]> data, int columnIndex){
        double res=0;
        if(data.size()!=0 && columnIndex>=0 && columnIndex<data.get(0).length) {
            for (double[] row : data) {
                res+= row[columnIndex];
            }
            res/=data.size();
        }
        return res;
    }

    private double sampleVariance(List<double[]> data, int columnIndex, double sampleAverage){
        double res=0;
        if(data.size()!=0 && columnIndex>=0 && columnIndex<data.get(0).length){
            for (double[] row : data) {
                res+=Math.pow(row[columnIndex]-sampleAverage, 2);
            }
            res/=data.size()-1;
        }
        return res;
    }

    private double pointEstimateOfStandardDeviation(double sampleVariance){return Math.sqrt(sampleVariance);}

    private double standardDeviationOfMeasurementResult(List<double[]> data, double pointEstimateOfStandardDeviation){
        return pointEstimateOfStandardDeviation/Math.sqrt(data.size());
    }
}