import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world!");
        new Main().run();
    }

    private void run(){
        //read data from file
        List<String[]> resClass = readFromFile("10.TXT");

        //Process data to 
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
}