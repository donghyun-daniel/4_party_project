from django.shortcuts import render, HttpResponse
import numpy as np
import pandas as pd
import os
from nlp.settings import BASE_DIR
import json
import math


# Create your views here.
from nlp_proj.models import Hotel

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