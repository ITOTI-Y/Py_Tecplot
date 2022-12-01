import tecplot as tp
from tecplot.constant import *

def creat_streamtraces(replace=True,zone_name='inlet',num = 50):
    frame = tp.active_frame()
    plot = frame.plot()
    zone_list = frame.dataset.zone_names
    zone_index = zone_list.index(zone_name)
    streamtraces = plot.streamtraces
    if replace:
            streamtraces.delete_all()
    streamtraces.add_on_zone_surface(zones=[zone_index],stream_type=Streamtrace.VolumeLine,num_seed_points=num)