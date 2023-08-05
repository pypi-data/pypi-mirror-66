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


class ConfigReference(object):
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
        'tenant': 'TenantConfigReference',
        'default': 'DefaultConfigReference'
    }

    attribute_map = {
        'tenant': 'tenant',
        'default': 'default'
    }

    def __init__(self, tenant=None, default=None, local_vars_configuration=None):  # noqa: E501
        """ConfigReference - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._tenant = None
        self._default = None
        self.discriminator = None

        if tenant is not None:
            self.tenant = tenant
        if default is not None:
            self.default = default

    @property
    def tenant(self):
        """Gets the tenant of this ConfigReference.  # noqa: E501


        :return: The tenant of this ConfigReference.  # noqa: E501
        :rtype: TenantConfigReference
        """
        return self._tenant

    @tenant.setter
    def tenant(self, tenant):
        """Sets the tenant of this ConfigReference.


        :param tenant: The tenant of this ConfigReference.  # noqa: E501
        :type: TenantConfigReference
        """

        self._tenant = tenant

    @property
    def default(self):
        """Gets the default of this ConfigReference.  # noqa: E501


        :return: The default of this ConfigReference.  # noqa: E501
        :rtype: DefaultConfigReference
        """
        return self._default

    @default.setter
    def default(self, default):
        """Sets the default of this ConfigReference.


        :param default: The default of this ConfigReference.  # noqa: E501
        :type: DefaultConfigReference
        """

        self._default = default

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
        if not isinstance(other, ConfigReference):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConfigReference):
            return True

        return self.to_dict() != other.to_dict()
