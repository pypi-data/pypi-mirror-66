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
from blackfox_restapi.models.ann_optimization_engine_config import AnnOptimizationEngineConfig  # noqa: E501
from blackfox_restapi.rest import ApiException

class TestAnnOptimizationEngineConfig(unittest.TestCase):
    """AnnOptimizationEngineConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AnnOptimizationEngineConfig
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = blackfox_restapi.models.ann_optimization_engine_config.AnnOptimizationEngineConfig()  # noqa: E501
        if include_optional :
            return AnnOptimizationEngineConfig(
                optimization_algorithm = VidnerovaNeruda, 
                crossover_distribution_index = 0, 
                crossover_probability = 0, 
                mutation_distribution_index = 0, 
                mutation_probability = 0, 
                proc_timeout_seconds = 0, 
                max_num_of_generations = 1, 
                population_size = 2, 
                hyper_volume = null
            )
        else :
            return AnnOptimizationEngineConfig(
                proc_timeout_seconds = 0,
                max_num_of_generations = 1,
        )

    def testAnnOptimizationEngineConfig(self):
        """Test AnnOptimizationEngineConfig"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
