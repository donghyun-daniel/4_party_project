from django.shortcuts import render, HttpResponse, redirect
import numpy as np
import pandas as pd
import os
from nlp.settings import BASE_DIR
import json
import math


# Create your views here.
from .models import RawData
from .models import UploadFile
from .forms import UploadFileForm


def index(request):
    txtfile = pd.read_csv(os.path.join(BASE_DIR, "nlp_proj/dummydata/FastText_8_sentiment_results.txt"), sep=",")
    category_pos_cnt = txtfile.groupby("category").sum()
    category_total_cnt = txtfile.groupby("category").count()
    category_total_cnt["pos_cnt"] = category_pos_cnt["sentiment"]
    category_total_cnt["neg_cnt"] = category_total_cnt["sentiment"] - category_total_cnt["pos_cnt"]

    category_total_cnt["pos_ratio"] = category_total_cnt["pos_cnt"] / (category_total_cnt["pos_cnt"] + category_total_cnt["neg_cnt"])
    category_total_cnt["neg_ratio"] = category_total_cnt["neg_cnt"] / (category_total_cnt["pos_cnt"] + category_total_cnt["neg_cnt"])

    category_total_cnt["pos_cnt_sqrt"] = category_total_cnt["pos_cnt"].apply(math.sqrt)
    category_total_cnt["neg_cnt_sqrt"] = category_total_cnt["neg_cnt"].apply(math.sqrt)

    scaling_val = max(category_total_cnt["pos_cnt_sqrt"] + category_total_cnt["neg_cnt_sqrt"])
    category_total_cnt["pos_cnt_sqrt_modified"] = category_total_cnt["pos_cnt_sqrt"] / (scaling_val*8)
    category_total_cnt["neg_cnt_sqrt_modified"] = category_total_cnt["neg_cnt_sqrt"] / (scaling_val*8)

    category_total_cnt["pos_cnt_sqrt_modified_normalized"] = (category_total_cnt["pos_cnt_sqrt_modified"] - category_total_cnt["pos_cnt_sqrt_modified"].mean()) / (category_total_cnt["pos_cnt_sqrt_modified"].std() * 50)
    category_total_cnt["neg_cnt_sqrt_modified_normalized"] = (category_total_cnt["neg_cnt_sqrt_modified"] - category_total_cnt["neg_cnt_sqrt_modified"].mean()) / (category_total_cnt["neg_cnt_sqrt_modified"].std() * 50)

    category_total_cnt["pos_ratio_calib"] = category_total_cnt["pos_ratio"] + category_total_cnt["pos_cnt_sqrt_modified_normalized"]
    category_total_cnt["neg_ratio_calib"] = category_total_cnt["neg_ratio"] + category_total_cnt["neg_cnt_sqrt_modified_normalized"]

    category_total_cnt["pos_score"] = (category_total_cnt["pos_ratio_calib"] + category_total_cnt["pos_cnt_sqrt_modified"])
    category_total_cnt["neg_score"] = (category_total_cnt["neg_ratio_calib"] + category_total_cnt["neg_cnt_sqrt_modified"])

    category_total_cnt["pos_score_scaled"] = category_total_cnt["pos_score"] * 100 
    category_total_cnt["neg_score_scaled"] = category_total_cnt["neg_score"] * 100

    category_total_cnt = category_total_cnt.reset_index()

    category_dic = {}
    for i in category_total_cnt:
        category_dic[i] = [str(category_total_cnt[i][size]) for size in range(len(category_total_cnt["category"]))]

    category_json = json.dumps(category_dic)
    pos_score_json = json.dumps(category_dic["pos_score"])

    total_cnt = {"positive": int(category_total_cnt["pos_cnt"].sum()), "negative": int(category_total_cnt["neg_cnt"].sum())}
    total_json = json.dumps(total_cnt)



    #sents8_json = pd.read_csv(os.path.join(BASE_DIR, 'nlp_proj/dummydata/FastText_8_sentiment_results.txt') , sep=",", names=["txt", "category", "sentiment", "rawIdx"])
    #overall = txtfile.groupby("label").count().iloc[:3, 1].values
    #overall_dic = {"neg" : overall[0], "pos" : overall[1]}
    #overall_json = json.dumps(overall_dic)

    #sents17_json = pd.read_csv(os.path.join(BASE_DIR, 'nlp_proj/dummydata/FastText_17_sentiment_results.txt') , sep=",", names=["txt", "category", "sentiment", "rawIdx"])


    # review_all = Hotel.objects.all()  # .get(), .filter(), ...
    # request가 POST -> Form을 완성.
    # Form이 유효하면 저장.\
    # if request.method == "POST":
    #     form = CoffeeForm(request.POST)  # 완성된 Form
    #     if form.is_valid():  # 채워진 Form이 유효하다면
    #         form.save()  # Form을 Model에 저장

    # form = CoffeeForm()
    return render(request, 'index.html', {"total_json" : total_json, "category_json" : category_json, "pos_score_json" : pos_score_json})

def upload_view(request):
    file_all = UploadFile.objects.all()
    url = "/home/ubuntu/5team/nlp/media/rawfile"
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        return redirect(upload_view)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {"file_list" : file_all, "uploadform" : form})
def lineChart(request):
    
    import pandas as pd
    #데이터 읽어오기 
    #raw_datas = pd.read_csv(os.path.join(BASE_DIR, "nlp_proj/dummydata/FastText_8_sentiment_results.txt"), sep=",")
    #raw_datas = pd.read_csv('/Users/hoon2hooni/Downloads/4_party_big_files/big_test.csv')
    results_after_sentimental_col8 = pd.read_csv(os.path.join(BASE_DIR, "nlp_proj/dummydata/FastText_8_sentiment_results.txt"), sep=",")
    #results_after_sentimental_col8=pd.read_csv('/Users/hoon2hooni/Downloads/4_party_big_files/FastText_8_sentiment_results.txt') 
    
    #각 항목별 긍정 부정 
    sentiment_category = results_after_sentimental_col8[['sentiment','category']].groupby('category').sum()
    total_category = results_after_sentimental_col8[['text','category']].groupby('category').count()
    sentiment_category['negative'] = total_category['text']-sentiment_category['sentiment']
    #긍정 부정 비율 추가
    sentiment_category['pos_ratio'] = sentiment_category['sentiment']/total_category['text']
    sentiment_category['neg_ratio'] = sentiment_category['negative']/total_category['text']
    sentiment_category.columns=['긍정','부정','긍정비율','부정비율']
    #카테고리, 각 카테고리별 긍정 부정 점수 전달
    categories  = sentiment_category.index.tolist()
    positive_nums = sentiment_category['긍정비율'].tolist()
    positive_nums =json.dumps(positive_nums)
    negative_nums = sentiment_category['부정비율'].tolist()
    negative_nums = json.dumps(negative_nums)
    test_list = [{'2017':[100,90],'2018':[12,0],'2019':[90,300]},\
    {'2017':[10,90],'2018':[4,0],'2019':[90,33]},{'2017':[100,90],'2018':[40,0],'2019':[90,300],'2020':[44,222]},{'2017':[45,90],'2018':[40,0],'2019':[90,300]}\
    ,{'2017':[20,90],'2018':[40,0],'2019':[90,90]},{'2017':[100,90],'2018':[40,0],'2019':[90,300]},{'2017':[33,90],'2018':[40,0],'2019':[90,500]}]   
    cleanness_timeseries_pos_neg = dict()
    for key, value in zip(categories, test_list):
        cleanness_timeseries_pos_neg[key] = value
    categories = json.dumps(categories)
    print(cleanness_timeseries_pos_neg)
    cleanness_timeseries_pos_neg = json.dumps(cleanness_timeseries_pos_neg)
    return render(request, 'lineChart.html', {'categories':categories, 'clean_data': cleanness_timeseries_pos_neg,\
        "positive": positive_nums, "negative": negative_nums})    