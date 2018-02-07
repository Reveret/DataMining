This is the NetKit-SRL Open source toolkit for Network Learning for
statistical relational learning.

See the LICENSE file for licensing information.

---------------------------------------------------------------------------
DIRECORY STRUCTURE
---------------------------------------------------------------------------
./
    README.txt    --- this file
    LICENSE       --- licensing information
    build.xml     --- Ant build file (Ant version 1.6+)
    changelog.txt --- changes since first release
    classes/      --- where class files end up
    docs/         --- the api docs
    examples/     --- examples for how to run the toolkit
                      [this is out of date and does not show all capabilities]
    lib/          --- properties files and the NetKit jar file.
    src/          --- sources, including junit tests
    userguide/    --- userguide (PDF)
                      [this is unfortunately out of date.  However, the help function
                      from the command-line should be able to get you started.]


---------------------------------------------------------------------------
REQUIREMENTS
---------------------------------------------------------------------------
  * Java 1.5+     --- NetKit is written to Java 1.5 specifications
  * Weka 3.4+     --- Needed to compile and if wanting to run with Weka
  * fetch-datastructures.jar --- needed for Active learning to cluster graphs
  * Colt 1.2.0+   --- Needed to compile and if wanting to get an adjancy matrix
  * Ant 1.6+      --- Needed to compile using the build file
  * JUnit 3.7+    --- Needed to build and run junit tests


---------------------------------------------------------------------------
BUILDING THE TOOLKIT
---------------------------------------------------------------------------
  * Use ant to build the jar file.  The build file also comes with tasks
    to build and run JUnit tests.  For this, you will need JUnit and need
    to put it in the Ant class path.

  * You will need to get the weka jarfile from:
        http://www.cs.waikato.ac.nz/ml/weka

  * You will need to get the colt jarfile from:
        http://dsd.lbl.gov/~hoschek/colt/

  * You will need to put these in the ./lib directory for ant to pick
    them up as part of the compile process.


---------------------------------------------------------------------------
RUNNING THE TOOLKIT
---------------------------------------------------------------------------
  * Once you have built NetKit, look at the examples directory and
    the example-runs.txt file to see general ways to run NetKit.

  * You can also peruse the userguide.pdf file to get more information.

  * If you intend to use Weka or colt functionalities, then you
    _must_ put the jars in the lib directory and name them:
        weka.jar
        colt.jar
        fetch-datastructures.jar
    These are the specific jars that the NetKit jar file expects in
    its classpath.


---------------------------------------------------------------------------
NOTE ON RUNNING NETKIT WITH THIRD PARTY LIBRARIES
---------------------------------------------------------------------------
  * You will only need colt.jar if you intend to get the adjacency matrix
    for matrix operations (that are done within colt)

  * You will only need weka.jar if you intend to use weka classifiers

  * You will only need fetch-datastructures.jar if you intend to use
    active learning or use the modularity clustering code which is
    part of the toolkit

