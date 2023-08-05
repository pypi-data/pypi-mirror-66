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


class PercentilesPoints(object):
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
        'percent': 'float',
        'duration': 'float'
    }

    attribute_map = {
        'percent': 'percent',
        'duration': 'duration'
    }

    def __init__(self, percent=None, duration=None, local_vars_configuration=None):  # noqa: E501
        """PercentilesPoints - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._percent = None
        self._duration = None
        self.discriminator = None

        if percent is not None:
            self.percent = percent
        if duration is not None:
            self.duration = duration

    @property
    def percent(self):
        """Gets the percent of this PercentilesPoints.  # noqa: E501

        The k-th percentile where  0.0 < k <= 100.0.  # noqa: E501

        :return: The percent of this PercentilesPoints.  # noqa: E501
        :rtype: float
        """
        return self._percent

    @percent.setter
    def percent(self, percent):
        """Sets the percent of this PercentilesPoints.

        The k-th percentile where  0.0 < k <= 100.0.  # noqa: E501

        :param percent: The percent of this PercentilesPoints.  # noqa: E501
        :type: float
        """

        self._percent = percent

    @property
    def duration(self):
        """Gets the duration of this PercentilesPoints.  # noqa: E501

        Value (duration in milliseconds) of this k-th percentiles.  # noqa: E501

        :return: The duration of this PercentilesPoints.  # noqa: E501
        :rtype: float
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this PercentilesPoints.

        Value (duration in milliseconds) of this k-th percentiles.  # noqa: E501

        :param duration: The duration of this PercentilesPoints.  # noqa: E501
        :type: float
        """

        self._duration = duration

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
        if not isinstance(other, PercentilesPoints):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PercentilesPoints):
            return True

        return self.to_dict() != other.to_dict()
