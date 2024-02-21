import pandas as pd

# 创建一个示例DataFrame
data = {'A': [1, 2, 2.5, 6, 7],
        'B': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# 获取与给定值最接近的索引位置
value = 2.7
indexer0 = df.index.get_indexer([4], method='pad')
indexer = df.index.get_indexer([value,4], method='backfill')
indexer1 = df.index.get_loc(value, method='backfill')

# 输出结果
print(indexer0)
print(indexer)
print(indexer1)