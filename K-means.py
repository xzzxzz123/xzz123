# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# 设置全局参数
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']
# 1. 加载数据
df = pd.read_csv('nigerian-songs.csv')
print("数据集列名:", df.columns.tolist())

# 2. 选择特征列（根据实际数据调整）
features = df[['danceability', 'energy', 'loudness', 'speechiness',
               'acousticness', 'instrumentalness', 'liveness', 'tempo']]

# 3. 数据预处理
features = features.fillna(features.median())  # 填充缺失值
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 4. 确定最佳K值
inertia = []
silhouette_scores = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_features, kmeans.labels_))

# 绘制肘部法则和轮廓系数图
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(k_range, inertia, 'bo-')
plt.xlabel('聚类数量(K)')
plt.ylabel('惯性值')
plt.title('肘部法则')

plt.subplot(1, 2, 2)
plt.plot(k_range, silhouette_scores, 'go-')
plt.xlabel('聚类数量(K)')
plt.ylabel('轮廓系数')
plt.title('轮廓分析')
plt.tight_layout()
plt.show()

# 5. 执行聚类（选择K=4）
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(scaled_features)
df['聚类分组'] = clusters  # 中文列名

# 6. 分析聚类结果
print("\n各分组歌曲数量:")
print(df['聚类分组'].value_counts())

print("\n各分组音频特征均值:")
feature_means = df.groupby('聚类分组')[features.columns].mean()
print(feature_means)

# 7. 可视化分析
# PCA降维可视化
pca = PCA(n_components=2)
pca_features = pca.fit_transform(scaled_features)
df['主成分1'] = pca_features[:, 0]
df['主成分2'] = pca_features[:, 1]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='主成分1', y='主成分2', hue='聚类分组',
               palette='viridis', alpha=0.8)
plt.title('K-Means聚类结果可视化(PCA降维)')
plt.xlabel('主成分1 (解释方差: {:.1f}%)'.format(pca.explained_variance_ratio_[0]*100))
plt.ylabel('主成分2 (解释方差: {:.1f}%)'.format(pca.explained_variance_ratio_[1]*100))
plt.legend(title='聚类分组')
plt.show()

# 平行坐标图（标准化后的特征）
plt.figure(figsize=(12, 6))
scaled_df = pd.DataFrame(scaled_features, columns=features.columns)
scaled_df['聚类分组'] = clusters
pd.plotting.parallel_coordinates(
    scaled_df,
    '聚类分组',
    colormap='viridis',
    alpha=0.5
)
plt.title('各聚类音频特征对比')
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.show()

# 分组与流派的关系（前5大流派）
plt.figure(figsize=(12, 6))
top_genres = df['artist_top_genre'].value_counts().index[:5]
sns.countplot(data=df[df['artist_top_genre'].isin(top_genres)],
             x='artist_top_genre', hue='聚类分组')
plt.title('不同流派在各分组的分布')
plt.xlabel('音乐流派')
plt.ylabel('歌曲数量')
plt.xticks(rotation=45)
plt.legend(title='聚类分组')
plt.show()

