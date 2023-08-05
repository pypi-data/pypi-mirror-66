# coding: utf-8

"""
    Canopy.Api

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from canopy.openapi.configuration import Configuration


class PoolSettings(object):
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
        'pool_id': 'str',
        'auto_scale_formula': 'str'
    }

    attribute_map = {
        'pool_id': 'poolId',
        'auto_scale_formula': 'autoScaleFormula'
    }

    def __init__(self, pool_id=None, auto_scale_formula=None, local_vars_configuration=None):  # noqa: E501
        """PoolSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pool_id = None
        self._auto_scale_formula = None
        self.discriminator = None

        if pool_id is not None:
            self.pool_id = pool_id
        if auto_scale_formula is not None:
            self.auto_scale_formula = auto_scale_formula

    @property
    def pool_id(self):
        """Gets the pool_id of this PoolSettings.  # noqa: E501


        :return: The pool_id of this PoolSettings.  # noqa: E501
        :rtype: str
        """
        return self._pool_id

    @pool_id.setter
    def pool_id(self, pool_id):
        """Sets the pool_id of this PoolSettings.


        :param pool_id: The pool_id of this PoolSettings.  # noqa: E501
        :type: str
        """

        self._pool_id = pool_id

    @property
    def auto_scale_formula(self):
        """Gets the auto_scale_formula of this PoolSettings.  # noqa: E501


        :return: The auto_scale_formula of this PoolSettings.  # noqa: E501
        :rtype: str
        """
        return self._auto_scale_formula

    @auto_scale_formula.setter
    def auto_scale_formula(self, auto_scale_formula):
        """Sets the auto_scale_formula of this PoolSettings.


        :param auto_scale_formula: The auto_scale_formula of this PoolSettings.  # noqa: E501
        :type: str
        """

        self._auto_scale_formula = auto_scale_formula

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
        if not isinstance(other, PoolSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PoolSettings):
            return True

        return self.to_dict() != other.to_dict()
