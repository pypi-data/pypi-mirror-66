# -*- coding:utf-8 -*-
"""
文件上传下载接口
"""

from __future__ import absolute_import, unicode_literals, division, print_function
import base64
import logging
import sys
import traceback
from collections import Iterable
from future.utils import raise_
import json
import os
import requests

if sys.version.startswith("2."):
    FileNotFoundError = IOError

code_dict = {
    '0': "操作成功",
    '1': "请求失败",
    "128501": "参数异常",
    "128502": "缺少请求必传参数",
    "128503": "文件缺少扩展名",
    "128504": "目录不存在",
    "128505": "文件不存在",
    "128506": "不是文件",
    "128507": "文件已存在",
    "128508": "目录已存在",
    "128509": "读取超时",
    "128510": "保存文件失败",
    "128511": "文件夹创建失败",
    "128512": "连接超时",
    "128513": "读取文件失败",
    "128514": "权限不足",
}


def create_file(remote_path, x_type, req_url, file=None, filename=None,
                file_path=None, mount_path=None, replace=True,
                recovery_path=None, timeout=3, logger=logging):
    """
    在服务器创建文件
    :param remote_path: 远程存储目录
    :param x_type: 业务类型
    :param req_url: 请求URL地址，必传
    :param file: 文件流，若不选择文件路径则必传文件流，也可以是base64编码的文件
    :param filename: 文件名称， 当上传对象为文件流时必传
    :param file_path: 本地文件路径，可以选择文件路径或者文件流
    :param mount_path: 服务器mount地址
    :param replace: 当文件已在服务器存在时是否强制替换，默认替换
    :param recovery_path: 容灾路径，当文件上传非正常失败时（调用接口非正常错误码），将文件存储的本地地址
    :param timeout: 超时时间，默认3秒
    :param logger: 日志对象
    :return:
    """
    file_like_obj, code, err, ret_mount_path = None, None, None, " "
    try:
        logger = logger if logger else logging
        if not remote_path or not x_type or not req_url:
            return 128502, code_dict.get("128502"), ""
        if file:
            if not filename:
                return 128502, code_dict.get("128502"), ""
            if isinstance(file, bytes):
                file = base64.b64decode(file)
            if isinstance(file, Iterable):
                f_file = b''
                for f in file:
                    f_file += f
                file = f_file
            param = {'picData': (filename, file, 'application/octet-stream')}
        elif file_path:
            if not os.path.isfile(file_path):
                return 128506, code_dict.get("128506"), ""
            try:
                file_like_obj = open(file_path, 'rb')
            except FileNotFoundError:
                return 128505, code_dict.get("128505"), ""
            param = {'picData': file_like_obj}
        else:
            return 128502, code_dict.get("128502"), ""
        headers = {
            "X-File-Path": remote_path,
            "X-Type": x_type,
            'X-Replace': "1" if replace else "0"
        }
        if mount_path:
            headers["X-Mount-Path"] = mount_path
        resp = requests.post(url=req_url, files=param, headers=headers, verify=False, timeout=timeout)
        http_code = resp.status_code
        if http_code == 200:
            response = resp.content.decode('utf-8')
            try:
                body = json.loads(response)
            except Exception as exc:
                body = response
            code = body.get('code')
            err = body.get('err', '') if body.get('err', '') else code_dict.get(str(code))
            ret_mount_path = body.get('biz', {}).get('mountPath')
        else:
            code = 1
            err = "请求失败"
            ret_mount_path = ""
    except requests.ConnectTimeout:
        code, err, ret_mount_path = 128512, code_dict.get("128512"), ""
    except requests.exceptions.ConnectionError:
        code, err, ret_mount_path = 128512, code_dict.get("128512"), ""
    except requests.exceptions.ReadTimeout:
        code, err, ret_mount_path = 128509, code_dict.get("128509"), ""
    except Exception as exc:
        logger.error(traceback.format_exc())
        raise_(Exception, exc)
    finally:
        if (code in [128509, 128512, 1] or not code_dict.get(str(code), None)) and recovery_path:
            try:
                if not os.path.exists(recovery_path):
                    code, err, ret_mount_path = 128504, code_dict.get("128504"), ""
                if file_path:
                    file_gen = None
                    filename = os.path.basename(file_path)
                    try:
                        file_gen = gen_file(file_path)
                    except FileNotFoundError:
                        code, err, ret_mount_path = 128505, code_dict.get("128505"), ""
                    except IOError:
                        code, err, ret_mount_path = 128513, code_dict.get("128513"), ""
                    except Exception as exc:
                        logger.error(traceback.format_exc())
                        raise_(Exception, exc)
                    if file_gen:
                        with open(os.path.join(recovery_path, filename), 'ab') as f:
                            for fc in file_gen:
                                f.write(fc)
                else:
                    with open(os.path.join(recovery_path, filename), 'ab') as f:
                        f.write(file)
            except IOError:
                return 128510, code_dict.get("128510"), ""
            except Exception as exc:
                logger.error(traceback.format_exc())
                raise_(Exception, exc)
        if file_like_obj:
            file_like_obj.close()
    return code, err, ret_mount_path


def describe_file(remote_full_path, req_url, local_full_path=None,
                  recovery_full_path=None, return_file=True, timeout=3, logger=logging):
    """
    返回文件信息
    :param remote_full_path: 远程文件存储路径及完整文件名称，全地址
    :param recovery_full_path: 容灾目录文件，当非正常错误发生时，读取此文件
    :param req_url: 请求URL地址，必传
    :param local_full_path: 下载的文件本地存储路径包含文件名，全地址
    :param return_file: 是否需要将文件流返回, 如不返回则需要传入local_full_path，同时返回""
    :param timeout: 超时时间
    :param logger: 日志对象
    :return:
    """
    code, err, ret_file = None, None, " "
    try:
        logger = logger if logger else logging
        if not remote_full_path or not req_url:
            return 128502, code_dict.get("128502"), ""
        if recovery_full_path and not os.path.isfile(recovery_full_path):
            return 128506, code_dict.get("128506"), ""
        if not return_file:
            if not local_full_path:
                return 128502, code_dict.get("128502"), ""
            else:
                if os.path.exists(local_full_path):
                    return 128507, code_dict.get("128507"), ""
                if not str(os.path.split('./demo.py')[-1]).split(".")[1]:
                    return 128503, code_dict.get(str(128503)), ""
        param = {'locateFile': remote_full_path}
        resp = requests.post(url=req_url, json=param, verify=False, timeout=timeout)
        http_code = resp.status_code
        if http_code == 200:
            ret_file = resp.content
            if local_full_path:
                if not os.path.exists(local_full_path):
                    try:
                        with open(local_full_path, "wb") as f:
                            f.write(ret_file)
                    except IOError:
                        return 128513, code_dict.get("128513"), ""
                else:
                    return 128507, code_dict.get("128507"), ""
            code = 0
            err = '操作成功'
        elif http_code == 401:
            code = 128501
            err = code_dict.get(str(code))
            ret_file = ""
        elif http_code == 402:
            code = 128504
            err = code_dict.get(str(code))
            ret_file = ""
        elif http_code == 403:
            code = 128514
            err = code_dict.get(str(code))
            ret_file = ""
        elif http_code == 404:
            code = 128505
            err = code_dict.get(str(code))
            ret_file = ""
        elif http_code == 500:
            code = 1
            err = code_dict.get(str(code))
            ret_file = ""
        else:
            code = 1
            err = "请求失败"
            ret_file = ""
    except requests.ConnectTimeout:
        code, err, ret_file = 128512, code_dict.get("128512"), ""
    except requests.exceptions.ConnectionError:
        code, err, ret_file = 128512, code_dict.get("128512"), ""
    except requests.exceptions.ReadTimeout:
        code, err, ret_file = 128509, code_dict.get("128509"), ""
    except Exception as exc:
        logger.error(traceback.format_exc())
        raise_(Exception, exc)
    finally:
        try:
            if (code in [128509, 128512, 1] or not code_dict.get(str(code), None)) and recovery_full_path:
                try:
                    recovery_file = gen_file(recovery_full_path)
                    if local_full_path:
                        if not os.path.exists(local_full_path):
                            with open(local_full_path, "wb") as f:
                                for fc in recovery_file:
                                    f.write(fc)
                        else:
                            code, err, ret_file = 128507, code_dict.get("128507"), ""
                except FileNotFoundError:
                    code, err, ret_file = 128505, code_dict.get("128505"), ""
                except IOError:
                    code, err, ret_file = 128513, code_dict.get("128513"), ""
                except Exception as exc:
                    logger.error(traceback.format_exc())
                    raise_(Exception, exc)
            if not return_file:
                ret_file = ""
            return code, err, ret_file
        except Exception as exc:
            logger.error(traceback.format_exc())
            raise_(Exception, exc)


def modify_file(remote_full_path, req_url, modified_file_name, timeout=3, logger=logging):
    """
    修改文件名
    :param remote_full_path: 远程文件存储路径及完整文件名称，全地址
    :param req_url: 请求URL地址，必传
    :param modified_file_name: 修改后的文件名
    :param timeout: 超时时间
    :param logger: 日志对象
    :return:
    """
    code, err = None, None
    try:
        logger = logger if logger else logging
        if not remote_full_path or not req_url or not modified_file_name:
            return 128502, code_dict.get("128502")
        _, old_name = os.path.split(remote_full_path)
        if old_name == modified_file_name:
            return 128507, code_dict.get("128507")
        param = {'filePath': remote_full_path, 'fileName': modified_file_name}
        resp = requests.post(url=req_url, json=param, verify=False, timeout=timeout)
        http_code = resp.status_code
        if http_code == 200:
            response = resp.content.decode('utf-8')
            try:
                body = json.loads(response)
            except Exception as exc:
                body = response
            print(response)
            code = body.get('code')
            err = body.get('err', '') if body.get('err', '') else code_dict.get(str(code))
        else:
            code = 1
            err = "请求失败"
    except requests.ConnectTimeout:
        code, err = 128512, code_dict.get("128512")
    except requests.exceptions.ConnectionError:
        code, err = 128512, code_dict.get("128512")
    except requests.exceptions.ReadTimeout:
        code, err = 128509, code_dict.get("128509")
    except Exception as exc:
        logger.error(traceback.format_exc())
        raise_(Exception, exc)
    return code, err


def gen_file(file_path, size=1024):
    """
    将文件读取为文件流
    :param file_path:
    :param size:
    :return:
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read(size)
            while data:
                yield data
                data = f.read(size)
    except FileNotFoundError:
        raise_(FileNotFoundError, "文件不存在")
    except IOError:
        raise_(IOError, "文件读取失败")
    except Exception as exc:
        raise_(Exception, exc)
