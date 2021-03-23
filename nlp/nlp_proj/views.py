from django.shortcuts import render, HttpResponse
# Create your views here.
from nlp_proj.models import Hotel


def index(request):
    review_all = Hotel.objects.all()  # .get(), .filter(), ...
    # request가 POST -> Form을 완성.
    # Form이 유효하면 저장.\
    # if request.method == "POST":
    #     form = CoffeeForm(request.POST)  # 완성된 Form
    #     if form.is_valid():  # 채워진 Form이 유효하다면
    #         form.save()  # Form을 Model에 저장

    # form = CoffeeForm()
    return render(request, 'index.html', {"review_list": review_all})
