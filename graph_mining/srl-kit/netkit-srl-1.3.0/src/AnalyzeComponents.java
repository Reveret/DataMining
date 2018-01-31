import netkit.graph.Graph;
import netkit.graph.Node;
import netkit.graph.Edge;
import netkit.util.*;
import java.io.File;
import java.util.*;

public class AnalyzeComponents {
    public static final String LINKTYPE = "origlink";
    public static final String BS_DELIM = ":";
    
    public static void main(String[] args) {
	for(String s : args) {
	    File f = new File(s);
	    System.out.println("=========================================");
	    System.out.println("Reading graph from file "+s);
	    Graph g = netkit.graph.io.SchemaReader.readSchema(f);
	    GraphMetrics metrics = g.getMetrics();
	    
	    int nn = (int)metrics.getNumNodes();
	    int nc = (int)metrics.getNumComponents();
	    
	    Node[][] c = new Node[nc][]; // array of components - each component is an array of strings
	    int[] ci = new int[nc]; // next 'index' for component i
	    int[] nb = new int[nc]; // number blog-users for component i
	    Arrays.fill(ci,0);
	    Arrays.fill(nb,0);
	    Map<Integer,Map<String,Integer>> cb = new HashMap<Integer,Map<String,Integer>>();

	    for(int i=0;i<nc;i++) {
		int size=metrics.getComponentSize(i);
		if(size<2)
		    continue;
		c[i] = new Node[size];
	    }

	    // first get component sizes, removing components that do not not have
	    // at least active 2 blog users (has ':' in name, with at least 1 link)
	    // also compute number of blogs and their priors
	    Map<String,Integer> blogSitePriors = new HashMap<String,Integer>();
	    int totBlogs = 0;
	    for(Node n : g.getNodes()) {
		int i = metrics.getComponent(n);
		if(c[i]==null)
		    continue;
		String nm = n.getName();
		c[i][ci[i]] = n;
		ci[i]++;
		if(nm.contains(BS_DELIM)) {
		    int numb=0;
		    String[] parts = nm.split(BS_DELIM,2);
		    if(blogSitePriors.containsKey(parts[0]))
			numb=blogSitePriors.get(parts[0]);
		    blogSitePriors.put(parts[0],numb+1);
		    totBlogs++;

		    // if this is not an active user, continue
		    boolean active=false;
		    for(Edge e : n.getEdgesByType(LINKTYPE)) {
			if(e.getDest() != n)
			    active=true;
		    }
		    if(!active)
			continue;
		    nb[i]++;
		    Map<String,Integer> blogs = cb.get(i);
		    if(blogs == null) {
			blogs = new HashMap<String,Integer>();
			cb.put(i,blogs);
		    }
		    numb=0;
		    if(blogs.containsKey(parts[0]))
			numb=blogs.get(parts[0]);
		    blogs.put(parts[0],numb+1);
		}
	    }

	    
	    int newTot = totBlogs;
	    int nbs=0;
	    String[] keys = blogSitePriors.keySet().toArray(new String[0]);
	    Map<String,Integer> blogNameIdx = new HashMap<String,Integer>();
	    List<String> blogNamesList = new ArrayList<String>();
	    for(String bnm : keys) {
		int prior = blogSitePriors.get(bnm);
		if(((double)prior/(double)totBlogs) < 0.01) {
		    newTot -= prior;
		    blogSitePriors.remove(bnm);
		} else {
		    blogNameIdx.put(bnm,nbs);
		    blogNamesList.add(bnm);
		    nbs++;
		}
	    }
	    totBlogs = newTot;

	    String[] blogNames = blogNamesList.toArray(new String[0]);
	    double[][] rMatrix = new double[nbs][5]; // numEdges, numReciprocal, numEdgesToSameBlogSite, numReciprocalToSameBlogSite, numSelfSites
	    for(Edge e : g.getEdges(LINKTYPE)) {
		Node n1 = e.getSource();
		Node n2 = e.getDest();
		if(!n1.getName().contains(BS_DELIM) || !n2.getName().contains(BS_DELIM))
		    continue;
		if(n2.getUnweightedDegree(e.getEdgeType())==0)
		    continue;
		String[] nm1 = n1.getName().split(BS_DELIM,2);
		String[] nm2 = n2.getName().split(BS_DELIM,2);
		if(!blogNameIdx.containsKey(nm1[0]) || !blogNameIdx.containsKey(nm2[0]))
		    continue;
		int idx1 = blogNameIdx.get(nm1[0]);
		int idx2 = blogNameIdx.get(nm2[0]);
		rMatrix[idx1][0]++;
		if(idx1==idx2)
		    rMatrix[idx1][2]++;
		if(n1==n2)
		    rMatrix[idx1][4]++;
		else {
		    for(Edge e2 : n2.getEdgesByType(LINKTYPE)) {
			if(e2.getDest()==n1) {
			    rMatrix[idx1][1]++;
			    if(idx1==idx2)
				rMatrix[idx1][3]++;
			}
		    }
		}
	    }

	    int ns=nn;
	    int rnc=0;
	    for(int i=0;i<nc;i++) {
		if(nb[i] < 2)
		    continue;
		rnc++;
		ns -= c[i].length;
	    }

	    System.out.println("Num-nodes      : "+nn);
	    System.out.println("Num-singletons : "+ns);
	    System.out.println("Num-components : "+rnc);

	    double[] priors = new double[nbs];
	    for(int i=0;i<nbs;i++) {
		String bnm = blogNames[i];
		int prior = blogSitePriors.get(bnm);
		priors[i] = (double)prior/(double)totBlogs;
		System.out.println("Blog-site-count            : "+bnm+" : "+prior+" : "+priors[i]);
		System.out.println("Blog-site-numEdges         : "+bnm+" : "+(int)rMatrix[i][0]);
		System.out.println("Blog-site-selfEdges        : "+bnm+" : "+(int)rMatrix[i][2]);
		System.out.println("Blog-site-userSelfEdges    : "+bnm+" : "+(int)rMatrix[i][4]);
		System.out.println("Blog-site-reciprocity      : "+bnm+" : "+(rMatrix[i][1]/rMatrix[i][0]));
		System.out.println("Blog-site-site-reciprocity : "+bnm+" : "+(rMatrix[i][3]/rMatrix[i][0]));
	    }

	    System.out.print("Component-sizes");
	    for(int i=0;i<nc;i++) {
		if(!cb.containsKey(i))
		    continue;
		System.out.print(","+c[i].length);
	    }
	    System.out.println();
	    
	    final double log2 = Math.log(2D);
	    for(int i=0;i<nc;i++) {
		Map<String,Integer> blogs = cb.get(i);
		if(blogs==null)
		    continue;
		keys = blogs.keySet().toArray(new String[0]);
		for(String bn : keys) {
		    if(!blogSitePriors.containsKey(bn))
			blogs.remove(bn);
		}
		System.out.println("Component-"+i);
		System.out.println("C-"+i+" : Num-nodes     : "+c[i].length);
		System.out.println("C-"+i+" : Num-bloggers  : "+nb[i]);
		System.out.println("C-"+i+" : Num-blogsites : "+blogs.size());
		double tot = 0;
		for(int num : blogs.values())
		    tot += num;
		double max = 0;
		for(String bn : blogs.keySet()) {
		    int num = blogs.get(bn);
		    if(num>max) max = num;
		    int exp = (int)(tot*priors[blogNameIdx.get(bn)]+0.5);
		    System.out.println("C-"+i+" : Blog-site : "+bn+" : "+num+" : "+exp+" : ("+(num-exp)+")");
		}
		System.out.println("C-"+i+" : Purity : "+(max/tot));

		double S = 0;
		double maxS = 1;
		if(blogs.size()>1) {
		    double prob = 1D/blogs.size();
		    maxS = -blogs.size()*(prob*Math.log(prob)/log2);
		    for(String bn : blogs.keySet()) {
			prob = blogs.get(bn) / tot;
			S -= prob*Math.log(prob)/log2;
		    }
		}
		System.out.println("C-"+i+" : Entropy : "+S);
		System.out.println("C-"+i+" : NormalizedEntropy : "+S/maxS);

		// compute density and reciprocity scoresn
		int maxE = c[i].length * (c[i].length-1);
		int numE = 0;
		int activeNumE = 0;
		int reciprocal = 0;
		int activeReciprocal = 0;
		int numSelf = 0;
		int numActive = 0;
		int[] degree = new int[c[i].length];
		Arrays.fill(degree,0);
		int nidx=0;
		for(Node n : c[i]) {
		    boolean self = false;
		    boolean active = false;
		    for(Edge e : n.getEdgesByType(LINKTYPE)) {
			Node nbr = e.getDest();
			if(nbr == n) {
			    self = true;
			    continue;
			}
			active = true;
			int cidx = metrics.getComponent(nbr);
			if(cidx == i) {
			    numE++;
			    degree[nidx]++;
			    boolean oActive = false;
			    boolean eReciprocal = false;
			    for(Edge nbre : nbr.getEdgesByType(LINKTYPE)) {
				if(nbre.getDest() == n)
				    eReciprocal=true;
				else
				    oActive = true;
			    }
			    if(eReciprocal)
				reciprocal++;
			    if(oActive) {
				activeNumE++;
				if(eReciprocal)
				    activeReciprocal++;
			    }

			}
		    }
		    if(active)
			numActive++;
		    if(self)
			numSelf++;
		    nidx++;
		}
		int maxActiveNumE = numActive * (numActive-1);
		Arrays.sort(degree);
		System.out.println("C-"+i+" : NumActive      : "+numActive);
		System.out.println("C-"+i+" : RatioActive    : "+((double)numActive/(double)c[i].length));
		System.out.println("C-"+i+" : NumSelflinks   : "+numSelf);
		System.out.println("C-"+i+" : RatioSelflinks : "+(double)numSelf/(double)numActive);
		System.out.println("C-"+i+" : Density        : "+(double)numE/(double)maxE);
		System.out.println("C-"+i+" : ActiveDensity  : "+(maxActiveNumE>0 ? (double)activeNumE/(double)maxActiveNumE : Double.NaN));
		System.out.println("C-"+i+" : Reciprocity  : "+(double)reciprocal/(double)numE);
		System.out.println("C-"+i+" : ActiveReciprocity  : "+(maxActiveNumE>0 ? (double)activeReciprocal/(double)maxActiveNumE : Double.NaN));
		System.out.print("C-"+i+" : Degree       : "+degree[degree.length-1]);
		for(int idx=degree.length-2;idx>=0;idx--)
		    System.out.print(","+degree[idx]);
		System.out.println();

		for(Node n : c[i]) {
		    System.out.println("C-"+i+" : Member : "+n.getName());
		}
	    }
	}
    }
}
