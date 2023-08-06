import unittest
from typing import List

from httprunner.schema import common
from httprunner.schema.api import Api
from httprunner.schema.common import TestsConfig
from httprunner.schema.testcase import TestStep


class ApiRunner(Api):

    name: common.Name
    variables: common.Variables = {}
    request: common.Request = {}

    def __init__(self, **variables):
        super().__init__(**variables)
        self.variables.update(variables)

    def run(self):
        pass


class TestCaseRunner(object):

    config: TestsConfig = {}
    teststeps: List[TestStep] = []

    def __init__(self, **variables):
        # super().__init__(methodName="run_test")
        self.config.variables.update(variables)

    def run_test(self):
        base_url = self.config.base_url
        for step in self.teststeps:
            print("-----", step.extract)
            variables = {}
            step.run(**variables)
