
# coding: utf-8

# In[52]:


import pandas as pd
import os
import utils
import numpy as np
from sklearn.cross_validation import train_test_split

# In[70]:


##File preparation

class gene_data():
    def __init__(self,sc_dir_list_raw,filter_dir_raw,env):
        self.sc_dir_list_raw=sc_dir_list_raw
        self.filter_dir_raw=filter_dir_raw
        self.env=env
        self.label=""
    def get_matrix_app(self,hint_list,bulk):
        file_root=os.getcwd()
        pj=lambda *path: os.path.abspath(os.path.join(*path))
        if self.filter_dir_raw != None:
            filter_path=pj(file_root,self.filter_dir_raw)
            filter_table=pd.read_table(filter_path,sep=" ")
            Symbol_filter=filter_table["Symbol"]
            print("The number of current RIF related gene is:%d" % len(Symbol_filter))
        sc_table=[]
        sc_data_list=self.sc_dir_list_raw
        if hint_list!=None:
            for sc_data,hint in zip(sc_data_list,hint_list):
                sc_path=pj(file_root,sc_data)
                this_df=pd.read_table(sc_path,sep=",")
                s_num=this_df.shape[0]
                print(s_num)
                self.label+=str(hint)*s_num
                sc_table.append(this_df)
        elif hint_list==None:
            sc_data_dir=self.sc_dir_list_raw
            sc_path=c_dir(file_root,sc_data_dir)
            s_num=pd.read_table(sc_path,sep="\t",index_col=[0]).shape[1]
            sc_table.append(pd.read_table(sc_path,sep="\t",index_col=[0]))
        if len(sc_table)>=2:
            sc_table_all=pd.concat(sc_table,axis=0)
        elif len(sc_table)==1:
            sc_table_all=sc_table[0]
        print("The number of scRNA RIF gene is:%d" % sc_table_all.shape[0])
        Symbol_sc=list(sc_table_all.columns)
        if bulk==False and self.filter_dir_raw != None:
            over_count,over_gene=utils.overlap(Symbol_filter,Symbol_sc)
            print("The number of overlap genes: %d" % over_count)
            sc_table_all=sc_table_all.loc[:,over_gene]
        elif bulk==True:
            sc_table_all=sc_table_all.iloc[0:5000]
        return sc_table_all

    def get_matrix(self,hint_list,bulk):
        file_root=os.getcwd()
        c_dir=lambda *path: os.path.abspath(os.path.join(*path))
        if bulk==False and self.filter_dir_raw != None:
            filter_path=c_dir(file_root,filter_dir)
            filter_table=pd.read_table(filter_path,sep="\t",index_col="tax_id")
            Symbol_filter=filter_table["Symbol"]
            print("The number of current RIF related gene is:%d" % len(Symbol_filter))
        sc_table=[]
        sc_data_list=self.sc_dir_list_raw
        if hint_list!=None:
            for sc_data,hint in zip(sc_data_list,hint_list):    
                sc_path=c_dir(file_root,sc_data)
                s_num=pd.read_table(sc_path,sep=",").shape[1]
                self.label+=str(hint)*s_num
                sc_table.append(pd.read_table(sc_path,sep=" "))
        elif hint_list==None:
            sc_data_dir=self.sc_dir_list_raw
            sc_path=c_dir(file_root,sc_data_dir)
            s_num=pd.read_table(sc_path,sep="\t",index_col=[0]).shape[1]
            sc_table.append(pd.read_table(sc_path,sep="\t",index_col=[0]))            
        if len(sc_table)>=2:
            sc_table_all=pd.concat(sc_table,axis=1)
        elif len(sc_table)==1:
            sc_table_all=sc_table[0]
        print("The number of scRNA RIF gene is:%d" % sc_table_all.shape[0])
        Symbol_sc=sc_table_all.index
        ##挑选出相应的scRNA_seq数据
        if bulk==False:
            if self.filter_dir_raw != None:
                over_count,over_gene=utils.overlap(Symbol_filter,Symbol_sc)
                print("The number of overlap genes: %d" % over_count)
                sc_table_all=sc_table_all.loc[over_gene,:]
        elif bulk==True:
            sc_table_all=sc_table_all.iloc[0:5000]
        return sc_table_all
    def gene_label(self,bulk,bulk_dir):##the ratio is the positive/negative
        if bulk:
            file_root=os.getcwd()
            c_dir=lambda *path: os.path.abspath(os.path.join(*path))
            bulk_path=c_dir(file_root,bulk_dir)
            all_label=pd.read_table(bulk_path,sep="\t",usecols=[0,2],index_col=[0],header=None)
            all_label.columns=["label"]
        else:
            label_list=[int(label_) for label_ in self.label]
            all_label=pd.DataFrame(label_list,columns=["labels"])
        return all_label


def check(df,genes):
    all_genes=df.columns
    not_in=[i for i in genes if i not in all_genes]
    if len(not_in)!=0:
        print("%d genes served as mismatch gene in the test dataset!!!pls check it or change the initial code!!!" % len(not_in))
        print("They are: %s" % str(not_in))
        return not_in
    else:
        print("all the gene matched")
        return None
   
class gene_test():
    def __init__(self,test_file,label):
        self.test_file=test_file
        self.label=label
    def gene_matrix(self):
        pj=lambda *path: os.path.abspath(os.path.join(*path))
        root=os.getcwd()
        f=pd.read_table(pj(root,"data/test_bulk/%s" % self.test_file),index_col=[0],sep=" ")
        return f.T
    def gene_label(self):
        pj=lambda *path: os.path.abspath(os.path.join(*path))
        root=os.getcwd()
        lb=pd.read_table(pj(root,"data/test_bulk/%s" % self.label),index_col=["Sample"],sep=" ",usecols=[1,2])
        return lb

        
#get matrix
if __name__=="__main__":
    ##setting the exvironment:
    env="win"##win or linux
    sc_dir_list_raw=["data//casemay10_test.txt","data//ctrlmay10_test.txt"]
    ncbi_dir="data//NCBI_leukemia_mm_gene.txt"
    data=gene_data(sc_dir_list_raw,ncbi_dir,"win")
    data_matrix=data.get_matrix()
    all_label=data.gene_label(ratio=0.5)
#     print(data_matrix)


# In[63]:


#a=np.array([1,2])
#b=np.array([2,3])
#c=np.hstack((a,b))
#print(c)

