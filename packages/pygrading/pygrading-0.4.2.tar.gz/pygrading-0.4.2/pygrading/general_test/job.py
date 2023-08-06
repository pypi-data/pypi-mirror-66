"""
    Name: job.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: The main process of a grading.
    Coding: UTF-8

    Change Log:
        **2020.02.04**
        Add get_result().

        **2020.02.03**
        Fix prework bug.

        **2020.02.01**
        Add custom result key.
        Change the order of prework run and postwork in gg.job().

        **2020.01.30**
        run()'s default value is None now.

        **2020.01.27**
        Create this file!
"""

from pygrading.general_test.testcase import TestCases
from typing import Dict, List
import json


# TODO 更新最佳实践，集成Job类，在Job类中添加prework、run、postwork的方法用于被继承


# noinspection PyBroadException
class Job(object):
    """Job

    A Job is a work flow, using run() function to handle each testcase.

    Attributes:
        run: A function can handle each testcase.
        prework: A function using to handel pre work. Default None.
        postwork: A function using to handel post work. Default None.
        testcases: An list of test cases. Default None.
        config: A dict of config information. Default None.
        is_terminate: A boolean when __terminate is True, job will exit immediately.
        result: A dict of grading result.For Example:
                {
                    "verdict":"可选，基本判定，一般为简要的评测结果描述或者简写，例如OJ系统的AC、PE、CE等",
                    "rank":{
                        "rank":"选择排行榜模式时，必须有该项，浮点数(正常值 ≥0)，该值决定了本次提交在排行榜上的位置，
                                排行榜从小到大排序。该rank可能来自后面几个值（value1、 value2、......）的加权。
                                如果提交的材料有误或者其它异常，将rank值置为负数，不参与排行!"，
                        "key1":"value1，可选，字符串，显示在排行榜上，Key1作为表头"，
                        "key2":"value2，可选，字符串，显示在排行榜上，Key2作为表头"，
                        ......
                    },
                    "score":"选择直接评测得分时，必须有该项，按照百分制给分，必须为大于等于0的整数，例如90",
                    "images":["可选，如果评测结果有图表，需要转换为base64或者SVG(启用HTML)格式", "图片2"],
                    "comment":"可选，评测结果的简要描述。",
                    "detail":"可选，评测结果的详细描述，可以包含协助查错的信息。布置作业的时候，可以选择是否显示这项信息。",
                    "secret":"可选，该信息只有教师评阅时才能看到。",
                    "HTML":"可选，如果置为enable，开发者可以使用HTML标签对verdict、comment、detail的输出内容进行渲染。"
                 }
    """

    def __init__(self, run=None, prework=None, testcases: TestCases = TestCases(), config: Dict = None, postwork=None):
        """Init Job instance"""
        self.run = run
        self.prework = prework
        self.postwork = postwork
        self.testcases = testcases
        self.config = config
        self.is_terminate = False
        self.result = {
            "verdict": "Unknown Error",
            "score": "0",
            "rank": {"rank": "-1"},
            "HTML": "enable"
        }
        self.summary = []

    def verdict(self, src: str):
        self.result["verdict"] = src

    def score(self, src: int):
        self.result["score"] = str(src)

    def rank(self, src: Dict):
        self.result["rank"] = src

    def images(self, src: List[str]):
        self.result["images"] = src

    def comment(self, src: str):
        self.result["comment"] = src

    def detail(self, src: str):
        self.result["detail"] = src

    def secret(self, src: str):
        self.result["secret"] = src

    def HTML(self, src: str):
        self.result["HTML"] = src

    def custom(self, key: str, value: str):
        self.result[key] = value

    def get_summary(self):
        return self.summary

    def get_result(self):
        return self.result

    def get_config(self):
        return self.config

    def get_total_score(self):
        ret = 0
        for i in self.summary:
            if type(i) == dict and "score" in i:
                ret += float(i["score"])
        return int(ret)

    def get_total_time(self):
        ret = 0
        for i in self.summary:
            if type(i) == dict and "time" in i:
                ret += int(i["time"])
        return int(ret)

    def set_testcases(self, testcases: TestCases):
        self.testcases = testcases

    def set_config(self, config: Dict):
        self.config = config

    def set_prework(self, prework):
        self.prework = prework

    def set_run(self, run):
        self.run = run

    def set_postwork(self, postwork):
        self.postwork = postwork

    def terminate(self):
        self.is_terminate = True

    def start(self) -> List:
        """Start a job and return summary"""
        if self.prework:
            self.prework(self)

        if self.is_terminate:
            return self.get_summary()

        testcases = self.testcases.get_testcases()
        for case in testcases:
            try:
                if self.run:
                    ret = self.run(self, case)
                    self.summary.append(ret)
            except Exception as e:
                self.summary.append({
                    "name": case.name,
                    "score": 0,
                    "verdict": "Runtime Error",
                    "output": str(e)
                })
            finally:
                if self.is_terminate:
                    return self.get_summary()
        if self.postwork:
            self.postwork(self)

        return self.get_summary()

    def print(self):
        str_json = json.dumps(self.result)
        print(str_json)


def job(prework=None, run=None, postwork=None):
    return Job(prework=prework, run=run, postwork=postwork)
