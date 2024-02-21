# 导入所需的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import os


class TsLabel():
    def __init__(self, filename) -> None:
        self.filename = filename
        self.df = pd.read_csv('data/'+filename, parse_dates=True, index_col=0)
        self.df['label'] = 0

    # 定义一个函数，用于根据用户的鼠标选择，给数据打上标签
    def label_data(self, start, end, label):
        # 找到开始和结束日期对应的索引
        start_index = self.df.index.get_indexer([start], method="nearest")[0]
        end_index = self.df.index.get_indexer([end], method="nearest")[0]
        # 给选中的区域打上标签
        start_t = self.df.index[start_index]
        end_t = self.df.index[end_index]
        self.df.loc[start_t:end_t, "label"] = label
        print(start_t, end_t, label)

    # 定义一个函数，用于绘制时间序列图，并添加鼠标交互功能
    def plot_data(self):
        # 定义一个回调函数，用于处理用户的选择
        def onselect(eclick, erelease):
            if eclick.button ==1:
                # 获取用户选择的开始和结束日期
                start = eclick.xdata
                end = erelease.xdata
                # 获取用户选择的标签
                label = int(radio.value_selected)
                # 调用标注函数
                self.label_data(start, end, label)
                # 在选中的区域上画一个矩形，颜色根据标签不同而不同
                rect = plt.Rectangle((start, ax.get_ylim()[0]), end-start, ax.get_ylim()[1]-ax.get_ylim()[0], alpha=0.2, color="green" if label == 0 else "red")
                ax.add_patch(rect)
                # 更新图像
                plt.draw()
        def on_right_click(self, event):
            # 判断是否是右键点击
            if event.button == 3:
                # 获取鼠标当前位置的日期
                date = event.xdata
                # 找到日期对应的索引
                index = self.df.index.get_indexer([date], method="nearest")[0]
                t = self.df.index[index]
                print(date, index, t)
                # 判断该位置是否已经打了标签1
                if self.df.loc[t, "label"] == 1:
                    # 找到该位置所在的矩形区域的边界
                    mask = self.df.index[self.df["label"] != 1]
                    startidx = np.where(mask < t)[0][-1]
                    endidx = np.where(mask > t)[0][0]
                    start = mask[startidx]
                    end = mask[endidx]
                    print('start&end =',start, end)
                    # 调用标注函数，将标签改为0
                    self.label_data(start, end, 0)
                    # 在该区域上画一个绿色的矩形
                    rect = plt.Rectangle((start, ax.get_ylim()[0]), end-start, ax.get_ylim()[1]-ax.get_ylim()[0], alpha=0.2, color="green")
                    ax.add_patch(rect)
                    # 更新图像
                    plt.draw()
        
        # 创建一个画布和一个子图
        fig, ax = plt.subplots()
        # 绘制时间序列数据
        ax.plot(self.df.index, self.df["P"], color="blue")
        # 设置标题和坐标轴标签
        ax.set_title("Time Series Data")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        # 创建一个矩形选择器，用于选择区域
        rect = widgets.RectangleSelector(ax, onselect, drawtype="box", useblit=True, spancoords="data")
        # 创建一个单选按钮，用于选择标签
        radio = widgets.RadioButtons(plt.axes([0.05, 0.4, 0.1, 0.15]), ("0", "1"))
        # 连接鼠标点击事件
        fig.canvas.mpl_connect("button_press_event", on_right_click)
        
        # 显示图像
        plt.show()

    def savecsv(self):
        self.df.to_csv('data/' + self.filename)


if __name__ == '__main__':
    files = os.listdir('data/')
    for file in files:
        print(file)
        labeltask = TsLabel(file)
        labeltask.plot_data()
        labeltask.savecsv()