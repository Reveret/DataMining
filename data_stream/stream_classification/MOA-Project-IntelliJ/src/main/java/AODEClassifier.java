import com.yahoo.labs.samoa.instances.Instance;
import moa.core.TimingUtils;
import moa.streams.ArffFileStream;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.AODE;
import weka.core.Instances;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class AODEClassifier {

    private static String file;

    public AODEClassifier(String file){
        this.file = file;
    }

    public void run(int numInstances, boolean isTesting) throws FileNotFoundException, IOException{

        BufferedReader reader = new BufferedReader(
                new FileReader(file));
        Instances data = new Instances(reader);
        reader.close();
        // setting class attribute
        data.setClassIndex(data.numAttributes() - 1);

        AODE learner = new AODE();
        learner.buildClassifier(data);
        Evaluation eval = new Evaluation(data);
        
    }

}
