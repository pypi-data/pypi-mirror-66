import configparser

from prutils.pr_utils import make_path_by_relfile


class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.conf.read(file_path, encoding="utf-8")

    @property
    def password(self):
        return self.conf.get("basic", "password")

    @property
    def username(self):
        return self.conf.get("basic", "username")

    @property
    def session_file(self):
        val = make_path_by_relfile(self.file_path, "tmp/{}_session".format(self.username))
        return self.conf.get("advanced", "session_file", fallback=val)

    @property
    def tuku_note_url(self):
        return self.conf.get("basic", "tuku_note_url", fallback="")

    @property
    def share_url(self):
        return self.conf.get("basic", "share_url")

    @property
    def proxy(self):
        return self.conf.get("advanced", "proxy", fallback=None)

    @property
    def link_resourceId(self):
        return self.conf.getboolean("advanced", "link_resourceId", fallback=False)

