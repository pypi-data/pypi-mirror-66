# encoding: utf-8

import ast
import os
import re

from httprunner import exceptions, utils

###############################################################################
##  parse content with variables and functions mapping
###############################################################################

def get_builtin_item(item_type, item_name):
    """

    Args:
        item_type (enum): "variables" or "functions"
        item_name (str): variable name or function name

    Returns:
        variable or function with the name of item_name

    """
    # override built_in module with debugtalk.py module
    from httprunner import loader
    built_in_module = loader.load_builtin_module()

    if item_type == "variables":
        try:
            return built_in_module["variables"][item_name]
        except KeyError:
            raise exceptions.VariableNotFound("{} is not found.".format(item_name))
    else:
        # item_type == "functions":
        try:
            return built_in_module["functions"][item_name]
        except KeyError:
            raise exceptions.FunctionNotFound("{} is not found.".format(item_name))


def parse_tests(testcases, variables_mapping=None):
    """ parse testcases configs, including variables/parameters/name/request.

    Args:
        testcases (list): testcase list, with config unparsed.
            [
                {   # testcase data structure
                    "config": {
                        "name": "desc1",
                        "path": "testcase1_path",
                        "variables": [],         # optional
                        "request": {}            # optional
                        "refs": {
                            "debugtalk": {
                                "variables": {},
                                "functions": {}
                            },
                            "env": {},
                            "def-api": {},
                            "def-testcase": {}
                        }
                    },
                    "teststeps": [
                        # teststep data structure
                        {
                            'name': 'test step desc2',
                            'variables': [],    # optional
                            'extract': [],      # optional
                            'validate': [],
                            'request': {},
                            'function_meta': {}
                        },
                        teststep2   # another teststep dict
                    ]
                },
                testcase_dict_2     # another testcase dict
            ]
        variables_mapping (dict): if variables_mapping is specified, it will override variables in config block.

    Returns:
        list: parsed testcases list, with config variables/parameters/name/request parsed.

    """
    variables_mapping = variables_mapping or {}
    parsed_testcases_list = []

    for testcase in testcases:
        testcase_config = testcase.setdefault("config", {})
        project_mapping = testcase_config.pop(
            "refs",
            {
                "debugtalk": {
                    "variables": {},
                    "functions": {}
                },
                "env": {},
                "def-api": {},
                "def-testcase": {}
            }
        )

        # parse config parameters
        config_parameters = testcase_config.pop("parameters", [])
        cartesian_product_parameters_list = parse_parameters(
            config_parameters,
            project_mapping["debugtalk"]["variables"],
            project_mapping["debugtalk"]["functions"]
        ) or [{}]

        for parameter_mapping in cartesian_product_parameters_list:
            testcase_dict = utils.deepcopy_dict(testcase)
            config = testcase_dict.get("config")

            # parse config variables
            raw_config_variables = config.get("variables", [])
            parsed_config_variables = parse_data(
                raw_config_variables,
                project_mapping["debugtalk"]["variables"],
                project_mapping["debugtalk"]["functions"]
            )

            # priority: passed in > debugtalk.py > parameters > variables
            # override variables mapping with parameters mapping
            config_variables = utils.override_mapping_list(
                parsed_config_variables, parameter_mapping)
            # merge debugtalk.py module variables
            config_variables.update(project_mapping["debugtalk"]["variables"])
            # override variables mapping with passed in variables_mapping
            config_variables = utils.override_mapping_list(
                config_variables, variables_mapping)

            testcase_dict["config"]["variables"] = config_variables

            # parse config name
            testcase_dict["config"]["name"] = parse_data(
                testcase_dict["config"].get("name", ""),
                config_variables,
                project_mapping["debugtalk"]["functions"]
            )

            # parse config request
            testcase_dict["config"]["request"] = parse_data(
                testcase_dict["config"].get("request", {}),
                config_variables,
                project_mapping["debugtalk"]["functions"]
            )

            # put loaded project functions to config
            testcase_dict["config"]["functions"] = project_mapping["debugtalk"]["functions"]
            parsed_testcases_list.append(testcase_dict)

    return parsed_testcases_list
