import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder



def clustering_data_method1_test():
    df = pd.read_csv('Cleaned.csv')
    x = df.copy()
    xx = x.drop(['id','patient_nbr'], axis=1)

    features, clusters = make_blobs(n_samples=40782,
                                    n_features=40,
                                    centers=7,
                                    cluster_std=0.4,
                                    shuffle=True)

    kmeans = KMeans(n_clusters=7)
    kmeans.fit(features)

    labels = kmeans.predict(features)

    xx['cluster'] = labels

    print("Feature Matrix: ")
    print(pd.DataFrame(features, columns=xx.columns).head())
    plt.scatter(features[:, 0], features[:, 1], c=labels)
    plt.show()
    

def clustering_data_method2_test():
    df = pd.read_csv('Cleaned.csv')
    x = df.copy()
    xx = x.drop(['id', 'patient_nbr'], axis=1)

    encoder = OneHotEncoder(sparse=False)
    gender_encoded = encoder.fit_transform(x.columns)

    scaler = StandardScaler()
    X_std = scaler.fit_transform(gender_encoded)
    X_std = pd.DataFrame(X_std, columns=gender_encoded.columns)

    cluster_colors = ['#b4d2b1', '#568f8b', '#1d4a60', '#cd7e59', '#ddb247', '#d15252']

    from sklearn.metrics import silhouette_score

    silhouette_scores = []
    for k in range(2, 7):
        km = KMeans(n_clusters=k,
                    max_iter=300,
                    tol=1e-04,
                    init='k-means++',
                    n_init=10,
                    random_state=42,
                    algorithm='auto')
        km.fit(X_std)
        silhouette_scores.append(silhouette_score(X_std, km.labels_))

    fig, ax = plt.subplots()
    ax.plot(range(2, 7), silhouette_scores, 'bx-')
    ax.set_title('Silhouette Score Method')
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Silhouette Scores')
    plt.xticks(range(2, 7))
    plt.tight_layout()
    plt.show()


def clustering_data_method1_test():
def clustering_data_method2_test():


