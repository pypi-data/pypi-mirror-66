from sklearn.cluster import KMeans

def kmeans(data, n_clusters):
    # Number of clusters
    kmeans = KMeans(n_clusters, n_init=2, max_iter=100, n_jobs=-1)
    # Fitting the input data
    kmeans = kmeans.fit(data)
    # Getting the cluster labels
    labels = kmeans.predict(data)
    # Centroid values
    centroids = kmeans.cluster_centers_

    return labels
