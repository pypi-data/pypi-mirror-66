# coding: utf-8

"""
    BlackFox

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import blackfox_restapi
from blackfox_restapi.models.output_window_config import OutputWindowConfig  # noqa: E501
from blackfox_restapi.rest import ApiException

class TestOutputWindowConfig(unittest.TestCase):
    """OutputWindowConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OutputWindowConfig
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = blackfox_restapi.models.output_window_config.OutputWindowConfig()  # noqa: E501
        if include_optional :
            return OutputWindowConfig(
                window = 56, 
                shift = 56
            )
        else :
            return OutputWindowConfig(
        )

    def testOutputWindowConfig(self):
        """Test OutputWindowConfig"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
