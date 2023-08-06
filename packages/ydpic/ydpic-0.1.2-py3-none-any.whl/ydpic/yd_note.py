import os
import random
import sys
from pathlib import Path
from urllib import parse

from prutils.pr_jinja2 import gen_file_use_template
from prutils.pr_requests import read_session, new_session, save_session, update_proxy, downloadfile
from prutils.pr_string import get_re_first_subs, rand_hex32
from prutils.pr_utils import get_timestamp13, md5, get_timestamp10, make_path_by_relfile


NOTE_TPL_PATH = make_path_by_relfile(__file__, "note_tpl.xml")
CONFIG_TPL_PATH = make_path_by_relfile(__file__, "config.ini.tpl")


def parse_tuku_url(url):
    return get_re_first_subs("/file/(.*?)/note/(.*?)/", url)


def parse_img_url(url):
    return get_re_first_subs(r"res/(\d+?)/(.*?)$", url)


def parse_share_url(url):
    return get_re_first_subs(r"noteshare\?id=(.*?)$", url)


def is_logined(s):
    url = "https://note.youdao.com/yws/mapi/user?method=get&vendor=&multilevelEnable=true"
    r = s.get(url)
    return r.status_code == 200


def login(s, username, password):
    url = "https://note.youdao.com/login/acc/urs/verify/check"
    params = {
        "app": "web",
        "product": "YNOTE",
        "tp": "urstoken",
        "cf": "6",
        "fr": "1",
        "systemName": "Windows",
        "deviceType": "WindowsPC",
        "ru": "https://note.youdao.com/signIn//loginCallback.html",
        "er": "https://note.youdao.com/signIn//loginCallback.html",
        "vcode": "",
        "timestamp": get_timestamp13()
    }
    data = {
        "username": username,
        "password": md5(password.encode())
    }
    s.post(url, params=params, data=data)


def _upload_img_step1(s, img_path):
    url = "https://note.youdao.com/yws/api/personal/sync/upload"
    params = {
        "cstk": s.cookies["YNOTE_CSTK"],
        "keyfrom": "web"
    }
    data = {
        "cstk": s.cookies["YNOTE_CSTK"],
    }
    headers = {
        "File-Size": str(Path(img_path).stat().st_size)
    }
    r = s.post(url, headers=headers, params=params, data=data)
    # {'multiPartsCount': 1, 'transmitId': '1585465015071E586', 'lastPartLength': 45822}
    assert (r.status_code == 200)
    return r


def _upload_img_step2(s, img_path, transmitId):
    url = "https://note.youdao.com/yws/api/personal/sync/upload" + "/" + transmitId
    params = {
        "cstk": s.cookies["YNOTE_CSTK"],
    }
    r = s.post(url, params=params, data=open(img_path, "rb"))
    assert (r.status_code == 200)
    return r


def _upload_img_step3(s, transmitId, resourceId):
    createTime = get_timestamp10()
    url = "https://note.youdao.com/yws/api/personal/sync"
    params = {
        "method": "putResource",
        "resourceId": resourceId,
        "resourceName": "{}.png".format(resourceId),
        "rootVersion": "-1",
        "sessionId": "",
        "transmitId": transmitId,
        "genIcon": "true",
        "createTime": createTime,
        "modifyTime": createTime,
        "keyfrom": "web",
        "cstk": s.cookies["YNOTE_CSTK"]
    }
    r = s.post(url, params=params)
    assert (r.status_code == 200)
    return r


def _upload_doc(s, img_url, parentId, fileId, output_file):
    url = "https://note.youdao.com/yws/api/personal/sync"
    params = {
        "method": "push",
        "keyfrom": "web",
        "cstk": s.cookies["YNOTE_CSTK"]
    }

    bodyString = gen_file_use_template(NOTE_TPL_PATH, output_file, **{
        "coId": str(random.randint(1000, 9999)) + "-" + get_timestamp13(),
        "source": img_url,
        "width": 40,
        "height": 40,
    })

    data = {
        "fileId": fileId,
        "parentId": parentId,
        "domain": "0",
        "rootVersion": "-1",
        "sessionId": "",
        "modifyTime": get_timestamp10(),
        "bodyString": bodyString,
        "transactionId": fileId,
        "transactionTime": get_timestamp10(),
        "orgEditorType": "1",
        "tags": "",
        "cstk": s.cookies["YNOTE_CSTK"]
    }
    r = s.post(url, params=params, data=data)
    assert (r.status_code == 200)
    return r


def upload_img(s, img_path, resourceId):
    r1 = _upload_img_step1(s, img_path)
    transmitId = r1.json()["transmitId"]
    r2 = _upload_img_step2(s, img_path, transmitId)
    r3 = _upload_img_step3(s, transmitId, resourceId)
    img_url = r3.headers["url"]
    return img_url


class YoudaoNote:
    def __init__(self, tuku_url, share_url, session_file, username, password, proxy, work_dir):
        self.work_dir = work_dir
        self.proxy = proxy
        self.password = password
        self.username = username
        self.session_file = session_file
        self.share_id = parse_share_url(share_url)[0]
        try:
            self.parentId, self.fileId = parse_tuku_url(tuku_url)
        except AttributeError:
            self.parentId, self.fileId = None, None

        self.s = None

    def load_session(self):
        # 加载session
        s = read_session(self.session_file)
        if not s:
            s = new_session()
        update_proxy(s, self.proxy)
        self.s = s

    def login(self, username, password):
        if not is_logined(self.s):
            login(self.s, username, password)
            assert (is_logined(self.s))
            save_session(self.s, self.session_file)

    def update_doc(self, img_url):
        output_file = make_path_by_relfile(self.work_dir, "tmp/output.xml")
        _upload_doc(self.s, img_url, self.parentId, self.fileId, output_file)

    def _get_final_img_url(self, img_url):
        version, xmlnote = parse_img_url(img_url)
        url = "http://note.youdao.com/yws/public/resource/{}/xmlnote/{}/{}".format(self.share_id, xmlnote, version)
        return url

    def pre_handle(self, url):
        # url = url.decode(sys.getdefaultencoding).encode("utf-8")
        r = parse.urlsplit(url)
        if r.scheme in ["http", "https"]:
            file_path = make_path_by_relfile(self.session_file, rand_hex32()[24:])
            downloadfile(url, file_path)
            url = file_path
        return url

    def process(self, files, resourceId_func):
        # 加载session
        self.load_session()

        # 登录
        self.login(self.username, self.password)

        img_urls = []
        for img_file in files:
            # 如果是网络图片，先下载到本地
            img_file = self.pre_handle(img_file)
            # 上传图片,获取图片URL
            img_url = upload_img(self.s, img_file, resourceId_func(img_file))
            # 更新共享文档
            # self.update_doc(img_url)
            img_urls.append(self._get_final_img_url(img_url))

        return img_urls

    def __del__(self):
        if self.s:
            self.s.close()
