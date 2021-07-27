import os, sys
from django import forms
from django.contrib.auth.models import User
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from table_view.models import Argo_User

class RegisterForm(forms.ModelForm): #주민번호 앞자리 뒷자리 나눠서 앞자리를 생년월일로 사용하게 설정
    MEMBER_TYPE_CHOICES = (('','--회원유형선택--'),('사기업','사기업'),('공기업','공기업'),('연구소','연구소'),('개인','개인'))
    memberType = forms.ChoiceField(initial='--회원유형선택--', widget=forms.Select(attrs={'class': 'form-control form-control-user'}), choices=MEMBER_TYPE_CHOICES, required=False)  

    class Meta:
        model = Argo_User
        fields = ['nationality','name','contactNum','researcherNumber','memberType']

        widgets = {
            'nationality': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder' : '국적'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder' : '이름'
                }
            ),
            'contactNum': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder' : '연락처'
                }
            ),
            'researcherNumber': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder' : '과학기술인번호'
                }
            )
        }
