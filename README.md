# 音乐数据聚类分析技术文档

## 1. 项目概述
本项目对尼日利亚歌曲数据集进行聚类分析，通过音频特征识别音乐的自然分组模式，支持音乐推荐、市场分析等应用。

## 2. 数据准备

### 2.1 数据集特征
| 特征名 | 类型 | 描述 | 取值范围 |
|--------|------|------|----------|
| danceability | 连续值 | 舞蹈性 | 0-1 |
| energy | 连续值 | 能量感 | 0-1 |
| loudness | 连续值 | 响度(dB) | -60~0 |
| speechiness | 连续值 | 语音度 | 0-1 |
| acousticness | 连续值 | 原声度 | 0-1 |
| instrumentalness | 连续值 | 乐器度 | 0-1 |
| liveness | 连续值 | 现场感 | 0-1 |
| tempo | 连续值 | 速度(BPM) | 50-200 |

### 2.2 缺失值处理
```python
# 中位数填充（常规特征）
features.fillna(features.median(), inplace=True)

# 特殊处理
features['instrumentalness'] = features['instrumentalness'].fillna(0)  # 人声为主的歌曲默认0
3. 聚类分析
3.1 标准化处理
采用Z-score标准化：

python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
3.2 确定最佳K值
肘部法则：观察惯性值拐点

轮廓系数：评估聚类紧密度
https://elbow_silhouette.png

3.3 K-Means实现
python
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(scaled_features)
4. 结果分析
4.1 聚类特征
聚类	主要特征	代表类型
0	高舞蹈性(0.85)+高能量(0.8)	派对音乐
1	低乐器度+高人声占比	说唱
2	高原声度+低响度	民谣
3	中速节奏+均衡特征	流行
4.2 可视化
PCA降维图
https://pca_visualization.png

平行坐标图
https://parallel_coordinates.png
