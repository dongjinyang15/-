#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random

data_train=pd.read_csv('D:/python/hw1/train.csv',encoding='big5')


# In[2]:


data_train=np.array(data_train.iloc[:,3:])


# In[3]:


for i in range(data_train.shape[0]):
    for j in range(data_train.shape[1]):
        if data_train[i,j]!='NR':
            data_train[i,j]=float(data_train[i,j])
        else:
            data_train[i,j]=0
#data_train=(data_train-data_train.mean())/data_train.std()


# In[4]:


train=np.zeros(shape=(240,24))
for i in range(240):
    train[i,:]=data_train[18*i+9,:]


# In[5]:


train=train.reshape((-1,20,24))


# In[11]:


train.shape


# In[6]:


data_train=np.zeros((12*15,20,10))
for i in range(15):
    data_train[12*i:12*(i+1),:,:]=train[:,:,i:i+10]


# In[13]:


data_train


# In[14]:


data_train.shape


# In[7]:


data_train=data_train.reshape((-1,10))


# In[8]:


label=np.zeros((data_train.shape[0],1))
for i in range(data_train.shape[0]):
    label[i]=data_train[i,9]


# In[9]:


data=data_train[:,:9]


# In[10]:


train_num=3000
data_train=data[:train_num,:]
data_val=data[train_num:,:]
label_train=label[:train_num,:]
label_val=label[train_num:,:]


# In[11]:


ls=list(range(data_train.shape[0]))
random.shuffle(ls)
data_train_shuffled=np.zeros_like(data_train)
label_train_shuffled=np.zeros_like(label_train)
for i in range(data_train.shape[0]):
    data_train_shuffled[i,:]=data_train[ls[i],:]
    label_train_shuffled[i,:]=label_train[ls[i],:]


# In[20]:


len(ls)


# In[12]:


weight=np.random.normal(scale=0.01,size=(9,1))
b=0
num_epochs=50
batch_size=300
batch=10
eps = 0.00000001
adagrad = np.zeros((9,1))
lr=0.0000005
for epoch in range(num_epochs):
    for bat in range(batch):
        data=data_train_shuffled[bat*batch_size:(bat+1)*batch_size,:]
        label=label_train_shuffled[bat*batch_size:(bat+1)*batch_size,:]
        pred=np.dot(data,weight)#+b
        loss=np.sqrt(0.5*np.mean(np.power((pred-label),2)))
        grad_w=np.dot(data.transpose(),(pred-label))
        grad_b=np.mean(pred-label)
        adagrad+=np.power(grad_w,2)
        #lr/=(adagrad+eps)
        weight-=lr*grad_w
        b-=lr*grad_b
        print(loss)


# In[17]:


np.sqrt(np.power((np.dot(data_val,weight)-label_val),2)).mean()

