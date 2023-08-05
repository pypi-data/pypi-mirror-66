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


class ConfigResolvedReferenceData(object):
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
        'modified_date': 'datetime',
        'user_id': 'str',
        'name': 'str',
        'config_type': 'str',
        'hashes': 'list[ConfigHash]',
        'is_support_session_open': 'bool'
    }

    attribute_map = {
        'modified_date': 'modifiedDate',
        'user_id': 'userId',
        'name': 'name',
        'config_type': 'configType',
        'hashes': 'hashes',
        'is_support_session_open': 'isSupportSessionOpen'
    }

    def __init__(self, modified_date=None, user_id=None, name=None, config_type=None, hashes=None, is_support_session_open=None, local_vars_configuration=None):  # noqa: E501
        """ConfigResolvedReferenceData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._modified_date = None
        self._user_id = None
        self._name = None
        self._config_type = None
        self._hashes = None
        self._is_support_session_open = None
        self.discriminator = None

        if modified_date is not None:
            self.modified_date = modified_date
        if user_id is not None:
            self.user_id = user_id
        if name is not None:
            self.name = name
        if config_type is not None:
            self.config_type = config_type
        if hashes is not None:
            self.hashes = hashes
        if is_support_session_open is not None:
            self.is_support_session_open = is_support_session_open

    @property
    def modified_date(self):
        """Gets the modified_date of this ConfigResolvedReferenceData.  # noqa: E501


        :return: The modified_date of this ConfigResolvedReferenceData.  # noqa: E501
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """Sets the modified_date of this ConfigResolvedReferenceData.


        :param modified_date: The modified_date of this ConfigResolvedReferenceData.  # noqa: E501
        :type: datetime
        """

        self._modified_date = modified_date

    @property
    def user_id(self):
        """Gets the user_id of this ConfigResolvedReferenceData.  # noqa: E501


        :return: The user_id of this ConfigResolvedReferenceData.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ConfigResolvedReferenceData.


        :param user_id: The user_id of this ConfigResolvedReferenceData.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def name(self):
        """Gets the name of this ConfigResolvedReferenceData.  # noqa: E501


        :return: The name of this ConfigResolvedReferenceData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConfigResolvedReferenceData.


        :param name: The name of this ConfigResolvedReferenceData.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def config_type(self):
        """Gets the config_type of this ConfigResolvedReferenceData.  # noqa: E501


        :return: The config_type of this ConfigResolvedReferenceData.  # noqa: E501
        :rtype: str
        """
        return self._config_type

    @config_type.setter
    def config_type(self, config_type):
        """Sets the config_type of this ConfigResolvedReferenceData.


        :param config_type: The config_type of this ConfigResolvedReferenceData.  # noqa: E501
        :type: str
        """

        self._config_type = config_type

    @property
    def hashes(self):
        """Gets the hashes of this ConfigResolvedReferenceData.  # noqa: E501


        :return: The hashes of this ConfigResolvedReferenceData.  # noqa: E501
        :rtype: list[ConfigHash]
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes):
        """Sets the hashes of this ConfigResolvedReferenceData.


        :param hashes: The hashes of this ConfigResolvedReferenceData.  # noqa: E501
        :type: list[ConfigHash]
        """

        self._hashes = hashes

    @property
    def is_support_session_open(self):
        """Gets the is_support_session_open of this ConfigResolvedReferenceData.  # noqa: E501


        :return: The is_support_session_open of this ConfigResolvedReferenceData.  # noqa: E501
        :rtype: bool
        """
        return self._is_support_session_open

    @is_support_session_open.setter
    def is_support_session_open(self, is_support_session_open):
        """Sets the is_support_session_open of this ConfigResolvedReferenceData.


        :param is_support_session_open: The is_support_session_open of this ConfigResolvedReferenceData.  # noqa: E501
        :type: bool
        """

        self._is_support_session_open = is_support_session_open

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
        if not isinstance(other, ConfigResolvedReferenceData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConfigResolvedReferenceData):
            return True

        return self.to_dict() != other.to_dict()
