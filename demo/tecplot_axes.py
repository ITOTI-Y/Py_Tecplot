# 坐标转换/坐标修正
import tecplot as tp
import pandas as pd
import numpy as np

#坐标转换
def axes_transform(frame = tp.active_frame(),transform = {'z':'y','y':'z'},init = True,fix = True):
    axes = frame.plot().axes #笛卡尔三维坐标系
    plot = frame.plot()
    dataset = frame.dataset
    for i in transform:
        if i == 'x' or i == 'X':
            axes.x_axis.variable = dataset.variable(f'{transform[i]}')
        elif i == 'y' or i == 'Y':
            axes.y_axis.variable = dataset.variable(f'{transform[i]}')
        elif i == 'z' or i == 'Z':
            axes.z_axis.variable = dataset.variable(f'{transform[i]}')
    if init: #初始化坐标轴，重设缩放
        axes.reset_range()
        axes.reset_scale()
        plot.view.fit()


#坐标修正
def axes_fix(origin = 'center',transform_axes = False):
    '''
    完成平面坐标居中和纵向坐标gui'ling
    '''
    dataset = tp.active_frame().dataset
    axes = tp.active_frame().plot().axes
    #------------------平面坐标居中------------------ 方法
    def axes_(transform_axes):
        #NO CHANGE
        transform_list = ['X','Y','Z']
        if transform_axes:
            temp = transform_list[2]
            transform_list[2] = transform_list[1]
            transform_list[1] = temp
        transform_x = -(dataset.variable('X').max()+dataset.variable('X').min())/2
        transform_y = -(dataset.variable(transform_list[1]).max()+dataset.variable(transform_list[1]).min())/2
        transform_z = -dataset.variable(transform_list[2]).min()
        tp.data.operate.execute_equation('{X_fix} =  {' + f'{transform_list[0]}'+'}'+f'{transform_x:+}')
        tp.data.operate.execute_equation('{Y_fix} =  {' + f'{transform_list[1]}'+'}'+f'{transform_y:+}')
        tp.data.operate.execute_equation('{Z_fix} =  {' + f'{transform_list[2]}'+'}'+f'{transform_z:+}')
        axes.x_axis.variable = dataset.variable('X_fix')
        axes.y_axis.variable = dataset.variable('Y_fix')
        axes.z_axis.variable = dataset.variable('Z_fix')

    #闭包函数调用不能在函数定义前
    if origin == 'center':
        return axes_(transform_axes)