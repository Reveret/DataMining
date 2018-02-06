
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayesUpdateable;
import weka.core.Debug;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffLoader;

import java.io.File;

public class NaiveBayesUpdateableClassifier {

    private static String file;

    public NaiveBayesUpdateableClassifier(String file){
        this.file = file;
    }

    public void run(int numInstances, boolean isTesting) throws Exception{
        ArffLoader loader = new ArffLoader();
        loader.setFile(new File(file));
        Instances structure = loader.getStructure();
        structure.setClassIndex(structure.numAttributes() - 1);

        // train NaiveBayes
        NaiveBayesUpdateable nb = new NaiveBayesUpdateable();
        nb.buildClassifier(structure);
        Instance current;
        while ((current = loader.getNextInstance(structure)) != null)
            nb.updateClassifier(current);

        // evaluate classifier and print some statistics
        Evaluation eval = new Evaluation(data);
        eval.evaluateModel(cls, test);
        System.out.println(eval.toSummaryString("\nResults\n======\n", false));
    }

}
