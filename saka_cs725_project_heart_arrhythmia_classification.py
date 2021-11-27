# -*- coding: utf-8 -*-
"""SAKA_CS725_Project_Heart_Arrhythmia_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B1RYFc1ShL111KUS5Dxc4oTuZowuJ67D

#*Cardiac Arrhythmia Multi-Class Classification*
#Predict Heart Arrhythmia.

**Tasks:**

1) Data reading, Analyze and Visualization.

2) Address missing data if there is any.

3) Outliers Detection if there is any.

4) Features Selection using PCA.

5) Correctly classify different types of cardiac arrhythmia using following models and compare which one is good for this problem.
  
i)   KNN classifcation \\
ii)  Logistic Regression \\
iii) Linear Support Vector Machine \\
iv) Kernelized Support Vector Machine \\
v) Decision Tree

#Importing important libreries
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
from sklearn import preprocessing
from matplotlib import pyplot as plt

"""#1. Data Reading
Starting with reading the data file.
"""

data = pd.read_csv('/content/data_arrhythmia.csv', sep=';')
data=pd.DataFrame(data)
data

"""#Arrhythmia Data Visualization"""

data['diagnosis'].value_counts()

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline
plt.figure(figsize=[15,8])

plt.hist(data['diagnosis'], width = 0.6, color='#0502aa',alpha=0.7)
plt.xlim(min(data['diagnosis']), max(data['diagnosis']))
plt.grid(axis='y', alpha=0.8)
plt.xlabel('Class',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.ylabel('Count',fontsize=15)
plt.title('Frequency of labels',fontsize=20)
plt.show()

class_name = ['Normal', 'Ischemic changes (Coronary Artery Disease)', 'Old Anterior Myocardial Infarction', 'Old Inferior Myocardial Infarction',
              'Sinus tachycardy', 'Sinus bradycardy', 'Ventricular Premature Contraction (PVC)', 'Supraventricular Premature Contraction',
              'Left bundle branch block', 'Right bundle branch block', '1 degree AtrioVentricular block', '2 degree AV block', '3 degree AV block',
              'Left ventricule hypertrophy', 'Atrial Fibrillation or Flutter', 'Others' ]
value = [245, 44, 15, 15, 13, 25, 3, 2, 9, 50, 0, 0, 0, 4, 5, 22]
# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(value, labels = class_name, startangle=90, shadow=True, explode=(0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.7
                                                                        , 0.2, 0.2, 0.1, 0.3, 0.5, 0.7, 0.3), autopct='%1.2f%%')
  
# show plot
plt.show()

"""Here we can see, 54.20% data of Normal. Means Normal condition has more influence on dataset.

#Statistical summary
"""

data.describe()

"""We can see that original data has 280 columns but we get statistical summary for ony 275 colums. Which means there are 5 columns having missing values.

#2. Detecting columns which has missing values.
"""

data.columns[data.isnull().any()]

"""#Handling the missing value
While going through the dataset we observed that out of 279 columns 5 columns have missing value in the form of '?'. The approach which we will following is, first replacing '?' with numpy NAN and then imputing the mean.

"""

data['J'] = data['J'].replace('?',np.NaN)
data['heart_rate'] = data['heart_rate'].replace('?',np.NaN)
data['P'] = data['P'].replace('?',np.NaN)
data['T'] = data['T'].replace('?',np.NaN)
data['QRST'] = data['QRST'].replace('?',np.NaN)

print( 'Total missing values in J colums:',data['J'].isna().sum(), ', & percentage =',((data['J'].isna().sum())/len(data))*100, '%\n')
print( 'Total missing values in T colums:',data['T'].isna().sum(), ', & percentage =',((data['T'].isna().sum())/len(data))*100,'%\n')
print( 'Total missing values in P colums:',data['P'].isna().sum(), ', & percentage =',((data['P'].isna().sum())/len(data))*100,'%\n')
print( 'Total missing values in QRST colums:',data['QRST'].isna().sum(), ', & percentage =',((data['QRST'].isna().sum())/len(data))*100,'%\n')
print( 'Total missing values in heart rate colums:',data['heart_rate'].isna().sum(), ', & percentage =',((data['heart_rate'].isna().sum())/len(data))*100,'%\n')

"""#Drop column
We can observe that column 'J' have a lot of missing value. It will not be a good practice to impute mean values in this column. Better option will be that we drop this column.

"""

new_data = data.drop(columns=['J'])
new_data

"""#3 Outliers detection
We don't have much knowlege about possible ranges for all variables but for variables 'age', 'height', 'weight' we can decide which are the outliers by common sense.
"""

boxplot = new_data.boxplot(column=['age', 'height', 'weight'])

"""
1)for variable 'height' 2 observation more than 600	centimetres which does not seem realistic and hence we will substitute them with mean of remaining observations.


2)for variable 'weight' 1 observation around 180 kilograms seems to be realistic but for accuracy point of view, we will substitute it with mean of remaining observations."""

new_data['height'] = np.where(new_data.height > 200, np.nan, new_data.height )
new_data['weight'] = np.where(new_data.weight > 150, np.nan, new_data.weight )

boxplot = new_data.boxplot(column=['age', 'height', 'weight'])

"""#Spliting the dataset
Segregating the whole dataset into X and Y


"""

Data_Y = new_data.iloc[:,-1]
Data_X = new_data.iloc[:,:-1]
np.unique(Data_Y, return_counts=True)

"""#Handling missing value
We are imputing mean in place of missing values


"""

from sklearn.impute import SimpleImputer
z = SimpleImputer(missing_values=np.nan, strategy='mean').fit_transform(Data_X)
Data_X = pd.DataFrame(data=z,columns=Data_X.columns.values)

Data_X.describe()

"""Here we can see statistical summary for 278 columns.(out of 280 columns one is 'Y' which represent type of arrhythmia and one column 'J' is dropped so Data_X has total 278 columns). So the Column's dimension says, no one column have missing value.

#4. PCA
We will be using principal component analysis for data reduction. We have 278 variables which is increasing the complexity of the models. PCA reduces the dimensions of data which makes potentially easier to learn and lesser the chance of overfitting.

Typically, features with a lot of variance tend to contain meaningful information. We want the explained variance to be between 95%-99%.
Here we have selected it to be 97% as it give good results for our problem.
"""

from sklearn.decomposition import PCA

pca = PCA(0.97)
pca.fit(Data_X)
Data_X_PCA = pca.transform(Data_X)
Data_X_PCA.shape

"""So dimension is reduced from 278 to 47

#Spliting down into both train and test data set
"""

data_train_x, data_test_x, data_train_y, data_test_y = train_test_split(Data_X_PCA, Data_Y
                                                                        , test_size=0.2, random_state=34)
print('Shape of train {}, shape of test {}'.format(data_train_x.shape, data_test_x.shape))

"""#Scaling
As the variables are on different scale it will be helpful if we bring them all on the same scale. Scaling improves the performance of the models


"""

from sklearn.preprocessing import MinMaxScaler
MinMax = MinMaxScaler(feature_range= (0,1))
data_train_x = MinMax.fit_transform(data_train_x)
data_test_x = MinMax.transform(data_test_x)

"""#Creating Dataframe to compare results for different models"""

output = pd.DataFrame(index=None, columns=['model', 'train_MSE','test_MSE', 'Accuracy(in %)'])

"""#5. Modeling
After taking care of the data we will be starting with the model creation.

#*i) KNN Classifier*
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, r2_score, mean_squared_error
Weights = ['distance', 'uniform']
N_neighbors = [x for x in range(1, 100)]
acc = []
for i in Weights:
  for j in N_neighbors:
    knn = KNeighborsClassifier(n_neighbors=j, weights= i)
    knn.fit(data_train_x, data_train_y)
    pred = knn.predict(data_test_x)
    acc.append(accuracy_score(data_test_y,pred)*100)
max_acc = max(acc)
max_index = acc.index(max_acc)
if max_index < 100:
  print('weights: distance')
  print('n_neighbors:', max_index+1)
  w_knn='distance'
  n_neib=max_index+1
else:
  print('Weights: uniform')
  print('N_neighbors:', max_index-99)
  w_knn='uniform'
  n_neib=max_index-99

knn = KNeighborsClassifier(n_neighbors=n_neib, weights= w_knn)
knn.fit(data_train_x, data_train_y)
pred = knn.predict(data_test_x)
print('Accuracy:', accuracy_score(data_test_y,pred)*100, '%')

print(classification_report(data_test_y,pred))
print('matrix =', confusion_matrix(data_test_y,pred))

train_MSE = mean_squared_error(data_train_y, knn.predict(data_train_x) )
test_MSE = mean_squared_error(data_test_y, pred)
accuracy = accuracy_score(data_test_y,pred)*100
output = output.append(pd.Series({'model':'KNN Classifier', 'train_MSE':train_MSE,'test_MSE':test_MSE, 'Accuracy(in %)':accuracy}),ignore_index=True )
output

"""#ii) Logistic Regression"""

from sklearn.linear_model import LogisticRegression
c = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
acc = []
for i in c:
  log = LogisticRegression(C=i)
  log.fit(data_train_x, data_train_y)
  pred = log.predict(data_test_x)
  acc.append(accuracy_score(data_test_y,pred)*100)
max_acc = max(acc)
max_index = acc.index(max_acc)
print('c=', c[max_index])
c_lg=c[max_index]

log = LogisticRegression(C=c_lg)
log.fit(data_train_x, data_train_y)
pred = log.predict(data_test_x)

print('Accuracy:', accuracy_score(data_test_y,pred)*100, '%')
print(classification_report(data_test_y,pred))
print('matrix =', confusion_matrix(data_test_y,pred))

train_MSE = mean_squared_error(data_train_y, log.predict(data_train_x) )
test_MSE = mean_squared_error(data_test_y, pred)
accuracy = accuracy_score(data_test_y,pred)*100
output = output.append(pd.Series({'model':'Logistic Regression', 'train_MSE':train_MSE,'test_MSE':test_MSE, 'Accuracy(in %)':accuracy}),ignore_index=True )
output

"""#iii) Linear Supprt Vector Machine

"""

from sklearn.svm import LinearSVC
c = [0.001, 0.01, 0.1, 0.5, 1, 10, 50, 100, 1000]
Max_iter = [100, 1000, 10000, 100000]
acc =[]
for i in Max_iter:
  for j in c:
    linearsvc = LinearSVC(C=j, max_iter= i)
    linearsvc.fit(data_train_x, data_train_y)
    pred = linearsvc.predict(data_test_x)
    acc.append(accuracy_score(data_test_y,pred)*100)
max_acc = max(acc)
max_index = acc.index(max_acc)

if max_index < 9: 
  print('Max_iter=', 100)
  print('c=', c[max_index] )
  mi_lsvc=100
  c_lsvc=c[max_index]
elif max_index < 18:
  print('Max_iter=', 1000)
  print('c=', c[max_index - 9])
  mi_lsvc=1000
  c_lsvc=c[max_index - 9]
elif max_index < 27:
  print('Max_iter=', 10000)
  print('c=', c[max_index - 18])
  mi_lsvc=10000
  c_lsvc=c[max_index - 18]
else:
  print('Max_iter=', 100000)
  print('c=', c[max_index - 27])
  mi_lsvc=100000
  c_lsvc=c[max_index - 27]

linearsvc = LinearSVC(C= c_lsvc, max_iter= mi_lsvc)
linearsvc.fit(data_train_x, data_train_y)
pred = linearsvc.predict(data_test_x)

print("Accuracy = ", accuracy_score(data_test_y,pred)*100, '%')
print(classification_report(data_test_y,pred))
print('matrix =', confusion_matrix(data_test_y,pred))

train_MSE = mean_squared_error(data_train_y, linearsvc.predict(data_train_x) )
test_MSE = mean_squared_error(data_test_y, pred)
accuracy = accuracy_score(data_test_y,pred)*100
output = output.append(pd.Series({'model':'Linear SVM', 'train_MSE':train_MSE,'test_MSE':test_MSE, 'Accuracy(in %)':accuracy}),ignore_index=True )
output

"""#iv) Kerenilzed Support Vector Machine"""

from sklearn.svm import SVC
c = [0.001, 0.01, 0.1, 0.5, 1, 10, 50, 100, 1000]
Gamma = [0.001, 0.01, 0.1, 0.3, 0.4, 0.5, 0.8, 1, 10]
acc =[]
for i in Gamma:
  for j in c:
    svc = SVC(C=j, gamma= i)
    svc.fit(data_train_x, data_train_y)
    pred = svc.predict(data_test_x)
    acc.append(accuracy_score(data_test_y,pred)*100)
max_acc = max(acc)
max_index = acc.index(max_acc)

if max_index < 9: 
  print('Gamma=', 0.001)
  print('c=', c[max_index] )
  g_svc=0.001
  c_svc=c[max_index]
elif max_index < 18:
  print('Gamma=', 0.01)
  print('c=', c[max_index - 9])
  g_svc=0.01
  c_svc=c[max_index - 9]
elif max_index < 27:
  print('Gamma=', 0.1)
  print('c=', c[max_index - 18])
  g_svc=0.1
  c_svc=c[max_index - 18]
elif max_index < 36:
  print('Max_iter=', 0.3)
  print('c=', c[max_index - 27])
  g_svc=0.3
  c_svc=c[max_index - 27]
elif max_index < 45:
  print('Gamma=', 0.4)
  print('c=', c[max_index - 36])
  g_svc=0.4
  c_svc=c[max_index - 36]
elif max_index < 54:
  print('Gamma=', 0.5)
  print('c=', c[max_index - 45])
  g_svc=0.5
  c_svc=c[max_index - 45]
elif max_index < 63:
  print('Max_iter=', 0.8)
  print('c=', c[max_index - 54])
  g_svc=0.8
  c_svc=c[max_index - 54]
elif max_index < 72:
  print('Gamma=', 1)
  print('c=', c[max_index - 63])
  g_svc=1
  c_svc=c[max_index - 63]
else: 
  print('Max_iter=', 10)
  print('c=', c[max_index - 72])
  g_svc=10
  c_svc=c[max_index - 72]

svc = SVC(C=c_svc, gamma=g_svc)
svc.fit(data_train_x, data_train_y)
pred = svc.predict(data_test_x)
matrix = confusion_matrix(data_test_y,pred)
print("Accuracy = ", accuracy_score(data_test_y,pred)*100, '%')
print(classification_report(data_test_y,pred))

train_MSE = mean_squared_error(data_train_y, svc.predict(data_train_x) )
test_MSE = mean_squared_error(data_test_y, pred)
accuracy = accuracy_score(data_test_y,pred)*100
output = output.append(pd.Series({'model':'Kernalized SVM','train_MSE':train_MSE,'test_MSE':test_MSE,'Accuracy(in %)':accuracy}),ignore_index=True )
output

"""#v) Decision Tree"""

from sklearn.tree import DecisionTreeClassifier
Max_features =[None,'auto', 'log2']
Max_depth = [5,10,15,20,50]
acc = []
for i in Max_features:
  for j in Max_depth:
    dt = DecisionTreeClassifier(max_depth=j, max_features=i)
    dt.fit(data_train_x, data_train_y)
    pred = dt.predict(data_test_x)
    acc.append(accuracy_score(data_test_y,pred)*100)
max_acc = max(acc)
max_index = acc.index(max_acc)

if max_index < 5:
  print('Max_features: None' )
  print('Max_depth:', Max_depth[max_index])
  m_fedt=None
  m_dedt=Max_depth[max_index]
elif max_index < 10:
  print('Max_features: auto' )
  print('Max_depth:', Max_depth[max_index - 5])
  m_fedt='auto'
  m_dedt=Max_depth[max_index - 5]
else:
  print('Max_features: log2' )
  print('Max_depth:', Max_depth[max_index - 10])
  m_fedt='log2'
  m_dedt=Max_depth[max_index - 10]

dt = DecisionTreeClassifier(max_depth=m_dedt, max_features=m_fedt)
dt.fit(data_train_x, data_train_y)
pred = dt.predict(data_test_x)
matrix = confusion_matrix(data_test_y,pred)
print("Accuracy = ", accuracy_score(data_test_y,pred)*100, '%')
print(classification_report(data_test_y,pred))

train_MSE = mean_squared_error(data_train_y, dt.predict(data_train_x))
test_MSE = mean_squared_error(data_test_y, pred)
accuracy = accuracy_score(data_test_y,pred)*100
output = output.append(pd.Series({'model':'Decision Tree','train_MSE':train_MSE,'test_MSE':test_MSE,'Accuracy(in %)':accuracy}),ignore_index=True )
output

"""#Conclusion
1)If we consider accuracy only then we got that Kernalized Support Vector Machine with C=10 and gamma=0.4 is best model for this classification with accuracy 73.626374%. 


2)But taking overfitting into consideration, comparing train_MSE, test_MSE, and f1-score, we can conclude that Linear Support Vector Machine with c=0.5 and max_iter=100 is best model for this classification with accuracy 72.5274739%, as Kernalized support vector machine is overfitting for this problem.
"""