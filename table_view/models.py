from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Argo_User(models.Model): #주민번호 앞자리 뒷자리로 나누어야 할듯 (앞자리를 생년월일로)
    MEMBER_TYPE_CHOICES = (('사기업','사기업'),('공기업','공기업'),('연구소','연구소'),('개인','개인'))
    STATE_CHOICES = ((False, '사용불가'), (True, '사용가능'))
    registrationNumber_F = models.CharField(null=True, max_length=6) #주민등록번호 앞자리
    registrationNumber_B = models.CharField(null=True, max_length=7) #주민등록번호 뒷자리
    researcherNumber = models.CharField(null=True, max_length=30, blank=True) #과학기술인번호
    nationality = models.CharField(null=True, max_length=20) #국적
    name = models.CharField(null=True, max_length=20) #성명
    contactNum = models.CharField(null=True, max_length=15) #연락처
    memberType = models.CharField(choices=MEMBER_TYPE_CHOICES,null=True, max_length=10) #회원 유형
    userID = models.ForeignKey(User, related_name= 'auths', on_delete=models.DO_NOTHING, blank=True, null=True) #auth_User index
    State = models.NullBooleanField(choices=STATE_CHOICES,default=True, null=True, blank=True) #회원 계정 사용여부(정지,차단 등)
    active = models.BooleanField(default=True) # 0: 삭제된데이터, 1: 등록된데이터
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Argo(models.Model):
    Serial_number = models.CharField(null=True, max_length=20, unique=True) #아르고 고유번호
    Last_location_lat = models.FloatField(null=True) #최근위도
    Last_location_long = models.FloatField(null=True) #최근경도
    Last_time = models.DateTimeField(null=True, default=datetime.now) #시작날짜
    Last_cycle = models.IntegerField(null=True) # 사이클 횟수
    Source_time = models.DateTimeField(null=True, default=datetime.now) #최근날짜
    Open_state = models.BooleanField(default=True) #공개여부
    Live = models.BooleanField(default=True) #기계 작동여부
    active = models.BooleanField(default=True) # 0: 삭제된데이터, 1: 등록된데이터


    def __str__(self):
        return self.Serial_number

class Relation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    argo = models.ForeignKey(Argo, on_delete=models.DO_NOTHING)

class ArgoInfo(models.Model):
    Latitude = models.FloatField(null=True) #위도
    Longitude = models.FloatField(null=True) #경도
    Temperature = models.FloatField(null=True) #수온
    Salinity = models.FloatField(null=True) #염분
    Pressure = models.FloatField(null=True) #압력
    Time = models.DateTimeField(null=True) #관측시간
    Cycle = models.IntegerField(null=True) #사이클
    argo = models.ForeignKey(Argo, on_delete=models.DO_NOTHING)