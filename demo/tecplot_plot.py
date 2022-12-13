import tecplot as tp
import numpy as np
from tecplot.constant import PlotType,Streamtrace

#新建frame
def add_frame(num=(3,4)):
    a = np.arange(0,(num[0]-1)*9+1,9)
    b = np.arange(0,(num[1]-1)*8+1,8)
    for j in range(len(b)):
        for i in range(len(a)):
            if i == 0 and j == 0:
                continue
            tp.active_page().add_frame(position=(a[i],b[j]),size=(9,8))
            tp.active_frame().plot_type = PlotType.Cartesian3D

#创建流线图
def creat_streamtraces(replace=True,zone_name='inlet',num = 50):
    frame = tp.active_frame()
    plot = frame.plot()
    zone_list = frame.dataset.zone_names
    zone_index = zone_list.index(zone_name)
    streamtraces = plot.streamtraces
    if replace:
            streamtraces.delete_all()
    streamtraces.add_on_zone_surface(zones=[zone_index],stream_type=Streamtrace.VolumeLine,num_seed_points=num)