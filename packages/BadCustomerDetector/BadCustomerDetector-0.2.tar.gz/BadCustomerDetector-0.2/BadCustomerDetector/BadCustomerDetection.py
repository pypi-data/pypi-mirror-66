import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
from scipy import stats

from pyod.models.cblof import CBLOF
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
from pyod.models.lof import LOF
import warnings
warnings.filterwarnings("ignore")

class BadCustomerDetection():
    def _init_(self):
        pass
    
    ##############################################
    #Calculate within-cluster sum of square (wss)#
    ############################################## 
    def k_finder(self, cluster_scaled, plot = False,S = 0, curve='convex', direction='decreasing'):
        clusters_range = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        sse = self.calculate_WSS(cluster_scaled, clusters_range, plot = plot)
        kneedle = KneeLocator(clusters_range, sse, S, curve, direction)
        return kneedle.elbow
                              
    def calculate_WSS(self, points, clusters_range, plot = False):
        sse = []  
        for k in clusters_range:
            kmeans = KMeans(n_clusters = k).fit(points)
            centroids = kmeans.cluster_centers_
            pred_clusters = kmeans.predict(points)
            curr_sse = 0 
        # calculate square of Euclidean distance of each point from its cluster center and add to current WSS
            for i in range(len(points)):
                curr_center = centroids[pred_clusters[i]]
                curr_sse += (points[i, 0] - curr_center[0]) ** 2 + (points[i, 1] - curr_center[1]) ** 2  
            sse.append(curr_sse)
        if(plot == True):
            plt.figure()
            plt.plot(clusters_range,sse, marker='o')  
        return sse
    
    ####################################
    #Detect Outliers or a group of data#
    ####################################
    #It's multivariate outlier detection, can choose method among 'CBLOF','FB','HBOS','IF','KNN' or 'Voting' 
    #which will run apply all the models and output the results based on the voting of all the model results 
    def outlier_detector(self, clustered_data, outliers_fraction = 0.05, method = 'Voting',cluster_number = 3):
        
        random_state = np.random.RandomState(42)
        outliers_df = pd.DataFrame()
        classifiers = {
            #Cluster-based Local Outlier Factor 
            'CBLOF':CBLOF(contamination=outliers_fraction,check_estimator=False, random_state=random_state),
            #Feature Bagging
            'FB':FeatureBagging(LOF(n_neighbors=35),contamination=outliers_fraction,check_estimator=False,random_state=random_state),
            #Histogram-base Outlier Detection 
            'HBOS': HBOS(contamination=outliers_fraction),
            #Isolation Forest
            'IF': IForest(contamination=outliers_fraction,random_state=random_state),
            #K Nearest Neighbors
            'KNN': KNN(contamination=outliers_fraction)
       }

        for k in range(cluster_number):

            curr_cluster = clustered_data[clustered_data['Cluster'] == k]
            X_train = curr_cluster.drop(['consumer_id','Cluster'], axis = 1)
            for i, (clf_name, clf) in enumerate(classifiers.items()):
                clf_pred = clf_name+'_Decision'
                clf.fit(X_train)
        # predict raw anomaly score
                scores_pred = clf.decision_function(X_train)
                scores_pred_df = pd.DataFrame(list(scores_pred), columns =[clf_name], index = curr_cluster.index.copy())
                curr_cluster = pd.concat([curr_cluster, scores_pred_df], axis=1)

                outliers_pred = clf.predict(X_train)
                outliers_pred_df = pd.DataFrame(list(outliers_pred), columns =[clf_pred], index = curr_cluster.index. copy())
                curr_cluster = pd.concat([curr_cluster, outliers_pred_df], axis=1)

            outliers_df = outliers_df.append(curr_cluster)

        
        if(method == 'Voting'):
            outliers_df['Voting'] = outliers_df.filter(regex='Decision').sum(axis = 1)
            outliers_df['bad_customer'] = 0
            outliers_df.loc[(outliers_df.Voting > len(classifiers)/2), 'bad_customer'] = 1
        else:
            decision = method + '_Decision'
            outliers_df['bad_customer'] = outliers_df[decision]

        return outliers_df

    def bad_customer_detector(self, df, log_transformation = True, elbow_finder = False, n_cluster = 3, outliers_fraction = 0.05, method = 'Voting'): ##if elbow = False, need to provide n_cluster
        
        if(log_transformation == True):
            cluster_log = np.log(df.drop(['consumer_id'], axis = 1))
        else:
            cluster_log = df.drop(['consumer_id'], axis = 1)

        scaler = StandardScaler()
        cluster_scaled = scaler.fit_transform(cluster_log)
        ##Start to test cluster numbers
        
        if(elbow_finder == True):
            K_elbow = self.k_finder(cluster_scaled)
            if K_elbow is None:
                print('Need to provide a number')
            else:
                cluster_number = kneedle.elbow
        else:
            cluster_number = n_cluster
        #clustering starts from here
        kmeans_sel = KMeans(n_clusters=cluster_number, random_state=1).fit(cluster_scaled)
        labels = pd.DataFrame(kmeans_sel.labels_)
        clustered_data = df.assign(Cluster=labels)

        outliers = self.outlier_detector(clustered_data, outliers_fraction, method, cluster_number)

        return outliers.sort_index()