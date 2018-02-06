import java.io.IOException;

public class Moa {
    public static void main(String[] args) throws IOException {

        String file = "/home/roc/Desktop/DM/Practiues/StreamMining/moa-release-2017.06b/covtypeNorm.arff";

        HoeffdingTreeClassifier hoeff = new HoeffdingTreeClassifier(file);
        hoeff.run(1000000, true);

        AODEClassifier aode = new AODEClassifier(file);
        aode.run(10000000, true);

        NaiveBayesUpdateableClassifier naive = new NaiveBayesUpdateableClassifier(file);
        naive.run(1000000, true);


    }
}
