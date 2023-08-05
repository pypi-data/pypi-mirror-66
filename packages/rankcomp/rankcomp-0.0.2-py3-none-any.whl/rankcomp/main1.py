# coding: utf-8
import time
import os
from multiprocessing import Pool
import get_reverse_index
import utils
import load_data
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.cross_validation import train_test_split
import pandas as pd
import p_selection
import feature_selection
t1=time.time()
##################################################setting#############################################
env="linux"
###for scRNA
bulk=False
sc_dir_list_raw_train=["data//clst_1_case_T.txt","data//clst_1_ctrl_T.txt"]
hint_list=[1,0]
root_dir=os.getcwd()
pj=lambda *path: os.path.abspath(os.path.join(*path))
#################################################pickle loading######################################
##these data should be transposed,colname=genes,rownames=samples
print("For the whole data we loaded:")
x_train=pickle.load(open(pj(root_dir,"result/RIFpj_clst_1_train_matrix_ovlp.pickle"),"rb"))
y_train=pickle.load(open(pj(root_dir,"result/RIFpj_clst_1_train_label_ovlp.pickle"),"rb"))
y_train=np.array(y_train)
x_test=pickle.load(open(pj(root_dir,"result/RIFpj_clst_1_test_matrix_ovlp.pickle"),"rb"))
y_test=pickle.load(open(pj(root_dir,"result/RIFpj_clst_1_test_label_ovlp.pickle"),"rb"))
y_test=np.array(y_test)
#################################################loading data########################################
#print("For the whole data we loaded:") 
#filter_gene="data/RIF_gene.txt"
#train_data=load_data.gene_data(sc_dir_list_raw_train,filter_gene,env)
#train_matrix=train_data.get_matrix_app(hint_list,bulk=False)
#print(train_matrix.shape)
#train_label=train_data.gene_label(bulk=bulk,bulk_dir=None)
#print(train_label.shape)
#train_x,test_x,train_y,test_y=train_test_split(train_matrix,train_label,test_size=0.2,random_state=0)
#####################################################################################################
print("Train matrix shape: %s" % str(x_train.shape))
print("Test matrix shape: %s" % str(x_test.shape))
print("Train label shape: %s" % str(y_train.shape[0]))
print("Test label shape: %s" % str(y_test.shape[0]))
#############################################fundamental setting######################################
typ="rank"
thre_type = 'fdr'
pvalue_list=[i for i in np.logspace(-47,-42,10)]
k_feature_lst=[i for i in range(5,50)]
err=50
exp=500
############################################getting the optimized pvalue##############################
print("Training the model...")
optimiazed_p=p_selection.plot_optimized_pvalue(pvalue_list,x_train,y_train,True,err,exp)
print("The optimized pvalue has been selected\n more option should be changed in the dir of ./figure/Pvalue_selection.pdf\n about top 500 pairs are selected\n if you want more, you can also change it by yourself!!!")
############################################main loop#################################################
#get_optimized_feature(k_feature_lst,threshold,x_train,y_train,index,c,d,num_raw_pair,typ,x_test,y_test,thre_type)
t2=time.time()
elapse=t2-t1
print("The full task elapsing: %s" % str(elapse))

