from django.shortcuts import render, HttpResponse
import numpy as np
import pandas as pd

# Create your views here.
from nlp_proj.models import Hotel

def read_dummy(txtfile):
    txtfile = pd.read_csv(txtfile, sep = ",", header = None)
    for i in txtfile:
        print(txtfile["1"])



def index(request):
    dd = read_dummy("dummydata/dummy.txt")

    # review_all = Hotel.objects.all()  # .get(), .filter(), ...
    # request가 POST -> Form을 완성.
    # Form이 유효하면 저장.\
    # if request.method == "POST":
    #     form = CoffeeForm(request.POST)  # 완성된 Form
    #     if form.is_valid():  # 채워진 Form이 유효하다면
    #         form.save()  # Form을 Model에 저장

    # form = CoffeeForm()
    return render(request, 'DH_Template.html')
