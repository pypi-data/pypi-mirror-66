import os
import unittest

class InstallTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("..")
        os.system(r"del dist\* /q")
        os.system("python setup.py bdist_wheel")

    def test_install(self):
        os.chdir("dist")
        whl = list(filter(lambda a: a.endswith(".whl"), os.listdir(".")))[0]
        cmd = "pip install --upgrade %s" % whl
        print("install cmd[%s]" % cmd)
        os.system(cmd)



if __name__ == '__main__':
    unittest.main()
