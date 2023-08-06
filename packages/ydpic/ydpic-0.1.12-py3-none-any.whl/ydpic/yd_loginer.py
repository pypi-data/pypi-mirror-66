from prutils.pr_utils import get_timestamp13, md5


class YDLoginer():
    def __init__(self, s, username, password):
        self.s = s
        self.password = password
        self.username = username

    def is_logined(self):
        url = "https://note.youdao.com/yws/mapi/user?method=get&vendor=&multilevelEnable=true"
        r = self.s.get(url)
        return r.status_code == 200

    def do_login(self):
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
            "username": self.username,
            "password": md5(self.password.encode())
        }
        self.s.post(url, params=params, data=data)

    def login(self):
        if not self.is_logined():
            self.do_login()
            assert(self.is_logined())
