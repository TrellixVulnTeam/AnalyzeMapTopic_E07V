# from django.views.decorators.csrf import csrf_exempt
import json
# from django.core import serializers
# import math
# import numpy
# import time
# from collections import Counter

from django.shortcuts import render
from django.http import JsonResponse
import pymongo
from math import radians, cos, sin, asin, sqrt
import re
import googlemaps
from . import legality as li

def haversine(lng1, lat1, lng2, lat2):
    # 将十进制度数转化为弧度
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    # haversine公式
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def ipeen_list(request):
    bigstyle = request.POST.get('bigstyle', "")
    smallstyle = request.POST.get('smallstyle', "")
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"

    #  print(radius,centerlat,centerlng)
    queryElements = {}
    if bigstyle != "":
        queryElements["bigstyle"] = bigstyle
    if smallstyle != "":
        queryElements["smallstyle"] = smallstyle
    if bigadd != "":
        queryElements["bigadd"] = bigadd
    if smalladd != "":
        queryElements["smalladd"] = smalladd
    # if radius != "":
    #     queryElements["radius"] = radius
    # print(queryElements)
    if bigstyle + bigadd + smalladd == "":
        # return JsonResponse({"不行": "什麼都沒篩會有一堆值，不給你"}, safe=False)
        client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
        # collection = client.rawData.wowprimeipeen
        collection = client.rawData.ipeenInfo
        ipeendata = list(collection.find(queryElements))
        client.close()
        ipeendata = [dien for dien in ipeendata if dien['status'] == "正常營業"
                     and dien['lat'] > 18
                     and dien['lat'] < 27
                     and dien['lng'] < 125
                     and dien['lng'] > 117
                     and dien['bigadd'] != 0
                     and dien['smalladd'] != 0
                     and dien['averagecost'] < 8000]
        if radius != "":  # lng1, lat1, lng2, lat2
            ipeendata = [dien for dien in ipeendata if
                         haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng, lat2=centerlat) < radius]

        for dien in ipeendata:
            dien["id"] = dien.pop("_id")
            # del dien["_id"]

        return JsonResponse(ipeendata, safe=False)
    else:
        client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
        # collection = client.rawData.wowprimeipeen
        collection = client.rawData.ipeenInfo
        ipeendata = list(collection.find(queryElements))
        client.close()
        ipeendata = [dien for dien in ipeendata if dien['status'] == "正常營業"
                     and dien['lat'] > 18
                     and dien['lat'] < 27
                     and dien['lng'] < 125
                     and dien['lng'] > 117
                     and dien['bigadd'] != 0
                     and dien['smalladd'] != 0
                     and dien['averagecost'] < 8000]
        if radius != "":  # lng1, lat1, lng2, lat2
            ipeendata = [dien for dien in ipeendata if
                         haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng, lat2=centerlat) < radius]

        for dien in ipeendata:
            dien["id"] = dien.pop("_id")
            # del dien["_id"]

        return JsonResponse(ipeendata, safe=False)


# @csrf_exempt
def hr104_list(request):
    print(request.POST)
    job = request.POST.get('job', "")
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    bigstyle = request.POST.get('bigstyle', "")  # 0124
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    queryElements = {}
    if job != "":
        queryElements["JOBCAT_DESCRIPT"] = job
    if bigadd != "":
        queryElements["bigadd"] = bigadd
    if smalladd != "":
        queryElements["smalladd"] = smalladd
    if bigstyle != "":  # 0124
        queryElements["bigstyle"] = bigstyle  # 0124
    # print(queryElements)

    if job + bigadd + smalladd + bigstyle == "":
        client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
        collection = client.rawData.HRdata104
        hr104data = list(collection.find(queryElements))
        client.close()
        hr104data = [dien for dien in hr104data if dien['LAT'] > 18
                     and dien['LAT'] < 27
                     and dien['SAL_MONTH_LOW'] > 18000
                     and dien['SAL_MONTH_LOW'] < 100000
                     and dien['SAL_MONTH_HIGH'] > 18000
                     and dien['SAL_MONTH_HIGH'] < 200000
                     and dien['LON'] < 125
                     and dien['LON'] > 117
                     and dien['bigadd'] != 0
                     and dien['smalladd'] != 0]
        for dien in hr104data:
            dien["lat"] = dien.pop("LAT")
            dien["lng"] = dien.pop("LON")
            del dien["_id"]
        if radius != "":  # lng1, lat1, lng2, lat2
            hr104data = [dien for dien in hr104data if
                         haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng, lat2=centerlat) < radius]
        return JsonResponse(hr104data, safe=False)
        # return JsonResponse({"不行": "什麼都沒篩會有一堆值，不給你"}, safe=False)
    else:
        client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
        collection = client.rawData.HRdata104
        hr104data = list(collection.find(queryElements))
        client.close()
        hr104data = [dien for dien in hr104data if dien['LAT'] > 18
                     and dien['LAT'] < 27
                     and dien['SAL_MONTH_LOW'] > 18000
                     and dien['SAL_MONTH_LOW'] < 100000
                     and dien['SAL_MONTH_HIGH'] > 18000
                     and dien['SAL_MONTH_HIGH'] < 200000
                     and dien['LON'] < 125
                     and dien['LON'] > 117
                     and dien['bigadd'] != 0
                     and dien['smalladd'] != 0]

        for dien in hr104data:
            dien["lat"] = dien.pop("LAT")
            dien["lng"] = dien.pop("LON")
            del dien["_id"]

        if radius != "":  # lng1, lat1, lng2, lat2
            hr104data = [dien for dien in hr104data if
                         haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng, lat2=centerlat) < radius]

        return JsonResponse(hr104data, safe=False)


# @csrf_exempt
def human_count_list(request):
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd
    if smalladd != "":
        queryElements["smalladd"] = smalladd

    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""

    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.Nhuman
    Nhumandata = list(collection.find(queryElements))
    client.close()
    for dien in Nhumandata:
        dien["weight"] = int(dien.pop("Nhuman"))
        dien["add"] = dien.pop("_id")
    if radius != "":  # lng1, lat1, lng2, lat2
        Nhumandata = [dien for dien in Nhumandata if
                      haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng, lat2=centerlat) < radius]

    return JsonResponse(Nhumandata, safe=False)


# @csrf_exempt
def cost_power_list(request):
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd
    if smalladd != "":
        queryElements["smalladd"] = smalladd

    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""

    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.CostPower
    CostPowerdata = list(collection.find(queryElements))
    client.close()
    for dien in CostPowerdata:
        dien["weight"] = int(dien.pop('costPower'))
        dien["weight_invoice"] = int(dien.pop('invoice'))
        dien["add"] = dien.pop("_id")

    if radius != "":  # lng1, lat1, lng2, lat2
        CostPowerdata = [dien for dien in CostPowerdata if
                         haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng, lat2=centerlat) < radius]

    return JsonResponse(CostPowerdata, safe=False)


# @csrf_exempt
def bus_list(request):
    bigadd = request.POST.get('bigadd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigCity"] = bigadd.replace("台", "臺")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.busData
    Busdata = list(collection.find(queryElements))
    client.close()
    for dien in Busdata:
        # dien["weight"] = int(dien.pop('costPower'))
        dien["add"] = dien.pop("_id")
    if radius != "":  # lng1, lat1, lng2, lat2
        Busdata = [dien for dien in Busdata if
                   'lng' in dien and haversine(lng1=dien["lng"], lat1=dien["lat"], lng2=centerlng,
                                               lat2=centerlat) < 500]  # 改radius成500

    return JsonResponse(Busdata, safe=False)


# @csrf_exempt
def store_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("台", "臺")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("台", "臺")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.conStore
    storedata = list(collection.find(queryElements))
    client.close()
    # for dien in Busdata:
    #     # dien["weight"] = int(dien.pop('costPower'))
    #     dien["add"] = dien.pop("_id")
    if radius != "":  # lng1, lat1, lng2, lat2
        storedata = [dien for dien in storedata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(storedata, safe=False)


def watsons_list(request):
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("臺", "台")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("臺", "台")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.Watsons
    watsonsdatas = list(collection.find(queryElements))
    client.close()
    # for dien in Busdata:
    #     # dien["weight"] = int(dien.pop('costPower'))
    #     dien["add"] = dien.pop("_id")
    if radius != "":  # lng1, lat1, lng2, lat2
        watsonsdatas = [dien for dien in watsonsdatas if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(watsonsdatas, safe=False)

def canSuMe_list(request):
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("臺", "台")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("臺", "台")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.canSuMe
    canSuMedatas = list(collection.find(queryElements))
    client.close()
    # for dien in Busdata:
    #     # dien["weight"] = int(dien.pop('costPower'))
    #     dien["add"] = dien.pop("_id")
    if radius != "":  # lng1, lat1, lng2, lat2
        canSuMedatas = [dien for dien in canSuMedatas if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(canSuMedatas, safe=False)

def carrefour_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("臺", "台")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("臺", "台")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.carrefour
    carrefourdata = list(collection.find(queryElements))
    client.close()
    if radius != "":  # lng1, lat1, lng2, lat2
        carrefourdata = [dien for dien in carrefourdata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(carrefourdata, safe=False)

def pxmart_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("台", "臺")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("台", "臺")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.pxmart
    pxmartdata = list(collection.find(queryElements))
    client.close()
    if radius != "":  # lng1, lat1, lng2, lat2
        pxmartdata = [dien for dien in pxmartdata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(pxmartdata, safe=False)

def tstore_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("台", "臺")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("台", "臺")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.info3Store
    Tstoredata = list(collection.find(queryElements))
    client.close()
    if radius != "":  # lng1, lat1, lng2, lat2
        Tstoredata = [dien for dien in Tstoredata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(Tstoredata, safe=False)

def dahu_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("臺", "台")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("臺", "台")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.dahu
    Dahudata = list(collection.find(queryElements))
    client.close()
    if radius != "":  # lng1, lat1, lng2, lat2
        Dahudata = [dien for dien in Dahudata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(Dahudata, safe=False)

def clinic_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("台", "臺")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("台", "臺")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.infoClinic
    clinicdata = list(collection.find(queryElements))
    client.close()
    if radius != "":  # lng1, lat1, lng2, lat2
        clinicdata = [dien for dien in clinicdata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(clinicdata, safe=False)

def psch_list(request):
    # queryElements = {}
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["bigadd"] = bigadd.replace("台", "臺")
    if smalladd != "":
        queryElements["smalladd"] = smalladd.replace("台", "臺")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.primarySchool
    pschdata = list(collection.find(queryElements))
    client.close()
    if radius != "":  # lng1, lat1, lng2, lat2
        pschdata = [dien for dien in pschdata if
                     'lng' in dien and haversine(lng1=float(dien["lng"]), lat1=float(dien["lat"]), lng2=centerlng,
                                                 lat2=centerlat) < radius]
    return JsonResponse(pschdata, safe=False)

def mrt_list(request):
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.MRTinfo
    MRTdata = list(collection.find({}, {'_id': False}))
    client.close()
    return JsonResponse(MRTdata, safe=False)

def train_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.trainStation
    trainData = list(collection.find({}, {'_id': False}))
    client.close()
    return JsonResponse(trainData, safe=False)

def eslite_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.eslite
    esliteData = list(collection.find({}, {'_id': False}))
    client.close()
    return JsonResponse(esliteData, safe=False)


# @csrf_exempt
def taiwan_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.taiwanInfo
    TaiwanData = list(collection.find({"$or": [{'Nhuman_Analyze': {"$gt": 0}}, {'costPower_Analyze': {"$gt": 0}}]}))
    client.close()
    return JsonResponse(TaiwanData, safe=False)

def stonetwo_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.taiwanInfoStoneTwo
    stoneTwoData = list(collection.find({'score':{"$gt":2}}, {'_id': False}))
    client.close()
    return JsonResponse(stoneTwoData, safe=False)

def hot7_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.taiwanInfoHot7
    hot7Data = list(collection.find({'score':{"$gt":2}}, {'_id': False}))
    client.close()
    return JsonResponse(hot7Data, safe=False)

def maBoss_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.taiwanInfoMaBoss
    maBossData = list(collection.find({'score':{"$gt":2}}, {'_id': False}))
    client.close()
    return JsonResponse(maBossData, safe=False)

#############0725
def suFood_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.taiwanInfoSuFood
    suFoodData = list(collection.find({'score':{"$gt":2}}, {'_id': False}))
    client.close()
    return JsonResponse(suFoodData, safe=False)

def ita_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.taiwanInfoIta
    itaData = list(collection.find({'score':{"$gt":2}}, {'_id': False}))
    client.close()
    return JsonResponse(itaData, safe=False)
##############0725
# 0713
def realPrice_list(request):
    queryElements = {}
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.realPriceLogin
    realPriceData = list(collection.find({}, {'_id': False}))
    client.close()
    return JsonResponse(realPriceData, safe=False)
# 0713


def info591_list(request):
    print(request)
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["area"] = bigadd.replace("臺", "台")
    if smalladd != "":
        queryElements["city"] = smalladd.replace("臺", "台")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    print(queryElements)
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.info591
    Data591 = list(collection.find(queryElements))
    # Data591 = list(collection.find({'soldout':"0"}))
    print(centerlng, centerlat)
    if radius != "":
        Data591 = [data for data in Data591 if
                   'lat' in data and haversine(lng1=float(data["lng"]), lat1=float(data["lat"]), lng2=centerlng,
                                               lat2=centerlat) < radius and data['soldout'] == "0"]
    else:
        Data591 = [data for data in Data591 if
                   'lat' in data and data['soldout'] == "0"]

    client.close()
    return JsonResponse(Data591, safe=False)




def push(request):
    print(request.POST)
    # idn = request.POST.get('_id', "")
    name = request.POST.get('name', "")
    othername = request.POST.get('othername', "")
    add = request.POST.get('add', "")
    performance = request.POST.get('performance', "")

    data = {}
    idn = name + othername
    if name != "":
        data['name'] = name
    if othername != "":
        data['othername'] = othername
    if add != "":
        data['add'] = add
        ######################
        try:
            data['bigadd'] = re.findall("(\w\w[巿|市|縣])(\w\w?\w?[區|市|鎮|鄉])", data['add'])[0][0].replace("巿", "市")
        except:
            try:
                data['bigadd'] = re.findall("(\w\w[巿|市|縣])", data['add'])[0].replace("巿", "市")
            except:
                pass
        try:
            data['smalladd'] = re.findall("(\w\w[巿|市|縣])(\w\w?\w?[區|市|鎮|鄉|村])", data['add'])[0][1].replace("巿", "市")
        except:
            try:
                data['smalladd'] = re.findall("(\w\w?\w?[巿|區|市|鎮|鄉|村])", data['add'])[0].replace("巿", "市")
            except:
                pass
        gmaps = googlemaps.Client(key='AIzaSyAF9GKxqgmgDEW_h7M4TtM5CbkK03xnS0E')
        address = data['add']
        try:
            geocode_result = gmaps.geocode(address)
            if geocode_result == []:
                geocode_result = gmaps.geocode(address[:11])
            data['lat'] = geocode_result[0]['geometry']['location']['lat']
            data['lng'] = geocode_result[0]['geometry']['location']['lng']
        except:
            print(data['name'] + "-" + data['add'] + "無經緯度資料")
    ######################
    if performance != "":
        data['performance'] = performance

    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.departmentStore
    if request.POST.get('action') == "del":
        collection.delete_one({'_id': idn})
    elif request.POST.get('action') == "update" and data:
        collection.update_one({"_id": idn}, {'$set': data}, upsert=True)  # , upsert=True
    print(data)
    alldata = list(collection.find({"lat": {"$gt": 1}}))
    return JsonResponse(alldata, safe=False)


def wow(request):
    print(request.POST)
    income = request.POST.get('income', "")
    idn = request.POST.get('_id', "")
    data = {}
    if income != "":
        data['income'] = income

    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.wowprimediendata
    if request.POST.get('action') == "del":
        collection.update_one({"_id": idn}, {'$set': {"income": ""}})
    elif data:
        collection.update_one({"_id": idn}, {'$set': data})  # , upsert=True
    # alldata=list(collection.find({}))
    alldata = list(collection.find({'CloseDate': 'None', "lat": {"$gt": 1}}))
    # print(alldata)
    alldata = [i for i in alldata if "A" not in i['StoreNo'] \
               and "B" not in i['StoreNo'] \
               and i['StoreNo'][0] != '3' \
               and i['StoreNo'][:2] != '19' \
               and i['StoreNo'][:2] != '41' \
               and i['StoreNo'][:2] != '50']
    return JsonResponse(alldata, safe=False)

def my591_list(request):
    bigadd = request.POST.get('bigadd', "")
    smalladd = request.POST.get('smalladd', "")
    queryElements = {}
    # 特管>>有些資料花蓮市會抓到大區，因為他沒顯示縣
    if bigadd == "花蓮市":
        bigadd = "花蓮縣"
    if bigadd == "竹北市":
        bigadd = "新竹縣"
    if bigadd != "":
        queryElements["area"] = bigadd.replace("臺", "台")
    if smalladd != "":
        queryElements["city"] = smalladd.replace("臺", "台")
    try:
        radius = int(request.POST.get('radius', ""))
        centerlat = float(request.POST.get('centerlat', ""))
        centerlng = float(request.POST.get('centerlng', ""))
    except:
        radius = ""
        centerlat = ""
        centerlng = ""
    print(queryElements)
    client = pymongo.mongo_client.MongoClient("localhost", 27017, username='j122085', password='850605')
    collection = client.rawData.my591
    Datamy591 = list(collection.find(queryElements,{"_id":False}))
    # Data591 = list(collection.find({'soldout':"0"}))
    print(centerlng, centerlat)
    if radius != "":
        Datamy591 = [data for data in Datamy591 if
                   'lat' in data and haversine(lng1=float(data["lng"]), lat1=float(data["lat"]), lng2=centerlng,
                                               lat2=centerlat) < radius and data['soldout'] == "0"]

    else:
        Datamy591 = [data for data in Datamy591 if
                   'lat' in data and data['soldout'] == "0"]

    client.close()
    return JsonResponse(Datamy591, safe=False)



def legality(request):
    print(request.POST)
    # bigadd = request.POST.get('bigadd', "")
    rp=request.POST
    address=rp.get('address',"")
    brand=rp.get('careerno',"")
    street = rp.get('storetype', "")
    use = rp.get('use', "")
    x=json.loads(rp.get('floorinfo',[]))
    terAreaClass=rp.get("ter","")
    # print(x)
    layer={int(i["floor"]):float(i['fsize']) for i in x}

    try:
        result = [li.getComment(address=address, brand=brand, use=use, layer=layer, street=street,terAreaClass=terAreaClass)]
        print(result)
    except Exception as e:
        print(e)
    # result=[123,321]
    print(result)
    return JsonResponse(result, safe=False)

def Amap(request):
    return render(request, 'api/compare.html', {})

def Tmap(request):
    return render(request, 'api/map.html', {})

def legalityNet(request):
    return render(request, 'api/legality.html', {})

