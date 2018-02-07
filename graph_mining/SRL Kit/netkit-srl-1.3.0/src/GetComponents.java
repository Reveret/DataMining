import netkit.graph.Graph;
import netkit.graph.Node;
import netkit.util.*;
import java.io.File;
import java.util.*;

public class GetComponents {
  public static void main(String[] args)
  {
    for(String s : args)
    {
      File f = new File(s);
      System.out.println("=========================================");
      System.out.println("Reading graph from file "+s);
      Graph g = netkit.graph.io.SchemaReader.readSchema(f);
      GraphMetrics metrics = g.getMetrics();

      int nn = (int)metrics.getNumNodes();
      int ns = metrics.getNumSingletons();
      int nc = metrics.getNumComponents();

      System.out.println("Num-nodes: "+nn);
      System.out.println("Num-singletons: "+ns);
      System.out.println("Num-components: "+(nc-ns));

      String[][] c = new String[nc][];
      int[] ci = new int[nc];
      Arrays.fill(ci,0);

      System.out.print("Component-sizes");
      for(int i=0;i<nc;i++)
      {
	  int size=metrics.getComponentSize(i);
	  if(size<2)
	      continue;
	  System.out.print(","+size);
	  c[i] = new String[size];
      }
      System.out.println();
      for(Node n : g.getNodes())
      {
	  int i = metrics.getComponent(n);
	  if(c[i]==null)
	      continue;
	  c[i][ci[i]] = n.getName();
	  ci[i]++;
      }
      for(int i=0;i<nc;i++)
      {
	  if(c[i]==null)
	      continue;
	  
	  for(String n : c[i])
	  {
	      System.out.println(i+","+n);
	  }
      }
    }
  }
}
