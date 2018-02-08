
import moa.core.TimingUtils;
import weka.classifiers.Classifier;
import moa.evaluation.LearningCurve;
import moa.evaluation.WindowClassificationPerformanceEvaluator;
import moa.streams.ArffFileStream;
import moa.tasks.EvaluatePrequential;
import weka.classifiers.bayes.AODE;
import weka.classifiers.meta.MOA;
import weka.core.Instance;
import weka.core.Instances;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class AODEClassifier {

    private static String file;

    public AODEClassifier(String file){
        this.file = file;
    }

    public void run(int numInstances) throws Exception{
        Classifier learner = new AODE();

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
        System.out.println("\nEvaluate prequential using AODE");
        System.out.println(le);

        /*
        TRIED TO USE THE MOA API CODE TO ADAPT THE WEKA CLASSIFIER TO PREQUENTIAL EVALUATION BUT
        IT DID NOT WORK

        Classifier learner = new AODE();
        BufferedReader reader = new BufferedReader(
                new FileReader("/some/where/data.arff"));
        Instances stream = new Instances(reader);
        reader.close();
        // setting class attribute
        stream.setClassIndex(stream.numAttributes() - 1);


        learner.buildClassifier(stream.firstInstance());

        int numberSamplesCorrect = 0;
        int numberSamples = 0;
        boolean preciseCPUTiming = TimingUtils.enablePreciseTiming();
        long evaluateStartTime = TimingUtils.getNanoCPUTimeOfCurrentThread();
        while (stream.hasMoreInstances() && numberSamples < numInstances) {
            Instance trainInst = stream.nextInstance().getData();
            if (isTesting) {
                if (learner.correctlyClassifies(trainInst)){
                    numberSamplesCorrect++;
                }
            }
            numberSamples++;
            learner.trainOnInstance(trainInst);
        }
        double accuracy = 100.0 * (double) numberSamplesCorrect/ (double) numberSamples;
        double time = TimingUtils.nanoTimeToSeconds(TimingUtils.getNanoCPUTimeOfCurrentThread()- evaluateStartTime);
        System.out.println(numberSamples + " instances processed with " + accuracy + "% accuracy in "+time+" seconds.");*/
    }

}
