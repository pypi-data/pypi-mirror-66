
import pandas as pd
import joblib
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression


class FraudDetectionModel:


    def elbowMethod(self):
        # find the appropriate cluster number
        plt.figure(figsize=(10, 8))
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
            kmeans.fit(dataset_standardized)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()

    def clusteringDendogram(self):
        # Hierarchical clustering for the same dataset
        # creating a dataset for hierarchical clustering
        # needed imports

        #creating the linkage matrix
        H_cluster = linkage(dataset_standardized,'ward')
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        dendrogram(
            H_cluster,
            truncate_mode='lastp',
            p=5,
            leaf_rotation=90.,
            leaf_font_size=12.,
            show_contracted=True,
        )
        plt.show()

    def clusteringPlot(self):
        H_cluster = linkage(dataset_standardized,'ward')
        dataset1_standardized = dataset_standardized
        # Assigning the clusters and plotting the observations as per hierarchical clustering
        from scipy.cluster.hierarchy import fcluster
        k=5
        cluster_2 = fcluster(H_cluster, k, criterion='maxclust')
        cluster_2[0:30:,]
        plt.figure(figsize=(10, 8))
        plt.scatter(dataset1_standardized.iloc[:,0], dataset1_standardized.iloc[:,1],c=cluster_2, cmap='prism')  # plot points with cluster dependent colors
        plt.title('Hierarchical Clutering')
        plt.show()

    def buildModel(self):
        from scipy.cluster.hierarchy import linkage,fcluster
        H_cluster = linkage(dataset_standardized, 'ward')
        cluster_2 = fcluster(H_cluster, 5, criterion='maxclust')
        # New Dataframe called cluster
        cluster_Hierarchical = pd.DataFrame(cluster_2)
        # Adding the hierarchical clustering to dataset
        dataset2=dataset_standardized
        dataset2['cluster'] = cluster_Hierarchical

        dataset2 = dataset2.assign(is_fraud=[1 if (x == 1 or x == 3) else 0 for x in dataset2['cluster']])

        #dataset2.to_csv(r'clustering_output.csv', index = False)

        y = dataset2['is_fraud'].values

        print(dataset2.head())
        print(y)
        X = dataset2.iloc[:, 0:18].values
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25)

        # Building and training the model
        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = classifier.predict(X_test)

        # Making the Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(cm)

        # Generating accuracy, precision, recall and f1-score
        target_names = ['fraud_No','fraud_Yes']
        print(classification_report(y_test, y_pred, target_names=target_names))


        # saving the model
        joblib.dump(classifier, "model_logistic.pkl")

        # Load the model from the file
        model_from_joblib = joblib.load('model_logistic.pkl')

        # Use the loaded model to make predictions
        output = model_from_joblib.predict(X_test)
        print(output)


original_df = pd.read_csv('data.csv')
df = original_df.drop('gender', 1)
df = df.drop('consumer_id', 1)
df = df.fillna(0)

# standardize the data to normal distribution
dataset_standardized = preprocessing.scale(df)
dataset_standardized = pd.DataFrame(dataset_standardized)

fd = FraudDetectionModel()
fd.elbowMethod()
fd.clusteringDendogram()
fd.clusteringPlot()
fd.buildModel()