import moa.classifiers.Classifier;
import moa.classifiers.meta.PairedLearners;
import moa.classifiers.trees.HoeffdingTree;
import moa.evaluation.BasicClassificationPerformanceEvaluator;
import moa.evaluation.LearningCurve;
import moa.streams.ArffFileStream;
import moa.tasks.EvaluatePrequential;
import weka.classifiers.bayes.AODE;

import java.io.IOException;

public class Moa {
    /*public static void main(String[] args) throws IOException {

        String file = "/home/roc/Desktop/DM/Practiues/StreamMining/moa-release-2017.06b/covtypeNorm.arff";

        HoeffdingTreeClassifier hoeff = new HoeffdingTreeClassifier(file);
        hoeff.run(1000000, true);

        AODEClassifier aode = new AODEClassifier(file);
        aode.run(10000000, true);

        NaiveBayesUpdateableClassifier naive = new NaiveBayesUpdateableClassifier(file);
        naive.run(1000000, true);


    }*/
    public static void main(String[] args) {

        String file = "/home/roc/Desktop/DM/DataMining/data_stream/stream_classification/covtypeNorm.arff";
        ArffFileStream fs = new ArffFileStream(file, -1);
        fs.prepareForUse();

        //Classifier learner = new HoeffdingTree();
        Classifier learner = (weka.classifiers.Classifier)new AODE();
        AODE aux = new AODE();
        aux.

        BasicClassificationPerformanceEvaluator evaluator = new BasicClassificationPerformanceEvaluator();

        EvaluatePrequential task = new EvaluatePrequential();
        task.learnerOption.setCurrentObject(learner);
        task.streamOption.setCurrentObject(fs);
        task.evaluatorOption.setCurrentObject(evaluator);

        task.prepareForUse();

        LearningCurve le = (LearningCurve) task.doTask();

        System.out.println(le);

    }
}
