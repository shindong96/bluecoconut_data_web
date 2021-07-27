import csv
import pandas as pd
import numpy as np
import gsw
import pymysql
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from .models import Argo, ArgoInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import os

def data_view_function(argo_num):

    data = pd.DataFrame(list(ArgoInfo.objects.filter(argo_id=argo_num).values()))
    data.head()

    latitude = data['Latitude']
    longitude = data['Longitude']
    pres = data['Pressure']
    temp = data['Temperature']
    salt = data['Salinity']

    #3d.png
    fig = plt.figure(num=None, figsize=(10, 10), facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111, projection="3d")

    im = ax.scatter(salt, temp, pres, s=1, c=pres, cmap="rainbow")
    ax.set_title("Three Dimension Plotting (Colormap : Pressure)", fontsize=12)

    ax.set_xlabel("Salinity (psu)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_zlabel("Pressure (Pa)")
    ax.grid("on")

    cmap = plt.colorbar(im, ax=ax)
    cmap.set_label("Pressure (Pa)", fontsize=12)
    cmap.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/3d_test.png", format="png", dpi=600, transparent=False)

    #3d-2.png
    fig = plt.figure(num=None, figsize=(10, 10), facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111, projection="3d")

    im = ax.scatter(salt, latitude, pres, s=1, c=pres, cmap="rainbow")
    ax.set_title("Three Dimensional Plotting (Salinity, Latitude, Pressure)", fontsize=12)

    ax.set_xlabel("Salinity (psu)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_zlabel("Pressure (Pa)")
    ax.grid("on")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Pressure (Pa)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/3d-2_test.png", format="png", dpi=600, transparent=False)

    #3d-3.png
    fig = plt.figure(num=None, figsize=(10, 10), facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111, projection="3d")

    im = ax.scatter(pres, latitude, temp, s=1, c=temp, cmap="rainbow")
    ax.set_title("Three Dimensional Plotting (Pressure, Latitude, Temperature)", fontsize=12)

    ax.set_xlabel("Pressure (Pa)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_zlabel("Temperature (°C)")
    ax.grid("on")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Temperature (°C)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/3d-3_test.png", format="png", dpi=600, transparent=False)

    #lat_ps.png
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10)) # ncols 는 한 화면에 출력될 그래프의 수

    im = ax.scatter(data["Latitude"], data["Pressure"], s=1, c=data["Salinity"], cmap="plasma")
    ax.set_title("Pressure Difference by Latitude Change (Colormap : Salinity)", fontsize=12)
    ax.set_xlabel("Latitude (°N)")
    ax.set_ylabel("Pressure (Pa)")
    ax.grid("on")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Salinity (psu)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/lat_ps_test.png", format="png", dpi=600, transparent=False)

    #lat_pt.png
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10)) # ncols 는 한 화면에 출력될 그래프의 수

    im = ax.scatter(data["Latitude"], data["Pressure"], s=1, c=data["Temperature"], cmap="plasma")
    ax.set_title("Pressure Difference by Latitude Change (Colormap : Temperature)", fontsize=12)
    ax.set_xlabel("Latitude (°N)")
    ax.set_ylabel("Pressure (Pa)")
    ax.grid("on")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Temperature (°C)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/lat_pt_test.png", format="png", dpi=600, transparent=False)

    #long_ps.png
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10)) # ncols 는 한 화면에 출력될 그래프의 수

    im = ax.scatter(data["Longitude"], data["Pressure"], s=1, c=data["Salinity"], cmap="plasma")
    ax.set_title("Pressure Difference by Longitude Change (Colormap : Salinity)", fontsize=12)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Pressure (Pa)")
    ax.grid("on")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Salinity (psu)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/long_ps_test.png", format="png", dpi=600, transparent=False)

    #long_pt.png
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10)) # ncols 는 한 화면에 출력될 그래프의 수

    im = ax.scatter(data["Longitude"], data["Pressure"], s=1, c=data["Temperature"], cmap="plasma")
    ax.set_title("Pressure Difference by Longitude Change (Colormap : Temperature)", fontsize=12)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Pressure (Pa)")
    ax.grid("on")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Temperature (°C)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.savefig("static/graph/long_pt_test.png", format="png", dpi=600, transparent=False)

def cycle_csv_create(argo_num,cycle):
    conn = pymysql.connect(host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"), db=os.environ.get("DB_NAME"), charset='utf8')

    if cycle == 0 or cycle == None:
        query = 'SELECT * FROM bluecoconut.table_view_argoinfo WHERE argo_id =' + str(argo_num)
    else:
        query = 'SELECT * FROM bluecoconut.table_view_argoinfo WHERE argo_id =' + str(argo_num) + ' and Cycle =' + str(cycle)
    df = pd.read_sql_query(query, conn)
    df.to_csv(r'static/csv_file/chart_test.csv', index=False)
