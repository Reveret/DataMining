#Include
library(cluster)

# Input
s2 <-read.table("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dataset/s2.txt")
seed <-read.table("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dataset/seeds_dataset.txt")
dim032 <-read.table("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dataset/dim032.txt")



# ----------------------------------------- Diana -----------------------------------------
jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_dim032")
plot(diana(dim032))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_dim032_metric_manhattan")
plot(diana(dim032, metric="manhattan"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_dim032_stand_T")
plot(diana(dim032, stand=T))
dev.off()

#----------------------------------------------------
jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_seed")
plot(diana(seed, metric="manhattan"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_seed_metric_manhattan")
plot(diana(seed))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_seed_stand_T")
plot(diana(seed, stand=T))
dev.off()

#-----------------------------------------------------
jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_s2")
plot(diana(s2, metric="manhattan"))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_s2_metric_manhattan")
plot(diana(s2))
dev.off()

jpeg("~/Dokumente/uni/17-18_ws/DataMining/sheet04/dendogram/diana_s2_stand_T")
plot(diana(s2, stand=T))
dev.off()













