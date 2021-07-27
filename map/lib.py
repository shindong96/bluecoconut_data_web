import csv
import pandas as pd
import numpy as np
import gsw
import pymysql
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

def csv_update(request,pk,cycle):
    conn = pymysql.connect(host='heap-pop-db.cvq2tkhhbqnh.ap-northeast-2.rds.amazonaws.com', user='admin', password='Qxv7rNaqpI30aIyr6GW1', db='bluecoconut', charset='utf8')

    if cycle == 0 or cycle == None:
        query = 'SELECT * FROM bluecoconut.table_view_argoinfo WHERE argo_id =' + str(pk)
    else:
        query = 'SELECT * FROM bluecoconut.table_view_argoinfo WHERE argo_id =' + str(pk) + ' and Cycle =' + str(cycle)

    df = pd.read_sql_query(query, conn)
    df.to_csv(r'static/csv_file/chart_test.csv', index=False)

    response = {'status': 1, 'message': 'data load success'}
    return HttpResponse(json.dumps(response), content_type='application/json')