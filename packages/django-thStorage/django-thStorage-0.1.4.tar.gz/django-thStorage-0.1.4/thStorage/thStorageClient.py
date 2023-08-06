#!/usr/bin/env python
# encoding: utf-8
# @author: LiChangsong
# @license: (C) Copyright 2013-2020/1/3, NSCC-TJ.AllRightsReserved.
# @contact: lics@nscc-tj.cn
# @software: 
# @file: thStorageClient.py
# @time: 2020/1/3 11:17
# @desc:


import hashlib
import time
import uuid
import requests

from rest_framework.response import Response
from django.conf import settings
from .errorList import *
from thStorage.models import NetDiskUser


def GenerateFailedResponse(errorInfo):
    '''
    根据错误码和错误描述，生成一个失败的消息。
    '''
    errorCode = errorInfo[0]
    errorDesc = errorInfo[1]
    print
    errorCode, errorDesc
    return Response({"success": "no",
                     "error_code": errorCode,
                     "error_desc": errorDesc})


def prefixAuth(console, cluster, username, encrypedToken, timestamp):
    '''
    对请求进行常规检查
    '''
    config = {
        'timestampInterval' : settings.TH_STORAGE_CONFIG["TOKEN_UPDATE_IMTERVAL"]
    }
    if console == 'web':
        nowTimestamp = int(time.time())
        if abs(nowTimestamp - int(timestamp)) > config['timestampInterval']:
            return {"status": 1, "error": 'timestampNotFit'}
            # return GenerateFailedResponse(generateError('timestampNotFit'))
        if not NetDiskUser.objects.filter(cluster=cluster, username=username).first():
            return {"status": 1, "error": 'UsernameNotExist'}
            # return GenerateFailedResponse(generateError('UsernameNotExist', username))
        if len(NetDiskUser.objects.filter(cluster=cluster, username=username)) > 1:
            return {"status": 1, "error": 'UsernameRepeat'}
            # return GenerateFailedResponse(generateError('UsernameRepeat', username))
        userInfo = NetDiskUser.objects.filter(cluster=cluster, username=username)[0]
        token = userInfo.tokenWeb
        tokenGererateTime = userInfo.tokenGererateTimeWeb
        tokenValidityPeriod = userInfo.tokenValidityPeriod
        if nowTimestamp > (tokenGererateTime + tokenValidityPeriod):
            return {"status": 1, "error": 'tokenTimeOut'}
            # return GenerateFailedResponse(generateError('tokenTimeOut', username))
        combToken = str(token) + str(timestamp)
        if not encrypedToken == hashlib.sha256(combToken.encode("utf-8")).hexdigest():
            return {"status": 1, "error": 'wrongToken'}
            # return GenerateFailedResponse(generateError('wrongToken', username))
        return {"status": 0}
    elif console == 'desk':
        nowTimestamp = int(time.time())
        if abs(nowTimestamp - int(timestamp)) > config['timestampInterval']:
            return {"status": 1, "error": 'timestampNotFit'}
        if not NetDiskUser.objects.filter(cluster=cluster, username=username):
            return {"status": 1, "error": 'UsernameNotExist'}
        if len(NetDiskUser.objects.filter(cluster=cluster, username=username)) > 1:
            return {"status": 1, "error": 'UsernameRepeat'}
        userInfo = NetDiskUser.objects.filter(cluster=cluster, username=username)[0]
        token = userInfo.tokenDesk
        tokenGererateTime = userInfo.tokenGererateTimeDesk
        tokenValidityPeriod = userInfo.tokenValidityPeriod
        if nowTimestamp > (tokenGererateTime + tokenValidityPeriod):
            return {"status": 1, "error": 'tokenTimeOut'}
        combToken = str(token) + str(timestamp)
        if not encrypedToken == hashlib.sha256(combToken).hexdigest():
            print
            "token:", token
            print
            "timestamp:", timestamp
            return {"status": 1, "error": 'wrongToken'}
        return {"status": 0}

def LoginAuth(func):
    '''验证登录装饰器，
    :param func:
    :return:
    '''
    def wrapper(request,*args,**kwargs):
        if request.method == "GET":
            inputData = request.GET
        else:
            inputData = request.data

        console = inputData.get("console")
        username = inputData.get("username")
        timestamp = inputData.get("timestamp")
        token = inputData.get("encrypedToken")
        cluster = inputData.get("cluster")
        checkPrefix = prefixAuth(console,cluster,username,token,timestamp)

        if not checkPrefix['status'] == 0:
            error = checkPrefix['error']
            return GenerateFailedResponse(generateError(error, username))

        return func(request, *args, **kwargs)
    return wrapper

class THStorageUser:
    def __init__(self,username,cluster,systemUsername):
        self.username = username
        self.cluster = cluster
        self.systemUsername = systemUsername

    def GenerateToken(self):
        '''
        生成一个32位的随机令牌
        '''
        random_str = str(uuid.uuid1())
        m = hashlib.md5()
        m.update(random_str.encode("utf8"))
        token = m.hexdigest()
        tokenGererateTime = int(time.time())
        tokenValidityPeriod = time.time() + settings.TH_STORAGE_CONFIG.get("TOKEN_UPDATE_IMTERVAL",36000000)
        return token,tokenGererateTime,tokenValidityPeriod

    def Login(self,console):
        user = NetDiskUser.objects.filter(username=self.username,systemUsername=self.systemUsername,cluster=self.cluster).first()
        token,tokenGererateTime,tokenValidityPeriod = self.GenerateToken()
        nowTime = int(time.time())

        if not user:
            if console == "desk":
                NetDiskUser.objects.create(cluster=self.cluster,
                                       username=self.username,
                                       systemUsername=self.systemUsername,
                                       tokenValidityPeriod=36000000,
                                       tokenDesk=token,
                                       tokenGererateTimeDesk=nowTime, )
            if console == "web":
                NetDiskUser.objects.create(cluster=self.cluster,
                                           username=self.username,
                                           systemUsername=self.systemUsername,
                                           tokenValidityPeriod=36000000,
                                           tokenWeb=token,
                                           tokenGererateTimeWeb=nowTime, )
        else:
            if console == "desk":
                NetDiskUser.objects.filter(username=self.username, systemUsername=self.systemUsername,
                                           cluster=self.cluster).update(tokenDesk=token,
                                                                        tokenGererateTimeDesk=tokenGererateTime,
                                                                        tokenValidityPeriod=tokenValidityPeriod)
            if console == "web":
                NetDiskUser.objects.filter(username=self.username, systemUsername=self.systemUsername,
                                           cluster=self.cluster).update(tokenWeb=token,
                                                                        tokenGererateTimeWeb=tokenGererateTime,
                                                                        tokenValidityPeriod=tokenValidityPeriod)

        return token,self.username,self.cluster,self.systemUsername

class THSClient:
    def __init__(self, appid, appkey, server, cluster, user, path, timeout=60, chunk_size=65536):
        self.appid = appid
        self.appkey = appkey
        self.server = server
        self.cluster = cluster
        self.user = user
        self.path = path
        self.timeout = timeout
        self.chunk_size = chunk_size

    def _make_sig(self, timestamp):
        str1 = "appkey=%s&timestamp=%s&cluster=%s&user=%s&path=%s" % (
            self.appkey, timestamp, self.cluster, self.user, self.path)
        hashStr = hashlib.sha256()
        hashStr.update(str1.encode())
        sig = hashStr.hexdigest()
        return sig

    def _make_sig2(self, timestamp):
        str1 = "appkey=%s&timestamp=%s&cluster=%s&user=%s" % (
            self.appkey, timestamp, self.cluster, self.user)
        hashStr = hashlib.sha256()
        hashStr.update(str1.encode())
        sig = hashStr.hexdigest()
        return sig

    def listObjects(self, sort="modify", desc=1, page=1, count=0, search=""):
        url = "%s/v1/%s/%s/storage/listObject?appid=%s&sort=%s&desc=%s&page=%s&count=%s&search=%s" % (
            self.server, self.cluster, self.user, self.appid, sort, desc, page, count, search)
        print("11111111111111:"+url)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return resp.json()
        else:
            raise ValueError(resp.json())

    def createObject(self, dir=0):
        url = "%s/v1/%s/%s/storage/createObject?appid=%s&dir=%s" % (
        self.server, self.cluster, self.user, self.appid, dir)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return {}
        else:
            raise ValueError(resp.json())

    def getObjectMeta(self):
        url = "%s/v1/%s/%s/storage/getObjectMeta?appid=%s" % (
            self.server, self.cluster, self.user, self.appid)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return resp.json()
        else:
            raise ValueError(resp.json())

    def copyObject(self, sourcePath, recursive=0):
        url = "%s/v1/%s/%s/storage/copyObject?appid=%s&recursive=%s" % (
            self.server, self.cluster, self.user, self.appid, recursive)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
            "sourcePath": sourcePath
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return {}
        else:
            raise ValueError(resp.json())

    def moveObject(self, sourcePath, recursive=0):
        url = "%s/v1/%s/%s/storage/moveObject?appid=%s&recursive=%s" % (
            self.server, self.cluster, self.user, self.appid, recursive)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
            "sourcePath": sourcePath
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return {}
        else:
            raise ValueError(resp.json())

    def deleteObject(self, recursive=0):
        url = "%s/v1/%s/%s/storage/deleteObject?appid=%s&recursive=%s" % (
            self.server, self.cluster, self.user, self.appid, recursive)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return {}
        else:
            raise ValueError(resp.json())

    def getObject(self, limit=0, offset=0):
        url = "%s/v1/%s/%s/storage/getObject?appid=%s&limit=%s&offset=%s" % (
            self.server, self.cluster, self.user, self.appid, limit, offset)
        print(url)
        print("222222222")
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return resp.content
        else:
            raise ValueError(resp.json())

    def putObject(self, file):
        url = "%s/v1/%s/%s/storage/putObject?appid=%s" % (self.server, self.cluster, self.user, self.appid)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }
        files = {'file': file}

        resp = requests.post(url=url, data=data, files=files, timeout=self.timeout)

        if resp.status_code < 300:
            return {}
        else:
            raise ValueError(resp.json())

    def appendObject(self, file):
        url = "%s/v1/%s/%s/storage/appendObject?appid=%s" % (self.server, self.cluster, self.user, self.appid)
        timestamp = int(time.time())
        data = {
            "path": self.path,
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }
        files = {'file': file}

        resp = requests.post(url=url, data=data, files=files, timeout=self.timeout)

        if resp.status_code < 300:
            return {}
        else:
            raise ValueError(resp.json())

    def getQuota(self):
        url = "%s/v1/%s/%s/storage/quota?appid=%s" % (
            self.server, self.cluster, self.user, self.appid)
        timestamp = int(time.time())
        data = {
            "role": 'u',
            "sig": self._make_sig2(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)
        print("getQuota:", resp.json())

        if resp.status_code < 300:
            if resp.json().get("kbytes").find("*") > 0 :
                print("55555")
                respJ = resp.json()
                respJ["kbytes"] = respJ["kbytes"].replace("*","")
                return respJ
            return resp.json()
        else:
            raise ValueError(resp.json())