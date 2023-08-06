import argparse
import os
import shutil
import sys
import locale

from prutils.pr_utils import make_path_by_relfile


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), '..')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prutils.pr_string import rand_hex32, replace_chinese

from ydpic.config import Config
from ydpic.yd_note import YoudaoNote, CONFIG_TPL_PATH





def link_resourceId_func(img_file_path):
    # 有道对中文url支持有问题,将中文替换成"_"
    img_file_path = replace_chinese("_", img_file_path)
    return (os.path.basename(img_file_path).split(".", 1)[0] \
           + "_" + rand_hex32())

def default_resourceId_func(img_file_path):
    return "WEBRESOURCE" + rand_hex32()


def init_env(args):
    if not os.path.exists(args.tmp_dir):
        os.makedirs(args.tmp_dir)


def upload(args):
    if args.tmp_dir is None:
        args.tmp_dir = make_path_by_relfile(args.config_file_path, "tmp")

    init_env(args)
    # 获取配置
    conf = Config(args.config_file_path)

    # 创建功能对象
    ydn = YoudaoNote(conf.tuku_note_url, conf.share_url, conf.session_file,
                            conf.username, conf.password, conf.proxy, args.tmp_dir)

    # 可选使用自己定义的resourceId
    if conf.link_resourceId:
        resourceId_func = link_resourceId_func
    else:
        resourceId_func = default_resourceId_func

    urls = ydn.process(args.files, resourceId_func)

    if args.output_format == "markdown":
        format_urls = map(lambda url: "![]({})".format(url), urls)
        output = "\n".join(format_urls)
    elif args.output_format == "typora":
        output = '''
        Upload Success:
        {}
        '''.format("\n".join(urls))
    elif args.output_format == "row":
        output = "\n".join(urls)

    print(output)
    # print(output.encode("utf-8").decode(sys.getdefaultencoding()))
    # print(output.encode("utf-8").decode(locale.getdefaultlocale()[1]))



def init(args):
    shutil.copy(CONFIG_TPL_PATH, args.output_file)


def test():
    import PySimpleGUI as sg

    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Some text on Row 1')],
              [sg.Text('Enter something on Row 2'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    window.close()


def main():
    # test()
    parser = argparse.ArgumentParser(description='上传图片到有道云笔记，返回指定格式的图片地址.')
    if sys.version_info > (3, 6):
        subparsers = parser.add_subparsers(dest="cmd", required=True)
    else:
        subparsers = parser.add_subparsers(dest="cmd")
    parser_upload = subparsers.add_parser('upload')
    parser_upload.add_argument("-c --config", dest="config_file_path", help="config file path.", default="config.ini")
    parser_upload.add_argument("-f --format", dest="output_format", help="img output format.", default="typora")
    parser_upload.add_argument("-t --tmp_dir", dest="tmp_dir", help="tmp_dir.", default=None)
    parser_upload.add_argument(dest="files", nargs='+', help='image files')
    parser_upload.set_defaults(func=upload)

    parser_new_config = subparsers.add_parser('init')
    parser_new_config.add_argument("-o", dest="output_file", default="config.ini")
    parser_new_config.set_defaults(func=init)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
