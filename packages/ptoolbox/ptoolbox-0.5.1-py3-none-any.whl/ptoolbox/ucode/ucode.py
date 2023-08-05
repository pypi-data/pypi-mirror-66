# coding=utf-8
import json
import logging

__author__ = 'ThucNC'

import configparser
from typing import List, Union

import requests
from ptoolbox.dsa.dsa_problem import DsaProblem
from ptoolbox.helpers.clog import CLog
from ptoolbox.models.general_models import Problem, TestCase

_logger = logging.getLogger(__name__)


class UCode:
    def __init__(self, base_url, token):
        self.s = requests.session()
        self.api_base_url = base_url
        self.token = token
        self._headers = {
            'access-token': self.token
        }

    def get_api_url(self, path):
        return self.api_base_url + path

    def create_problem(self, lesson_id, problem: Union[Problem, str], score=10, xp=100):
        if isinstance(problem, str):
            problem: Problem = DsaProblem.load(problem, load_testcase=True)

        data = {
            "name": problem.name,
            "type": "code",
            "statement": problem.statement,
            "statement_format": "markdown",
            "input_desc": problem.input_format,
            "output_desc": problem.output_format,
            "constraints": problem.constraints,
            "compiler": "python",
            "statement_language": "vi",
            "score": score,
            "solution": problem.solution,
            "status": "string",
            "visibility": "public",
            "ucoin": xp
        }

        url = self.get_api_url(f"/lesson-item/{lesson_id}/question")
        response = self.s.post(url, json=data, headers=self._headers)

        print(response.status_code)
        res = response.json()
        print(res)
        if res['success']:
            question_id = res['data']['id']
            print("question_id:", question_id)
        else:
            raise Exception("Cannot create question:" + json.dumps(res))

        # upload testcase
        for testcase in problem.testcases:
            self.upload_testcase(question_id, testcase)

        return question_id

    def create_problems(self, lesson_id, problems: List[Problem], score=10, xp=100):
        question_ids = []
        for problem in problems:
            q_id = self.create_problem(self, lesson_id, problem, score, xp)
            question_ids.append(q_id)

        return question_ids

    def upload_testcase(self, problem_id, testcase: TestCase, is_sample=True, score=10):
        url = self.get_api_url(f"/question/{problem_id}/testcase")
        data = {
            "name": testcase.name,
            "explanation": testcase.explanation,
            "input": testcase.input,
            "output": testcase.output,
            "score": score,
            "is_sample": bool(is_sample)
        }

        response = self.s.post(url, json=data, headers=self._headers)
        print(response.status_code)
        res = response.json()
        print(res)
        if res['success']:
            testcase_id = res['data']['id']
            print("testcase_id:", testcase_id)
        else:
            CLog.error("Cannot create testcase:" + json.dumps(res))

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('UCODE'):
            CLog.error(f'Section `UCODE` should exist in {credential_file} file')
            return None, None
        if not config.has_option('UCODE', 'api_url') or not config.has_option('UCODE', 'token'):
            CLog.error(f'api_url and/or token are missing in {credential_file} file')
            return None, None

        api_url = config.get('UCODE', 'api_url')
        token = config.get('UCODE', 'token')

        return api_url, token


if __name__ == "__main__":
    ucode = UCode("https://dev-api.ucode.vn/api", "72821b59462c5fdb552a049c1caed85c")
    # problem_folder = "../../problems/domino_for_young"
    problem_folder = "/home/thuc/projects/ucode/courses/course-py101/lesson2/c1_input/p13_chao_ban"
    ucode_lesson_id = 172

    problem: Problem = DsaProblem.load(problem_folder, load_testcase=True)
    #
    # print(problem)
    #
    print(len(problem.testcases))
    for testcase in problem.testcases:
        print(testcase)


    # ucode.create_problem(lesson_id=172, problem=problem_folder)

