from django.shortcuts import render
from django.http import HttpResponse
from table_view.models import *
# from django.views.generic import ListView
import json
import logging
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import os

@login_required()
def my_view(request):
    context = {
        'api_key': os.environ.get('GOOGLE_MAPS_API_KEY')
    }
    return render('map.html', context)

@login_required()
def map_main(request):
    argoObjects = Argo.objects.values('Serial_number', 'Last_location_lat', 'Last_location_long','Last_time','Last_cycle','Source_time')    
    argos = []
    for argoObject in argoObjects:
        argo = {}
        argo["number"] = argoObject["Serial_number"]
        argo["lat"] = argoObject["Last_location_lat"]
        argo["lng"] = argoObject["Last_location_long"]
        if argoObject["Last_time"] is not None:
            argo["last_time"] = argoObject["Last_time"].strftime("%Y-%m-%d")
        else:
            argo["last_time"] = argoObject["Last_time"]
        argo["cycle"] = argoObject["Last_cycle"]
        if argoObject["Source_time"] is not None:
            argo["source_time"] = argoObject["Source_time"].strftime("%Y-%m-%d")
        else:
            argo["source_time"] = argoObject["Source_time"]
        argos.append(argo)
    argosJson = json.dumps(argos, cls=DjangoJSONEncoder)
    return render(request, 'map.html', {'argosJson': argosJson})


# CLASS 형태로 URL에 return
# class Map_Markup(ListView):
#     template_name = 'map.html'

#     def get_queryset(self):
#         argos = Argo.objects.values('Serial_number', 'Source_location_lat', 'Source_location_long')
#         return argos

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(Map_Markup, self).get_context_data(**kwargs)
#         context['Argo'] = self.get_queryset()
#         return context

def argo_data(request, pk):
    # (주의사항)
    # 현재 MYSQL에는 없는데, ArgoInfo에서 
    # id: 123123이 가져와짐(예전에 insert했을때 실패해서 안 들어갔다고 떴었음)
    # id 998과 동일한 lat, lng 값을 가지고 있어서
    # polyline을 그리면 사이클 처럼 나오게 되는 상황임
    # argoCycleObjects = ArgoInfo.objects.filter(argo_id=pk).values('id','Latitude', 'Longitude')
    argoCycleObjects = ArgoInfo.objects.filter(argo_id=pk).values('Cycle','Latitude', 'Longitude', 'Time').distinct()
    argoCycleDatas = []
    for argoCycleObject in argoCycleObjects:
        argoCycleData = {}
        argoCycleData["cycle_number"] = argoCycleObject["Cycle"]
        # argoCycleData["id"] = argoCycleObject["id"]
        argoCycleData["lat"] = argoCycleObject["Latitude"]
        argoCycleData["lng"] = argoCycleObject["Longitude"]
        if argoCycleObject["Time"] is not None:
            argoCycleData["time"] = argoCycleObject["Time"].strftime("%Y-%m-%d")
        else:
            argoCycleData["time"] = argoCycleObject["Time"]
        argoCycleDatas.append(argoCycleData)
    return HttpResponse(json.dumps({"argoCycleDatas": argoCycleDatas},cls=DjangoJSONEncoder), content_type='application/json')

# ajax 참고 by 구본
# class EmployeeDetailView(DetailView):
# def get(self,request,pk):
#     employee = Employee.objects.get(pk=pk)
#     response = {'employee_number': employee.employee_number, 'name': employee.name,
#                 'name_eng': employee.name_eng, 'registrationNumber': employee.registrationNumber,
#                 'researcherNumber': employee.researcherNumber, 'phoneNumber': employee.phoneNumber,
#                 'emailAddress_company': employee.emailAddress_company, 'address': employee.address,
#                 'department': employee.department_id, 'jobTitleType': employee.jobTitleType_id,
#                 'newcorner': employee.newcorner, 'startDate': employee.startDate,
#                 'endDate': employee.endDate, 'userID': employee.userID_id, 'workPlace': employee.workPlace}
#     return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json')