# coding: utf-8

"""
    BlackFox

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from blackfox_restapi.configuration import Configuration
from blackfox_restapi.models.convergency_criterion import ConvergencyCriterion


class OptimizationEngineConfig(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'crossover_distribution_index': 'int',
        'crossover_probability': 'float',
        'mutation_distribution_index': 'int',
        'mutation_probability': 'float',
        'proc_timeout_seconds': 'int',
        'max_num_of_generations': 'int',
        'population_size': 'int',
        'hyper_volume': 'ConvergencyCriterion'
    }

    attribute_map = {
        'crossover_distribution_index': 'crossoverDistributionIndex',
        'crossover_probability': 'crossoverProbability',
        'mutation_distribution_index': 'mutationDistributionIndex',
        'mutation_probability': 'mutationProbability',
        'proc_timeout_seconds': 'procTimeoutSeconds',
        'max_num_of_generations': 'maxNumOfGenerations',
        'population_size': 'populationSize',
        'hyper_volume': 'hyperVolume'
    }

    def __init__(self, crossover_distribution_index=20, crossover_probability=0.9, mutation_distribution_index=20, mutation_probability=0.01, proc_timeout_seconds=10800, max_num_of_generations=50, population_size=50, hyper_volume=ConvergencyCriterion(), local_vars_configuration=None):  # noqa: E501
        """OptimizationEngineConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._crossover_distribution_index = None
        self._crossover_probability = None
        self._mutation_distribution_index = None
        self._mutation_probability = None
        self._proc_timeout_seconds = None
        self._max_num_of_generations = None
        self._population_size = None
        self._hyper_volume = None
        self.discriminator = None

        if crossover_distribution_index is not None:
            self.crossover_distribution_index = crossover_distribution_index
        if crossover_probability is not None:
            self.crossover_probability = crossover_probability
        if mutation_distribution_index is not None:
            self.mutation_distribution_index = mutation_distribution_index
        if mutation_probability is not None:
            self.mutation_probability = mutation_probability
        self.proc_timeout_seconds = proc_timeout_seconds
        self.max_num_of_generations = max_num_of_generations
        if population_size is not None:
            self.population_size = population_size
        self.hyper_volume = hyper_volume

    @property
    def crossover_distribution_index(self):
        """Gets the crossover_distribution_index of this OptimizationEngineConfig.  # noqa: E501


        :return: The crossover_distribution_index of this OptimizationEngineConfig.  # noqa: E501
        :rtype: int
        """
        return self._crossover_distribution_index

    @crossover_distribution_index.setter
    def crossover_distribution_index(self, crossover_distribution_index):
        """Sets the crossover_distribution_index of this OptimizationEngineConfig.


        :param crossover_distribution_index: The crossover_distribution_index of this OptimizationEngineConfig.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                crossover_distribution_index is not None and crossover_distribution_index > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `crossover_distribution_index`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                crossover_distribution_index is not None and crossover_distribution_index < 0):  # noqa: E501
            raise ValueError("Invalid value for `crossover_distribution_index`, must be a value greater than or equal to `0`")  # noqa: E501

        self._crossover_distribution_index = crossover_distribution_index

    @property
    def crossover_probability(self):
        """Gets the crossover_probability of this OptimizationEngineConfig.  # noqa: E501


        :return: The crossover_probability of this OptimizationEngineConfig.  # noqa: E501
        :rtype: float
        """
        return self._crossover_probability

    @crossover_probability.setter
    def crossover_probability(self, crossover_probability):
        """Sets the crossover_probability of this OptimizationEngineConfig.


        :param crossover_probability: The crossover_probability of this OptimizationEngineConfig.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                crossover_probability is not None and crossover_probability > 1):  # noqa: E501
            raise ValueError("Invalid value for `crossover_probability`, must be a value less than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                crossover_probability is not None and crossover_probability < 0):  # noqa: E501
            raise ValueError("Invalid value for `crossover_probability`, must be a value greater than or equal to `0`")  # noqa: E501

        self._crossover_probability = crossover_probability

    @property
    def mutation_distribution_index(self):
        """Gets the mutation_distribution_index of this OptimizationEngineConfig.  # noqa: E501


        :return: The mutation_distribution_index of this OptimizationEngineConfig.  # noqa: E501
        :rtype: int
        """
        return self._mutation_distribution_index

    @mutation_distribution_index.setter
    def mutation_distribution_index(self, mutation_distribution_index):
        """Sets the mutation_distribution_index of this OptimizationEngineConfig.


        :param mutation_distribution_index: The mutation_distribution_index of this OptimizationEngineConfig.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                mutation_distribution_index is not None and mutation_distribution_index > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `mutation_distribution_index`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                mutation_distribution_index is not None and mutation_distribution_index < 0):  # noqa: E501
            raise ValueError("Invalid value for `mutation_distribution_index`, must be a value greater than or equal to `0`")  # noqa: E501

        self._mutation_distribution_index = mutation_distribution_index

    @property
    def mutation_probability(self):
        """Gets the mutation_probability of this OptimizationEngineConfig.  # noqa: E501


        :return: The mutation_probability of this OptimizationEngineConfig.  # noqa: E501
        :rtype: float
        """
        return self._mutation_probability

    @mutation_probability.setter
    def mutation_probability(self, mutation_probability):
        """Sets the mutation_probability of this OptimizationEngineConfig.


        :param mutation_probability: The mutation_probability of this OptimizationEngineConfig.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                mutation_probability is not None and mutation_probability > 1):  # noqa: E501
            raise ValueError("Invalid value for `mutation_probability`, must be a value less than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                mutation_probability is not None and mutation_probability < 0):  # noqa: E501
            raise ValueError("Invalid value for `mutation_probability`, must be a value greater than or equal to `0`")  # noqa: E501

        self._mutation_probability = mutation_probability

    @property
    def proc_timeout_seconds(self):
        """Gets the proc_timeout_seconds of this OptimizationEngineConfig.  # noqa: E501

        Time in seconds in which individual network must finish training.  If not finished in time error will have maximum value.  # noqa: E501

        :return: The proc_timeout_seconds of this OptimizationEngineConfig.  # noqa: E501
        :rtype: int
        """
        return self._proc_timeout_seconds

    @proc_timeout_seconds.setter
    def proc_timeout_seconds(self, proc_timeout_seconds):
        """Sets the proc_timeout_seconds of this OptimizationEngineConfig.

        Time in seconds in which individual network must finish training.  If not finished in time error will have maximum value.  # noqa: E501

        :param proc_timeout_seconds: The proc_timeout_seconds of this OptimizationEngineConfig.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and proc_timeout_seconds is None:  # noqa: E501
            raise ValueError("Invalid value for `proc_timeout_seconds`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                proc_timeout_seconds is not None and proc_timeout_seconds > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `proc_timeout_seconds`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                proc_timeout_seconds is not None and proc_timeout_seconds < 0):  # noqa: E501
            raise ValueError("Invalid value for `proc_timeout_seconds`, must be a value greater than or equal to `0`")  # noqa: E501

        self._proc_timeout_seconds = proc_timeout_seconds

    @property
    def max_num_of_generations(self):
        """Gets the max_num_of_generations of this OptimizationEngineConfig.  # noqa: E501

        Maximum number of generations in which to find optimal network  # noqa: E501

        :return: The max_num_of_generations of this OptimizationEngineConfig.  # noqa: E501
        :rtype: int
        """
        return self._max_num_of_generations

    @max_num_of_generations.setter
    def max_num_of_generations(self, max_num_of_generations):
        """Sets the max_num_of_generations of this OptimizationEngineConfig.

        Maximum number of generations in which to find optimal network  # noqa: E501

        :param max_num_of_generations: The max_num_of_generations of this OptimizationEngineConfig.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and max_num_of_generations is None:  # noqa: E501
            raise ValueError("Invalid value for `max_num_of_generations`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_num_of_generations is not None and max_num_of_generations > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `max_num_of_generations`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_num_of_generations is not None and max_num_of_generations < 1):  # noqa: E501
            raise ValueError("Invalid value for `max_num_of_generations`, must be a value greater than or equal to `1`")  # noqa: E501

        self._max_num_of_generations = max_num_of_generations

    @property
    def population_size(self):
        """Gets the population_size of this OptimizationEngineConfig.  # noqa: E501

        Number of individials in one generation  # noqa: E501

        :return: The population_size of this OptimizationEngineConfig.  # noqa: E501
        :rtype: int
        """
        return self._population_size

    @population_size.setter
    def population_size(self, population_size):
        """Sets the population_size of this OptimizationEngineConfig.

        Number of individials in one generation  # noqa: E501

        :param population_size: The population_size of this OptimizationEngineConfig.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                population_size is not None and population_size > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `population_size`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                population_size is not None and population_size < 2):  # noqa: E501
            raise ValueError("Invalid value for `population_size`, must be a value greater than or equal to `2`")  # noqa: E501

        self._population_size = population_size

    @property
    def hyper_volume(self):
        """Gets the hyper_volume of this OptimizationEngineConfig.  # noqa: E501

        Define hyper volume for early stopping  # noqa: E501

        :return: The hyper_volume of this OptimizationEngineConfig.  # noqa: E501
        :rtype: ConvergencyCriterion
        """
        return self._hyper_volume

    @hyper_volume.setter
    def hyper_volume(self, hyper_volume):
        """Sets the hyper_volume of this OptimizationEngineConfig.

        Define hyper volume for early stopping  # noqa: E501

        :param hyper_volume: The hyper_volume of this OptimizationEngineConfig.  # noqa: E501
        :type: ConvergencyCriterion
        """

        self._hyper_volume = hyper_volume

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OptimizationEngineConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OptimizationEngineConfig):
            return True

        return self.to_dict() != other.to_dict()
