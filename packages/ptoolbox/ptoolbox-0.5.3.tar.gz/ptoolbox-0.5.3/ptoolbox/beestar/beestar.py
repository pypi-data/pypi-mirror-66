# coding=utf-8
import copy
import logging

__author__ = 'ThucNC'

import configparser
import os

import pypandoc as pypandoc
import requests
from bs4 import BeautifulSoup
from ptoolbox.helpers.clog import CLog

_logger = logging.getLogger(__name__)


class Beestar:
    def __init__(self):
        self.username = None
        self.csrf_token = None
        self.s = requests.session()
        self._headers = {
            'host': 'beestar.org',
            'origin': 'https://beestar.org',
            'referer': 'https://beestar.org/user?cmd=getLogin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
        }

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('BEESTAR'):
            CLog.error(f'Section `BEESTAR` should exist in {credential_file} file')
            return None
        if not config.has_option('BEESTAR', 'cookie'):
            CLog.error(f'cookie are missing in {credential_file} file')
            return None

        return config.get('BEESTAR', 'cookie')

    def login_by_cookie(self, cookie):
        self._headers['cookie'] = cookie

    def get_review_detail(self, review_url, output_file):
        headers = copy.deepcopy(self._headers)
        r = self.s.get(review_url, headers=headers)
        # print(r.status_code)
        # print(r.headers)
        # print(r.text)

        test_url = "https://beestar.org/exam?cmd=reviewresult"
        r = self.s.get(test_url, headers=headers)
        print(r.status_code)
        print(r.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        body = soup.select("body")[0]

        centers = soup.select("center")
        title = centers[0].select("h2")[0]
        centers[0].replaceWith(title)
        centers[-1].decompose()

        scripts = soup.select("script")
        for script in scripts:
            script.decompose()

        bookmarks = soup.select("span.bm")
        for bookmark in bookmarks:
            bookmark.decompose()

        inputs = soup.select("input")
        for input_tag in inputs:
            input_tag.decompose()

        body.attrs = {}
        imgs = soup.select("image")
        for img in imgs:
            if "white_diam.gif" in img['src']:
                img.decompose()
            elif "or_diam.gif" in img['src']:
                img['src'] = "https://beestar.org/images/or_diam.gif"

        with_ans = soup.prettify()

        imgs = soup.select("image")
        for img in imgs:
            if "diam.gif" in img['src']:
                img.decompose()

        fonts = soup.select("font")
        for font in fonts:
            if font['size'] == "2":
                font.decompose()

        without_ans = soup.prettify()

        with open(output_file, "w") as f:
            f.write(without_ans)
        filename, file_extension = os.path.splitext(output_file)
        out_file_with_ans = filename + "_ans" + file_extension
        with open(out_file_with_ans, "w") as f:
            f.write(with_ans)

        return without_ans, with_ans


if __name__ == "__main__":
    cookie = "JSESSIONID=3D1E55E372FEC17514ACD24CCFEF6428; beestar.div=4"
    beestar = Beestar()
    beestar.login_by_cookie(cookie)
    beestar.get_review_detail(
        "https://beestar.org/exam?cmd=startexerciseconfirm&session_num3=5840895393186993&status=FINISH&descID=186&exam_num=1&check_sus=true",
        "../../problems/beestar/result.html"
    )

    # output = pypandoc.convert_file(source_file="../../problems/beestar/result.html", format='html', to='docx',
    #                           outputfile="../../problems/beestar/result.docx")





