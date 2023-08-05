# coding: utf-8

"""
    NeoLoad API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class AsCodeFile(object):
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
        'path': 'str',
        'includes': 'list[str]'
    }

    attribute_map = {
        'path': 'path',
        'includes': 'includes'
    }

    def __init__(self, path=None, includes=None, local_vars_configuration=None):  # noqa: E501
        """AsCodeFile - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._path = None
        self._includes = None
        self.discriminator = None

        if path is not None:
            self.path = path
        if includes is not None:
            self.includes = includes

    @property
    def path(self):
        """Gets the path of this AsCodeFile.  # noqa: E501

        The yaml file path  # noqa: E501

        :return: The path of this AsCodeFile.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this AsCodeFile.

        The yaml file path  # noqa: E501

        :param path: The path of this AsCodeFile.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def includes(self):
        """Gets the includes of this AsCodeFile.  # noqa: E501

        List of yaml files included  # noqa: E501

        :return: The includes of this AsCodeFile.  # noqa: E501
        :rtype: list[str]
        """
        return self._includes

    @includes.setter
    def includes(self, includes):
        """Sets the includes of this AsCodeFile.

        List of yaml files included  # noqa: E501

        :param includes: The includes of this AsCodeFile.  # noqa: E501
        :type: list[str]
        """

        self._includes = includes

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
        if not isinstance(other, AsCodeFile):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsCodeFile):
            return True

        return self.to_dict() != other.to_dict()
