import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# 获取openid
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from adminapp.models import Users, Images, Lunbo, Records


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

# Obtain the wechat openid
class Getopenid(APIView):
    def post(self, request):
        wxcode = request.data.get('code')
        wxspAppid = "wx0a08cb1681bc7d74"
        wxspSecret = "44946af771e204b784421db8ff444336"
        data = {
            "appid": wxspAppid,
            "secret": wxspSecret,
            "js_code": wxcode,
            "grant_type": "authorization_code"
        }
        url = "https://api.weixin.qq.com/sns/jscode2session"
        json_data = requests.post(url=url, data=data).json()
        print(json_data)
        data_user = Users.objects.filter(openid=json_data['openid']).all()
        sear = UsersSerializers(instance=data_user, many=True)
        return Response({'code': 200, 'data': sear.data, 'openid': json_data['openid']})


class Userminiinsert(APIView):

    def post(self, request):
        sear = UsersSerializers(data=request.data)
        print(request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)


class Userminiupdate(APIView):

    def put(self, request, id):
        data = Users.objects.get(pk=id)
        sear = UsersSerializers(instance=data, data=request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)


class LunboSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lunbo
        fields = "__all__"


class Lunbomini(APIView):

    def get(self, request):
        data_list = Lunbo.objects.filter(is_start=1).all()
        sear = LunboSerializers(instance=data_list, many=True)
        return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})


class RecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = "__all__"


class ImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class RecordsView(APIView):

    def get(self, request):
        id = request.query_params.get('id')
        is_finshed = request.query_params.get('is_finshed')
        create_time = request.query_params.get('create_time')
        data_list = Records.objects.filter(user_id=id, is_finshed__contains=is_finshed,
                                           create_time__contains=create_time).all()
        sear = RecordsSerializers(instance=data_list, many=True)
        list = []
        for item in sear.data:
            items = item
            data_list_ = Images.objects.filter(id=item['images_id']).all()
            sear_ = ImagesSerializers(instance=data_list_, many=True)
            items['images'] = sear_.data
            list.append(items)
        print(list)
        return Response({'code': 200, 'total': data_list.count(), 'data': list})

    def post(self, request):
        sear = RecordsSerializers(data=request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)


class RecordsminiViewdetail(APIView):

    def get(self, request, id):
        data = Records.objects.get(pk=id)
        sear = RecordsSerializers(instance=data, many=False)
        return Response(sear.data)

    def put(self, request, id):
        data = Records.objects.get(pk=id)
        sear = RecordsSerializers(instance=data, data=request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)


class ImagesminiView(APIView):

    def get(self, request):
        image_type = request.query_params.get('image_type')
        image_name = request.query_params.get('image_name')
        data_list = Images.objects.filter(image_type__icontains=image_type, image_name__icontains=image_name).all()
        sear = ImagesSerializers(instance=data_list, many=True)
        return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})

    def post(self, request):
        sear = ImagesSerializers(data=request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)


class ImagesminiViewdetail(APIView):

    def put(self, request, id):
        book = Images.objects.get(pk=id)
        sear = ImagesSerializers(instance=book, many=False)
        return Response(sear.data)
