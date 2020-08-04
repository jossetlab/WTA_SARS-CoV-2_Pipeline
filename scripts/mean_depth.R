argv <- commandArgs(TRUE)

input<-as.character(argv[1])
output<-as.character(argv[2])

depth_table<-read.table(input,sep="\t",header=T)
depth_table<-depth_table[,-c(1,2,3)]
Mean_Cov<-aggregate(depth_table$coverage, list(depth_table$sample_ID), function(x) mean(x))
colnames(Mean_Cov)<-c("SAMPLE","MEAN")

write.table(Mean_Cov,output,sep="\t",quote = F , row.names = F)
