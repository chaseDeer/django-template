import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from adminapp.models import Users


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


# Obtain the wechat openid
# 获取openid
class Getopenid(APIView):
    def post(self, request):
        wxcode = request.data.get('code')
        wxspAppid = ""
        wxspSecret = ""
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
