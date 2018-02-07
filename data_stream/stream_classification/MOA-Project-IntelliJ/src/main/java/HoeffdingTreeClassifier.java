
import moa.classifiers.Classifier;
import moa.classifiers.trees.HoeffdingTree;
import moa.core.TimingUtils;
import moa.streams.ArffFileStream;
import com.yahoo.labs.samoa.instances.Instance;


public class HoeffdingTreeClassifier {

        private static String file;

        public HoeffdingTreeClassifier(String file){
                this.file = file;
        }

        public void run(int numInstances, boolean isTesting){
                Classifier learner = new HoeffdingTree();
                ArffFileStream stream = new ArffFileStream(file,-1);
                stream.prepareForUse();

                learner.setModelContext(stream.getHeader());
                learner.prepareForUse();

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
                System.out.println(numberSamples + " instances processed with " + accuracy + "% accuracy in "+time+" seconds.");
        }

}
