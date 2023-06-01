import os
import time

from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from jwt import exceptions
from rest_framework.views import APIView

from adminapp.models import Users, Admins, Images, Lunbo, Records
from temp_admin_api import settings
from temp_admin_api.settings import BASE_DIR
from rest_framework import serializers
from rest_framework.response import Response
from django.core.cache import cache

import jwt
import datetime


# Create your views here.

# Use redis and jwt to generate and validate tokens
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
        user_object = Admins.objects.filter(username=username, password=password).first()
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
        image_name = timecuo + img.name
        print(image_name)
        save_path = '{}/up_image/{}'.format(settings.MEDIA_ROOT, image_name)
        with open(save_path, 'wb') as f:
            for content in img.chunks():
                f.write(content)
        return Response({'code': 200, 'mgs': '成功', 'url': image_name})


class AdminsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = "__all__"


class AdminsView(APIView, CzToken):

    def get(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            searchinfo = request.query_params.get('searchinfo')
            pageSize = request.query_params.get('pageSize')
            pageNumber = request.query_params.get('pageNumber')
            data_list = Admins.objects.filter(username__icontains=searchinfo).all()
            paginator = Paginator(data_list, pageSize)
            page = paginator.get_page(pageNumber)
            sear = AdminsSerializers(instance=page, many=True)
            return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})
        return Response(res)

    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            sear = AdminsSerializers(data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class AdminsViewdetail(APIView, CzToken):

    def get(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Admins.objects.get(pk=id)
            sear = AdminsSerializers(instance=data, many=False)
            return Response(sear.data)
        return Response(res)

    def delete(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            Admins.objects.get(pk=id).delete()
            return HttpResponse('1')
        return Response(res)

    def put(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Admins.objects.get(pk=id)
            sear = AdminsSerializers(instance=data, data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class UsersView(APIView, CzToken):

    def get(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            searchinfo = request.query_params.get('searchinfo')
            pageSize = request.query_params.get('pageSize')
            pageNumber = request.query_params.get('pageNumber')
            data_list = Users.objects.filter(nickname__icontains=searchinfo).all()
            paginator = Paginator(data_list, pageSize)
            page = paginator.get_page(pageNumber)
            sear = UsersSerializers(instance=page, many=True)
            return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})
        return Response(res)

    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            sear = UsersSerializers(data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class UsersViewdetail(APIView, CzToken):

    def get(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Users.objects.get(pk=id)
            sear = UsersSerializers(instance=data, many=False)
            return Response(sear.data)
        return Response(res)

    def delete(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            Users.objects.get(pk=id).delete()
            return HttpResponse('1')
        return Response(res)

    def put(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Users.objects.get(pk=id)
            sear = UsersSerializers(instance=data, data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class ImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class ImagesView(APIView, CzToken):

    def get(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            searchinfo = request.query_params.get('searchinfo')
            pageSize = request.query_params.get('pageSize')
            image_type = request.query_params.get('image_type')
            pageNumber = request.query_params.get('pageNumber')
            data_list = Images.objects.filter(image_name__icontains=searchinfo,image_type__icontains=image_type).all()
            paginator = Paginator(data_list, pageSize)
            page = paginator.get_page(pageNumber)
            sear = ImagesSerializers(instance=page, many=True)
            return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})
        return Response(res)

    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            sear = ImagesSerializers(data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class ImagesViewdetail(APIView, CzToken):

    def get(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Images.objects.get(pk=id)
            sear = ImagesSerializers(instance=data, many=False)
            return Response(sear.data)
        return Response(res)

    def delete(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            Images.objects.get(pk=id).delete()
            return HttpResponse('1')
        return Response(res)

    def put(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Images.objects.get(pk=id)
            sear = ImagesSerializers(instance=data, data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class RecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = "__all__"


class RecordsView(APIView, CzToken):

    def get(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            searchinfo = request.query_params.get('searchinfo')
            pageSize = request.query_params.get('pageSize')
            pageNumber = request.query_params.get('pageNumber')
            data_list = Records.objects.filter(user_id__icontains=searchinfo).all()
            paginator = Paginator(data_list, pageSize)
            page = paginator.get_page(pageNumber)
            sear = RecordsSerializers(instance=page, many=True)
            return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})
        return Response(res)

    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            sear = RecordsSerializers(data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class RecordsViewdetail(APIView, CzToken):

    def get(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Records.objects.get(pk=id)
            sear = RecordsSerializers(instance=data, many=False)
            return Response(sear.data)
        return Response(res)

    def delete(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            Records.objects.get(pk=id).delete()
            return HttpResponse('1')
        return Response(res)

    def put(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            data = Records.objects.get(pk=id)
            sear = RecordsSerializers(instance=data, data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class LunboSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lunbo
        fields = "__all__"


class LunboView(APIView, CzToken):

    def get(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            is_start = request.query_params.get('is_start')
            pageSize = request.query_params.get('pageSize')
            pageNumber = request.query_params.get('pageNumber')
            data_list = Lunbo.objects.filter(is_start__icontains=is_start).all()
            paginator = Paginator(data_list, pageSize)
            page = paginator.get_page(pageNumber)
            sear = LunboSerializers(instance=page, many=True)
            return Response({'code': 200, 'total': data_list.count(), 'data': sear.data})
        return Response(res)

    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            sear = LunboSerializers(data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class LunboViewdetail(APIView, CzToken):

    def get(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            book = Lunbo.objects.get(pk=id)
            sear = LunboSerializers(instance=book, many=False)
            return Response(sear.data)
        return Response(res)

    def delete(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            Lunbo.objects.get(pk=id).delete()
            return HttpResponse('1')
        return Response(res)

    def put(self, request, id):
        res = self.CheckToken(request)
        if res['code'] == 200:
            book = Lunbo.objects.get(pk=id)
            sear = LunboSerializers(instance=book, data=request.data)
            if sear.is_valid():
                sear.save()
                return Response(sear.data)
            else:
                return Response(sear.errors)
        return Response(res)


class Resetpassw(APIView, CzToken):
    def post(self, request):
        res = self.CheckToken(request)
        if res['code'] == 200:
            loginName = request.data.get('loginName')
            oldpass = request.data.get('oldpass')
            newpass = request.data.get('newpass')
            data = Admins.objects.filter(username=loginName).first()
            sear = AdminsSerializers(instance=data)
            print(sear.data)
            if sear.data['password'] != oldpass:
                return Response({'code': 4033, 'msg': '旧密码有误'})
            else:
                Admins.objects.filter(username=loginName).update(password=newpass)
                return Response({'code': 200, 'msg': '修改成功！'})
        return Response(res)


