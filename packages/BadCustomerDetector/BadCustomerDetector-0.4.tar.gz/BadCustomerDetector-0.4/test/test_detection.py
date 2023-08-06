#pytest case
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath('../BadCustomerDetector'))
import BadCustomerDetection as detection
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
  
def test_answer():
    detector = detection.BadCustomerDetection()
    df = pd.read_csv('./unique_consumers.csv')
    outliers_fraction = 0.05
    method = 'Voting'
    
    assert len(df.columns) == 6
    assert len(df) == 9888
    column_names = df.columns == ['consumer_id', 'unique_offer_clicked', 'total_offer_clicks','unique_offer_rides', 'total_offer_rides', 'total_offers_claimed']
    assert column_names.all() == True

    cluster_log = np.log(df.drop(['consumer_id'], axis = 1))
    scaler = StandardScaler()
    cluster_scaled = scaler.fit_transform(cluster_log)

    K_elbow = detector.k_finder(cluster_scaled)
    assert K_elbow == 3
    
    cluster_number = K_elbow
    kmeans_sel = KMeans(n_clusters=cluster_number, random_state=1).fit(cluster_scaled)
    labels = pd.DataFrame(kmeans_sel.labels_)
    clustered_data = df.assign(Cluster=labels)

    assert len(clustered_data.Cluster.unique()) == 3

    outliers, detectors_list = detector.outlier_detector(clustered_data, outliers_fraction, method, cluster_number)

    assert len(outliers.bad_customer.unique()) == 2
    assert len(detectors_list) == 3