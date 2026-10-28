import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


# df = pd.read_csv("C:/Users/bakar/OneDrive/Desktop/Master's folder/College_Data.csv")


# print(df.head(25))




from tf_idf import tfidf_X, word_list
from preprocessing import preprocessed_questions
from difficulty_level import tfidf_x_dif_lev_X
from w2v_tfidf_dl import word2vec_tfidf_dl_embeddings, word2vec_embeddings, df_X_WE, tfidf_wordEmb

X = tfidf_X
# X = tfidf_x_dif_lev_X
# X = tfidf_wordEmb
# X = df_X_WE
# X = word2vec_embeddings
# X = word2vec_tfidf_dl_embeddings

df = pd.DataFrame(X, columns=word_list(preprocessed_questions))
print(df)

#print(df.info())

#print(df.isnull().sum())

#print(df.describe())

# df=df.drop(['NameofInstitution',],axis=1)
df=df.drop(df.columns[0],axis=1)


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
#Fit the model to all the data except for the Private label.

# kmeans.fit(df.drop('Private',axis=1))
kmeans.fit(df.drop(df.columns[1],axis=1))
print(kmeans.labels_)

def converter(cluster):
    if cluster=='Yes':
        return 0
    else:
        return 1
# df['Cluster'] = df['Private'].apply(converter)
df[df.columns[2]] = df[df.columns[1]].apply(converter)

print(df[df.columns[1]].value_counts())
#df['Cluster'] --> holds the actual labels for each row; kmeans.labels --> predicted values/lablels
#so what we are doing is comparing actual labels against predicted labels
#the challenge is only one - need to identify correctly the correct cluster that
#reflects 0 or 1 label for binaru clase (two possibilities)
#question clustering --> three labels - LOTS, MOTS, HOTS, so clustering will assign
#0,1,2 values to name clusters, so need to identify 0 corresponds to LOTS or MOTS or HOTS
from sklearn.metrics import confusion_matrix,classification_report
# print(confusion_matrix(df['Cluster'],kmeans.labels_))
# print(classification_report(df['Cluster'],kmeans.labels_))
print(confusion_matrix(df[df.columns[2]],kmeans.labels_))
print(classification_report(df[df.columns[2]],kmeans.labels_))