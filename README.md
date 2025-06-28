# 音乐数据聚类分析技术文档

## 1. 项目概述
本项目对尼日利亚歌曲数据集进行聚类分析，通过音频特征识别音乐的自然分组模式，支持音乐推荐、市场分析等应用。

## 2. 数据准备

### 2.1 数据集特征选取
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

#### 中位数填充（常规特征）
features.fillna(features.median(), inplace=True)

#### 特殊处理
features['instrumentalness'] = features['instrumentalness'].fillna(0)  # 人声为主的歌曲默认0

## 3. 聚类分析
### 3.1 标准化处理
采用Z-score标准化：

![image](https://github.com/user-attachments/assets/dd5bad09-3520-4162-9214-242cd0da031b)

### 3.2 确定最佳K值
肘部法则：观察惯性值拐点

轮廓系数：评估聚类紧密度
最佳k为4
![image](https://github.com/user-attachments/assets/ffadda74-a9eb-4761-87b4-98be3732f2e6)

### 3.3 K-Means实现



## 4. 结果分析
### 4.1 聚类特征
聚类	主要特征	代表类型
0	高舞蹈性(0.85)+高能量(0.8)	派对音乐
1	低乐器度+高人声占比	说唱
2	高原声度+低响度	民谣
3	中速节奏+均衡特征	流行
### 4.2 可视化
PCA降维图
![image](https://github.com/user-attachments/assets/8db00059-ee14-44d7-ad9c-68ae61efeb1e)

聚类分组图
![image](https://github.com/user-attachments/assets/46783dad-d375-43dc-9e16-043e483090d5)

特征对比图
![image](https://github.com/user-attachments/assets/1f62d8b6-a3fd-43bf-ade0-7f8b22fe3467)

### 4.3 总结分析
  通过对尼日利亚音乐数据的聚类分析，我们发现四类音乐风格呈现出鲜明的听觉特征分布：主流流行风格（分组0）以均衡的舞蹈性和能量值见长，代表作品如《Fall》展现了尼igerian pop的典型魅力；器乐型风格（分组1）则通过《Sparky》等作品凸显出高乐器性和声学性的独特质感，形成舒缓深沉的听觉体验；高能量舞曲（分组2）以《Kukere》为代表，凭借强烈的节奏能量和最大响度占据35%的曲库，成为最受欢迎的派对音乐类型；而语言叙事型（分组3）如《Ojuelegba》则通过突出的语言表达和节奏变化，在中等声学环境中构建出独特的叙事空间。市场偏好分析表明，尼日利亚听众对高能量舞曲的青睐度最高，这类歌曲不仅数量占比最大，平均流行度也显著领先，反映出当地音乐消费的活力化倾向，而器乐型作品虽数量较少却形成了稳定的艺术欣赏群体。这种基于音频特征的分类方式，为音乐服务平台提供了超越传统流派标签的内容组织新维度，能更精准地匹配健身场景的激昂舞曲或咖啡馆场景的舒缓器乐，实现用户体验的深度优化。
