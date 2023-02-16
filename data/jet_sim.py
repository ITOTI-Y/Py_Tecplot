import numpy as np
import pandas as pd
from decimal import Decimal
from plotly import express as px
import plotly.graph_objects as go
R = 0.1 # radius of the people
U = 0.2 # veloctiy of the field

def U_stockes(x,y,U = 0.2,R = 0.1):
    a = np.sqrt((x-(-R))**2+(y-0)**2)
    b = np.sqrt((x-0)**2+(y-0)**2) # distance from the center of the people to the point == r
    c = np.sqrt((-R-0)**2+(0-0)**2)
    d = round((b**2+c**2-a**2)/(2*b*c),12)
    rad_theta = np.arccos(d)
    u_r = -U*np.cos(rad_theta)*(1-3*R/(2*b)+R**3/(2*b**3))
    u_theta = U*np.sin(rad_theta)*(1-3*R/(4*b)-R**3/(4*b**3))
    u_x = round(u_r*(-np.cos(rad_theta))+u_theta*(np.sin(rad_theta)),10)
    u_y = round(u_r*(np.sin(rad_theta))+u_theta*(np.cos(rad_theta)),10)
    deg_theta = np.rad2deg(rad_theta).round(10)
    return[u_x,u_y,deg_theta,u_r,u_theta]

def dim(s):
    # s 为累计距离，单位m
    alpha = 0.076
    d0 = 0.02
    d = d0*6.8*(alpha*s/d0+1/6.8) # 0.147 = 1/6.8 使之满足s = 0时d = d0
    return d

def sim_jet(Total_time = 10,delta_t = 0.005,k = 0.65,U = 0.2,U_origin = [0,0.55],position = [0,0.1]):
    x = position[0]
    y = position[1] # initial people position
    u_p_x = U_origin[0] # initial people velocity
    u_p_y = U_origin[1] # initial people velocity
    s = 0 # initial distance
    res = [[x,y,u_p_x,u_p_y,s]]
    delta_t = delta_t # time step unit: 1/s
    for i in range(int(Total_time/delta_t)):
        alpha = 0.076
        delta_x = res[i][2]*delta_t
        delta_y = res[i][3]*delta_t
        x += delta_x
        y += delta_y
        s += np.sqrt(delta_x**2+delta_y**2)
        U_stockes_origin = U_stockes(res[i][0],res[i][1],U=U)
        U_stockes_next = U_stockes(x,y,U=U)
        u_real = np.sqrt(res[i][2]**2+res[i][3]**2)
        delta_u_real_x = -(0.48*alpha/dim(s)*(res[i][2]-U_stockes_next[0])*abs(u_real)*delta_t*k/(0.147)**2)+U_stockes_next[0]-U_stockes_origin[0]
        delta_u_real_y = -(0.48*alpha/dim(s)*(res[i][3]-U_stockes_next[1])*abs(u_real)*delta_t*k/(0.147)**2)+U_stockes_next[1]-U_stockes_origin[1]
        u_real_x = res[i][2]+delta_u_real_x
        u_real_y = res[i][3]+delta_u_real_y
        res.append([x,y,u_real_x,u_real_y,s])
    return res

def transform_pd(data,columns = ['x','y','u_real_x','u_real_y','s']):
    df = pd.DataFrame(data,columns = columns)
    df['y'] = df['y'] - 0.1
    return(df)