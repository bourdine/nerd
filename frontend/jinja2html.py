# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader
import json
import os
import argparse
import pyinotify

parser = argparse.ArgumentParser()
parser.add_argument("--DEV", action="store_true", help="Developers mode")
args = parser.parse_args()

env = Environment(loader=PackageLoader('jinja2html'))


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self):
        self.generate_html_all()

    def process_IN_CREATE(self, event):
        print 'create: ' + event.pathname
        self.generate_html_file(event.name)

    def process_IN_DELETE(self, event):
        print 'delete: ' + event.pathname
        self.generate_html_file(event.name)

    def process_IN_MODIFY(self, event):
        print 'modify: ' + event.pathname
        if event.name != "base.jinja2":
            self.generate_html_file(event.name)
        else:
            self.generate_html_all()

    def generate_html_all(self):
        for filename in os.listdir('./templates/'):
            if '.jinja2' in filename:
                self.generate_html_file(filename)

    def generate_html_file(self, filename):
        decoded_params = self.get_params()

        name, extension = filename.split('.')
        if name == "index":
            decoded_params["index"] = True

        template = env.get_template(filename)
        html = template.render(DEV=args.DEV, params=decoded_params)

        decoded_params["index"] = False

        f = open(name + '.html', 'w')
        f.write(html.encode('UTF-8'))
        f.close()

    def get_params(self):
        params = ''
        try:
            f = open('params.json', 'r')
            params = f.read()
            f.close()
        except Exception:
            pass

        decoded_params = json.loads(params)

        return decoded_params


wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, EventHandler())
mask = mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
wm.add_watch('./templates/', mask)
if args.DEV:
    notifier.loop()

exit(0)
