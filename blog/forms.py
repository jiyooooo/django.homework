from django import forms
from .models import Blog

class BlogPost(forms.ModelForm): #모델을 기반으로 한 입력공간

    class Meta:
        model = Blog #어떤 모델쓸지
        fields = '__all__' #그 모델에서 어떤 필드 쓸지
