
import moa.classifiers.Classifier;
import moa.classifiers.bayes.NaiveBayes;
import moa.evaluation.LearningCurve;
import moa.evaluation.WindowClassificationPerformanceEvaluator;
import moa.streams.ArffFileStream;
import moa.tasks.EvaluatePrequential;

public class NaiveBayesUpdateableClassifier {

    private static String file;

    public NaiveBayesUpdateableClassifier(String file){
        this.file = file;
    }

    public void run(int numInstances) {
        Classifier learner = new NaiveBayes();

        ArffFileStream stream = new ArffFileStream(file,-1);
        stream.prepareForUse();

        //prepare classification performance evaluator
        WindowClassificationPerformanceEvaluator windowClassEvaluator =
                new WindowClassificationPerformanceEvaluator();
        windowClassEvaluator.widthOption.setValue(1000);
        windowClassEvaluator.prepareForUse();

        //do the learning and checking using evaluate-prequential technique
        EvaluatePrequential ep = new EvaluatePrequential();
        ep.instanceLimitOption.setValue(numInstances);
        ep.learnerOption.setCurrentObject(learner);
        ep.streamOption.setCurrentObject(stream);
        ep.evaluatorOption.setCurrentObject(windowClassEvaluator);
        ep.prepareForUse();

        //do the task and get the result
        LearningCurve le = (LearningCurve) ep.doTask();
        System.out.println("\nEvaluate prequential using Naive Bayes");
        System.out.println(le);
    }
}
