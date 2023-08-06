import argparse
import io
import os
import sys
import unittest

from ydpic.yd_loginer import YDLoginer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ydpic.config import Config
from prutils.pr_requests import load_session


class MyTestCase(unittest.TestCase):
    def test_config(self):
        conf = Config("./config.ini.tpl")
        print(conf.username)
        print(conf.password)

    def test_argpaser(self):
        def foo(args):
            print(args.x * args.y)

        def bar(args):
            print('((%s))' % args.z)

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser_foo = subparsers.add_parser('foo')
        parser_foo.add_argument('-x', type=int, default=1)
        parser_foo.add_argument('y', type=float)
        parser_foo.set_defaults(func=foo)

        # create the parser for the "bar" command
        parser_bar = subparsers.add_parser('bar')
        parser_bar.add_argument('z')
        parser_bar.set_defaults(func=bar)

        args = parser.parse_args('foo 1 -x 2 a b c d e '.split())
        print(args)
        args.func(args)

    def test_login(self):
        config_path = os.path.abspath("../config.ini")
        conf = Config(config_path)
        s = load_session(conf.session_file, conf.proxy)

        print(conf.username)
        print(conf.password)
        ydl = YDLoginer(s, conf.username, conf.username)
        ydl.login()

    def test_tk(self):
        import tkinter
        top = tkinter.Tk()
        # 进入消息循环
        top.mainloop()

    def test_t2(self):
        import tkinter as tk

        root = tk.Tk()
        image = tk.PhotoImage(file="../imgs/demo.gif")
        # image = tk.PhotoImage(file="../imgs/demo.gif", format="gif -index 10")
        label = tk.Label(image=image)
        label.pack()
        root.mainloop()

    def test_pysimplegui(self):
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

    def test_pysimplegui2(self):
        import PySimpleGUI as sg
        from PIL import Image, ImageTk, ImageDraw

        def draw_frame(target, im_path):  # Point
            """double-buffered redraw of the background image and the red rubber-rect"""
            img = Image.open(im_path).convert("RGBA")
            # img = Image.open(im_path)
            # ImageTk.PhotoImage(im_path)

            b = io.BytesIO()
            img.save(b, 'PNG')

            target.DrawImage(data=b.getvalue(), location=(200, 200))

        layout = [
            [
                sg.Graph(
                    canvas_size=(400, 400),
                    graph_bottom_left=(0, 0),
                    graph_top_right=(400, 400),
                    key="graph"
                )
            ],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
        ]

        window = sg.Window("rect on image", layout)
        window.Finalize()

        graph = window.Element("graph")
        im = Image.open("../imgs/get.jpg")
        buffer = im.copy()
        b = io.BytesIO()
        buffer.save(b, 'PNG')


        # graph.DrawImage(filename="../imgs/get.jpg", location=(0, 400))
        # graph.DrawImage(filename="../imgs/get.jpg", location=(0, 400))
        # graph.DrawImage(data=b.getvalue(), location=(0, 400))
        draw_frame(graph, "../imgs/get.jpg")
        # graph.DrawRectangle((200, 200), (250, 300), line_color="red")

        while True:
            event, values = window.Read()
            if event is None:
                break

    def test_remi(self):
        pass
if __name__ == '__main__':
    unittest.main()
