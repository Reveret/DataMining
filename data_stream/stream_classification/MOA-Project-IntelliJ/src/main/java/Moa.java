

public class Moa {
    public static void main(String[] args) {

        String file;
        file = "./covtypeNorm.arff";
        //file = "./poker-lsn.arff";
        //file = "./elecNormNew.arff";

        HoeffdingTreeClassifier hoeff = new HoeffdingTreeClassifier(file);
        hoeff.run(1000000);

        NaiveBayesUpdateableClassifier naive = new NaiveBayesUpdateableClassifier(file);
        naive.run(1000000);

        AODEClassifier aode = new AODEClassifier(file);
        aode.run(10000000);
    }
}
