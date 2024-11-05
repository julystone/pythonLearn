#coding=utf-8

import matplotlib.pyplot as plt
import networkx as nx

# 创建一个NetworkX图
G = nx.Graph()

# 添加节点（这里假设是合约的名称）
G.add_nodes_from(['合约A', '合约B', '合约C', '合约D'])

# 添加边（这里表示合约之间的关系）
G.add_edge('合约A', '合约B')
G.add_edge('合约B', '合约C')
G.add_edge('合约C', '合约D')
G.add_edge('合约D', '合约A')

# 使用NetworkX的绘图功能
pos = nx.spring_layout(G)  # 使用弹簧布局算法进行节点布局
nx.draw(G, pos, with_labels=True)

# 添加标题和轴标签（如果需要的话）
plt.title('期货合约关系图')
plt.axis('off')  # 关闭坐标轴

# 显示图表
plt.show()