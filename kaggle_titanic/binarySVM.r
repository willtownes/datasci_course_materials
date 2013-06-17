#library(e1071)
#help(libsvm)
library(kernlab)
library(ROCR)
#help(ksvm)
dataPrep<-function(dat){
  dat$survived<-as.factor(dat$survived)
  dat$pclass<-as.factor(dat$pclass)
  dat<-na.omit(within(dat,rm(ticket,cabin,embarked)))
  return(dat)
}
imputeGaussian<-function(vec){
  #takes a vector with some NAs, and replaces the NAs with random variates drawn from the normal distribution having mean and stdev of the non-missing parts of the vector
  missing<-which(is.na(vec))
  nonmissing<-which(!is.na(vec))
  vec[missing]<-rnorm(length(missing),mean=mean(nonmissing),sd=sd(nonmissing))
  return(vec)
}
splitIndex<-function(dat,folds=10){
  #given a dataset, returns a list of 10 (or value specified) chunks
  #each chunk is a vector of indices on the rows of the dataset provided
  #the list of chunks can be used to partition the dataset for k-fold cross validation
  n<-nrow(dat)
  index<-sample(1:n)
  chunks<-split(index,1:folds)
  return(chunks)
}
svmClassifier<-function(dat,nu,chunks){
  # train SVM classifier on the data (assumes class indicator is first column, and uses all other columns as predictors). Returns a list of predicted values (each slot from a different cross validation) and a list of true values (each slot from a different cross validation).
    # kernel=rbfdot means Gaussian Kernel
    # nu determines the threshold fraction of training set cases considered anomalies.This is the crucial parameter to be optimized
  folds<-length(chunks)
  preds<-vector("list",folds) #empty list container for predicted values
  truths<-vector("list",folds) #empty list container for true values
  for(k in 1:folds){
    #print(length(chunks[[k]]))
    test<-dat[chunks[[k]], ]
    truths[[k]]<-test[,1] #first column only is true values
    xtest<-test[,-1] #all but the first column
    train<-dat[-chunks[[k]], ]
    model<-ksvm(survived~. ,data=train,type='nu-svc',kernel='rbfdot',nu=nu,prob.model=T)
    preds[[k]]<-predict(model,xtest,type='probabilities')[,"1"]
  }
  return(list(preds=preds,truths=truths))
}

# read in data
data1<-read.csv("train.csv",header=T,row.names=3)
dat1<-dataPrep(data1)
chunks<-splitIndex(dat1,folds=20)

# Try many different values of nu, each with same 10x cross validation, and compare them using area under vertically averaged ROC.
nu<-c(.4,.5,.6,.65,.7,.75)
#nu<-c(.01,.1)
K<-length(chunks)
auc<-matrix(NA,nrow=K,ncol=length(nu),dimnames=list(NULL,as.character(nu)))
for(v in nu){
  res<-svmClassifier(dat1,v,chunks)
  rocr.pred<-prediction(res$preds,res$truths)
  perfs<-performance(rocr.pred,measure="auc")
  auc[,as.character(v)]<-unlist(perfs@y.values)
}
# perfs is now a matrix whose rows represent cross validation folds, columns represent different values of nu, and values represent area-under-ROC.
tvals<-apply(auc,2,FUN=function(col){(mean(col)-.5)*sqrt(K-1)/sd(col)})
# we select as the best nu whichever has the largest t-statistic.

# Graph ROC for 20 different cross validations, all with nu=0.6
nu<-.6
res1<-svmClassifier(dat1,nu,chunks)
rocr.pred<-prediction(res1$preds,res1$truths)
perf<-performance(rocr.pred,measure="tpr",x.measure="fpr")
plot(perf,col="grey82",lty=3)
# overlay the vertical-averaged curve, still with nu=0.1
plot(perf,lwd=3,avg="vertical",spread.estimate="boxplot",add=T)
abline(0,1) #for comparison

# more model validations, using whole training set.
nus<-c(.3,.4,.5,.6)
train.err<-rep(NA,length(nus))
cross.err<-rep(NA,length(nus))
models<-list()
names(train.err)<-names(cross.err)<-as.character(nus)
for(i in nus){
  models[[as.character(i)]]<-model<-ksvm(survived~. ,data=dat1,type='nu-svc',kernel='rbfdot',nu=i,cross=20)
  train.err[as.character(i)]<-error(model)
  cross.err[as.character(i)]<-cross(model)
}
cbind(train.err,cross.err)
# based on this, we choose nu=.4 (same as .6 except different ordering of the levels of the response variable?)

# Read in test data and write out the predicted values for the test data
test.data<-read.csv('test.csv',header=T,row.names=2)
test.data$age<-imputeGaussian(test.data$age) #fill in missing values
test.data$fare<-imputeGaussian(test.data$fare)
dat2<-within(test.data,{
  pclass<-as.factor(pclass)
  rm(ticket,cabin,embarked)
})
test.preds<-predict(models[["0.4"]],dat2)
stopifnot(length(test.preds)==nrow(dat2)) #sanity check
write.table(test.preds,file="predictions.csv",row.names=F,col.names=F,sep=",")