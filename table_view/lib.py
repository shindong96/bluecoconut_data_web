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


def PaginatorManager(request, queryset, num=20):
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, num)

    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1
    page_numbers_range = 5  # Display only 5 page numbers

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return page_range, queryset

def PaginatorManagerFilter(request, queryset, filter_factor):
    page = request.GET.get('page', 1)

    if filter_factor is not None:
        if int(filter_factor) == -1:
            pass
        else:
            queryset = queryset.filter(Cycle=filter_factor)

    paginator = Paginator(queryset, 20)

    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1
    page_numbers_range = 5  # Display only 5 page numbers

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return page_range, queryset

def csv_load():
    with open('test.csv','r') as f:
        dr = csv.DictReader(f)
        s = pd.DataFrame(dr)

    ss = []
    for i in range(len(s)):
        st = (s['LATITUDE (degree_north)'][i], s['LONGITUDE (degree_east)'][i], s['TEMP (degree_Celsius)'][i], s['PSAL (psu)'][i], s['PRES (decibar)'][i], s['VERTICAL_SAMPLING_SCHEME'], 1)
        ss.append(st)

    for i in range(len(s)):
        ArgoInfo.objects.create(Latitude=float(ss[i][0]), Longitude=float(ss[i][1]), Temperature=float(ss[i][2]), Salinity=float(ss[i][3]), Pressure=float(ss[i][4]), argo_id=int(ss[i][6]))

#Data visualization work

def ts_diagram():
    #queryset = ArgoInfo.objects.filter(argo_id=1)
    #print(queryset[2].Pressure)
    #데이터 불러오기
    data = pd.DataFrame(list(ArgoInfo.objects.all().values()))

    #T-S 다이어그램
    ts = data[['Temperature', 'Salinity']]
    df = ts.sort_values('Temperature', ascending = True)
    mint = np.min(df['Temperature'])
    maxt = np.max(df['Temperature'])
    mins = np.min(df['Salinity'])
    maxs = np.max(df['Salinity'])
    tempL = np.linspace(mint - 1, maxt + 1, 15420)
    salL = np.linspace(mins - 1, maxs + 1, 15420)
    Tg, Sg = np.meshgrid(tempL, salL)
    sigma_theta = gsw.sigma0(Sg, Tg)
    cnt = np.linspace(sigma_theta.min(), sigma_theta.max(), 15420)
    fig, ax = plt.subplots(figsize = (10, 10))
    cs = ax.contour(Sg, Tg, sigma_theta, colors = 'grey', zorder = 1)
    cl = plt.clabel(cs, fontsize = 10, inline = False, fmt = '%.1f')
    sc = plt.scatter(df['Salinity'], df['Temperature'], c = cnt, s = 10)
    cb = plt.colorbar(sc)
    ax.set_xlabel('Salinity ($‰$)')
    ax.set_ylabel('Temperature[$^\circ$C]')
    ax.set_title('T-S Diagram Temp-Adjusted', fontsize = 14, fontweight = 'bold')
    ax.xaxis.set_major_locator(MaxNLocator(nbins = 6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins = 8))
    ax.tick_params(direction = 'out')
    cb.ax.tick_params(direction = 'out')
    cb.set_label('Density[kg m$^{-3}$]')
    plt.tight_layout()
    plt.savefig('static/graph/test.png', format = 'png', dpi = 500, transparent = False)

    #Depth별 수온, 염분
    latitude = data['Latitude']
    longitude = data['Longitude']
    pres = data['Pressure']
    temp = data['Temperature']
    salt = data['Salinity']
    
    # Three in one
    test2, (ax2, ax3, ax4) = plt.subplots(1, 3, sharey = True)

    # Temperature
    ax2.scatter(temp, pres, c = 'blue', s = 0.1)
    ax2.set_ylabel('Pressure (Pa)')
    ax2.set_ylim(ax2.get_ylim()[::-1])
    ax2.set_xlabel('Temperature ($^\circ$C)')
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.set_ticks_position('top')

    # Salinity
    ax3.scatter(salt, pres, c = 'red', s = 0.1)
    ax3.set_xlabel('Salinity ($‰$)')
    ax3.xaxis.set_label_position('top')
    ax3.xaxis.set_ticks_position('top')
    ax3.yaxis.set_visible(False)

    # T-S Diagram
    ax4.scatter(temp, salt, c = 'green', s = 0.1)
    ax4.set_xlabel('Temperature ($^\circ$C)')
    ax4.set_ylabel('Salinity ($‰$)')
    ax4.xaxis.set_label_position('top')
    ax4.xaxis.set_ticks_position('top')

    plt.savefig('static/graph/test2.png', format = 'png', dpi = 900, transparent = False)

# def data_print():
    
#     data = pd.DataFrame(list(ArgoInfo.objects.all().values()))

#     ts = data[['Temperature', 'Salinity']]
#     df = ts.sort_values('Temperature', ascending = True)

#     latitude = data['Latitude']
#     longitude = data['Longitude']
#     pres = data['Pressure']
#     temp = data['Temperature']
#     salt = data['Salinity']

#     # Three in one
#     fig2, (ax2, ax3, ax4) = plt.subplots(1, 3, sharey = True)

#     # Temperature
#     ax2.scatter(temp, pres, c = 'blue', s = 0.1)
#     ax2.set_ylabel('Pressure (Pa)')
#     ax2.set_ylim(ax2.get_ylim()[::-1])
#     ax2.set_xlabel('Temperature ($^\circ$C)')
#     ax2.xaxis.set_label_position('top')
#     ax2.xaxis.set_ticks_position('top')

#     # Salinity
#     ax3.scatter(salt, pres, c = 'red', s = 0.1)
#     ax3.set_xlabel('Salinity ($‰$)')
#     ax3.xaxis.set_label_position('top')
#     ax3.xaxis.set_ticks_position('top')
#     ax3.yaxis.set_visible(False)

#     # T-S Diagram
#     ax4.scatter(temp, salt, c = 'green', s = 0.1)
#     ax4.set_xlabel('Temperature ($^\circ$C)')
#     ax4.set_ylabel('Salinity ($‰$)')
#     ax4.xaxis.set_label_position('top')
#     ax4.xaxis.set_ticks_position('top')

#     plt.savefig('fig2.png', format = 'png', dpi = 900, transparent = False)


def csv_create(request,pk):
    conn = pymysql.connect(host='heap-pop-db.cvq2tkhhbqnh.ap-northeast-2.rds.amazonaws.com', user='admin', password='Qxv7rNaqpI30aIyr6GW1', db='bluecoconut', charset='utf8')
    query = 'SELECT * FROM bluecoconut.table_view_argoinfo WHERE argo_id =' + str(pk)
    df = pd.read_sql_query(query, conn)
    df.to_csv(r'static/csv_file/download.csv', index=False)
    response = {'status': 1, 'message': '최신 데이터를 갱신하여 다운로드를 시작합니다.'}
    return HttpResponse(json.dumps(response), content_type='application/json')

def cycle_csv_create(request,pk,cycle):
    conn = pymysql.connect(host='heap-pop-db.cvq2tkhhbqnh.ap-northeast-2.rds.amazonaws.com', user='admin', password='Qxv7rNaqpI30aIyr6GW1', db='bluecoconut', charset='utf8')
    query = 'SELECT * FROM bluecoconut.table_view_argoinfo WHERE argo_id =' + str(pk) + ' and Cycle =' + str(cycle)
    df = pd.read_sql_query(query, conn)
    df.to_csv(r'static/csv_file/download.csv', index=False)
    response = {'status': 1, 'message': '최신 데이터를 갱신하여 다운로드를 시작합니다.'}
    return HttpResponse(json.dumps(response), content_type='application/json')

# #cycle생성기
# def cycle_data(argo_num, cycle):
#     print(cycle)

#     if cycle is None:
#         data = pd.DataFrame(list(ArgoInfo.objects.filter(argo_id=argo_num).values()))
#     else:
#         if int(cycle) is 0:
#             data = pd.DataFrame(list(ArgoInfo.objects.filter(argo_id=argo_num).values()))
#         else:
#             data = pd.DataFrame(list(ArgoInfo.objects.filter(argo_id=argo_num,Cycle=cycle).values()))

#     latitude = data['Latitude']
#     longitude = data['Longitude']
#     pres = data['Pressure']
#     temp = data['Temperature']
#     salt = data['Salinity']

#     # Three in one
#     test2, (ax2, ax3, ax4) = plt.subplots(1, 3, sharey = True)

#     # Temperature
#     ax2.scatter(temp, pres, c = 'blue', s = 0.1)
#     ax2.set_ylabel('Pressure (Pa)')
#     ax2.set_ylim(ax2.get_ylim()[::-1])
#     ax2.set_xlabel('Temperature ($^\circ$C)')
#     ax2.xaxis.set_label_position('top')
#     ax2.xaxis.set_ticks_position('top')

#     # Salinity
#     ax3.scatter(salt, pres, c = 'red', s = 0.1)
#     ax3.set_xlabel('Salinity ($‰$)')
#     ax3.xaxis.set_label_position('top')
#     ax3.xaxis.set_ticks_position('top')
#     ax3.yaxis.set_visible(False)

#     # T-S Diagram
#     ax4.scatter(temp, salt, c = 'green', s = 0.1)
#     ax4.set_xlabel('Temperature ($^\circ$C)')
#     ax4.set_ylabel('Salinity ($‰$)')
#     ax4.xaxis.set_label_position('top')
#     ax4.xaxis.set_ticks_position('top')

#     plt.savefig('static/graph/test2.png', format = 'png', dpi = 900, transparent = False)


def map_data_print(request,cycle):

    if cycle is 0:
        data = pd.DataFrame(list(ArgoInfo.objects.all().values()))
    else:
        if int(cycle) == 0:
            data = pd.DataFrame(list(ArgoInfo.objects.all().values()))
        else:
            data = pd.DataFrame(list(ArgoInfo.objects.filter(Cycle=cycle).values()))

    latitude = data['Latitude']
    longitude = data['Longitude']
    pres = data['Pressure']
    temp = data['Temperature']
    salt = data['Salinity']

    # Three in one
    test2, (ax2, ax3, ax4) = plt.subplots(1, 3, sharey = True)

    # Temperature
    ax2.scatter(temp, pres, c = 'blue', s = 0.1)
    ax2.set_ylabel('Pressure (Pa)')
    ax2.set_ylim(ax2.get_ylim()[::-1])
    ax2.set_xlabel('Temperature ($^\circ$C)')
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.set_ticks_position('top')

    # Salinity
    ax3.scatter(salt, pres, c = 'red', s = 0.1)
    ax3.set_xlabel('Salinity ($‰$)')
    ax3.xaxis.set_label_position('top')
    ax3.xaxis.set_ticks_position('top')
    ax3.yaxis.set_visible(False)

    # T-S Diagram
    ax4.scatter(temp, salt, c = 'green', s = 0.1)
    ax4.set_xlabel('Temperature ($^\circ$C)')
    ax4.set_ylabel('Salinity ($‰$)')
    ax4.xaxis.set_label_position('top')
    ax4.xaxis.set_ticks_position('top')

    plt.savefig('static/graph/test2.png', format = 'png', dpi = 900, transparent = False)
    