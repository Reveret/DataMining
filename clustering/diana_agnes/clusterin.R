#Include
library(cluster)

# Input
s2 <-read.table("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dataset/s2.txt")
seed <-read.table("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dataset/seeds_dataset.txt")
dim032 <-read.table("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dataset/dim032.txt")


#-------------------------------------------- Agnes --------------------------------------------
jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_dim032")
plot(agnes(dim032))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_dim032_metric_manhattan")
plot(agnes(dim032, metric="manhattan"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_dim032_methods_single")
plot(agnes(dim032, method="single"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_dim032_method_complete")
plot(agnes(dim032, method = "complete"))
dev.off()
#---------------------------------------------------
jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_seed")
plot(agnes(seed))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_seed_metric_manhattan")
plot(agnes(seed, metric="manhattan"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_seed_methods_single")
plot(agnes(seed, method="single"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_seed_method_complete")
plot(agnes(seed, method = "complete"))
dev.off()
#---------------------------------------------------
jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_s2")
plot(agnes(s2))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_s2_metric_manhattan")
plot(agnes(s2, metric="manhattan"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_s2_methods_single")
plot(agnes(s2, method="single"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/agnes_s2_method_complete")
plot(agnes(s2, method = "complete"))
dev.off()







