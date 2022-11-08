# 超出范围检测
import tecplot as tp
import pandas as pd
import numpy as np

def out_of_range_check(direction = 'x',num = 0):
    num = float(num)
    direciton_dict = {'x':0,'y':1,'z':2}
    vec = direciton_dict[direction]
    axes = tp.active_frame().plot().axes
    l_axes = [axes.x_axis,axes.y_axis,axes.z_axis]
    if num > l_axes[0].max or num < l_axes[0].min:
        print('Range: %.2f to %.2f' %(l_axes[0].min,l_axes[0].max))
        raise Exception('Point:%s Out of range of coordinates !' % num)
