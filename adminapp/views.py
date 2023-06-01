import os
import time

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from jwt import exceptions
from rest_framework.views import APIView

from temp_admin_api import settings
from temp_admin_api.settings import BASE_DIR
from .models import Users, Article
from rest_framework import serializers
from rest_framework.response import Response
from django.core.cache import cache

import jwt
import datetime


# Create your views here.
class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["_all_"]
        # ["_all_"]


class CzToken:

    def CheckToken(self, req):
        token = req.headers['Authorization']
        salt = 'sdjakfhahshjkfhahjhf22323'
        msg = None
        verified_payload = None
        try:
            verified_payload = jwt.decode(token, salt, algorithms=['HS256'])
            redistoken = cache.get(verified_payload['username'])
            if redistoken:
                return {'code': 200, "data": verified_payload}
            else:
                return {'code': 403, "msg": 'token已失效'}
        except exceptions.ExpiredSignatureError:
            msg = 'token已失效'
        except jwt.DecodeError:
            msg = 'token认证失败'
        except jwt.InvalidTokenError:
            msg = '非法的token'
        if not verified_payload:
            return {'code': 403, "msg": msg}


class Login(APIView, CzToken):

    def post(self, request):
        salt = 'sdjakfhahshjkfhahjhf22323'
        username = request.data.get('username')
        password = request.data.get('password')
        user_object = Users.objects.filter(username=username, password=password).first()
        if not user_object:
            return Response({'code': 403, 'msg': '账号或密码错误'})
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        payload = {
            'user_id': user_object.id,
            'username': user_object.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)

        }
        result = jwt.encode(payload=payload, key=salt, algorithm="Hs256", headers=headers)
        cache.set(user_object.username, result, timeout=3600)
        return Response({'code': 200, 'token': result, 'username': user_object.username, 'msg': '登录成功！'})


class LoginOut(APIView, CzToken):

    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            cache.delete(res['data']['username'])
            return Response({'code': 200, 'msg': '退出成功！'})
        return Response(res)


class UploadImg(APIView):
    def post(self, request):
        img = request.FILES.get("filename", None)
        print("111", img)
        timecuo = str(round(time.time() * 1000))
        image_name = timecuo+img.name
        print(image_name)
        save_path = '{}/up_image/{}'.format(settings.MEDIA_ROOT, image_name)
        with open(save_path, 'wb') as f:
            for content in img.chunks():
                f.write(content)
        return Response({'code': 200, 'mgs': '成功', 'url': 'http://127.0.0.1:8000/media/up_image/'+image_name})


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleView(APIView):

    def get(self, request):
        # data_list = {}
        searchinfo = request.query_params.get('searchinfo')
        pageSize = request.query_params.get('pageSize')
        pageNumber = request.query_params.get('pageNumber')
        selectinfo =request.query_params.get('selectinfo')
        data_list = Article.objects.filter(title__icontains=searchinfo, type__icontains=selectinfo).all()
        paginator = Paginator(data_list, pageSize)
        page = paginator.get_page(pageNumber)
        # if searchinfo == "0":
        #     data_list = Article.objects.all()
        # else:
        #     data_list = Article.objects.filter(type__icontains=searchinfo).all()
        sear = ArticleSerializers(instance=page, many=True)
        return Response({'code':200,'total':data_list.count(),'data':sear.data})

    def post(self, request):
        print("data", request.data)
        sear = ArticleSerializers(data=request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)


class ArticleViewdetail(APIView):

    def get(self, request, id):
        book = Article.objects.get(pk=id)
        sear = ArticleSerializers(instance=book, many=False)
        return Response(sear.data)

    def delete(self, request, id):
        Article.objects.get(pk=id).delete()
        return HttpResponse('1')

    def put(self, request, id):
        book = Article.objects.get(pk=id)
        sear = ArticleSerializers(instance=book, data=request.data)
        if sear.is_valid():
            sear.save()
            return Response(sear.data)
        else:
            return Response(sear.errors)
