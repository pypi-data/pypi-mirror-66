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
from blackfox_restapi.models.convergency_criterion import ConvergencyCriterion  # noqa: E501
from blackfox_restapi.rest import ApiException

class TestConvergencyCriterion(unittest.TestCase):
    """ConvergencyCriterion unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ConvergencyCriterion
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = blackfox_restapi.models.convergency_criterion.ConvergencyCriterion()  # noqa: E501
        if include_optional :
            return ConvergencyCriterion(
                number_of_latest_generations = 56, 
                percentage_of_tolerance = 1.337
            )
        else :
            return ConvergencyCriterion(
        )

    def testConvergencyCriterion(self):
        """Test ConvergencyCriterion"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
