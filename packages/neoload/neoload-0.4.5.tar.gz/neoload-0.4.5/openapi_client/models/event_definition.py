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


class EventDefinition(object):
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
        'id': 'str',
        'code': 'str',
        'elementid': 'str',
        'fullname': 'str',
        'offset': 'int',
        'type': 'EventType',
        'duration': 'int',
        'source': 'str'
    }

    attribute_map = {
        'id': 'id',
        'code': 'code',
        'elementid': 'elementid',
        'fullname': 'fullname',
        'offset': 'offset',
        'type': 'type',
        'duration': 'duration',
        'source': 'source'
    }

    def __init__(self, id=None, code=None, elementid=None, fullname=None, offset=None, type=None, duration=None, source=None, local_vars_configuration=None):  # noqa: E501
        """EventDefinition - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._code = None
        self._elementid = None
        self._fullname = None
        self._offset = None
        self._type = None
        self._duration = None
        self._source = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if code is not None:
            self.code = code
        if elementid is not None:
            self.elementid = elementid
        if fullname is not None:
            self.fullname = fullname
        if offset is not None:
            self.offset = offset
        if type is not None:
            self.type = type
        if duration is not None:
            self.duration = duration
        if source is not None:
            self.source = source

    @property
    def id(self):
        """Gets the id of this EventDefinition.  # noqa: E501


        :return: The id of this EventDefinition.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this EventDefinition.


        :param id: The id of this EventDefinition.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def code(self):
        """Gets the code of this EventDefinition.  # noqa: E501


        :return: The code of this EventDefinition.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this EventDefinition.


        :param code: The code of this EventDefinition.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def elementid(self):
        """Gets the elementid of this EventDefinition.  # noqa: E501


        :return: The elementid of this EventDefinition.  # noqa: E501
        :rtype: str
        """
        return self._elementid

    @elementid.setter
    def elementid(self, elementid):
        """Sets the elementid of this EventDefinition.


        :param elementid: The elementid of this EventDefinition.  # noqa: E501
        :type: str
        """

        self._elementid = elementid

    @property
    def fullname(self):
        """Gets the fullname of this EventDefinition.  # noqa: E501


        :return: The fullname of this EventDefinition.  # noqa: E501
        :rtype: str
        """
        return self._fullname

    @fullname.setter
    def fullname(self, fullname):
        """Sets the fullname of this EventDefinition.


        :param fullname: The fullname of this EventDefinition.  # noqa: E501
        :type: str
        """

        self._fullname = fullname

    @property
    def offset(self):
        """Gets the offset of this EventDefinition.  # noqa: E501


        :return: The offset of this EventDefinition.  # noqa: E501
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this EventDefinition.


        :param offset: The offset of this EventDefinition.  # noqa: E501
        :type: int
        """

        self._offset = offset

    @property
    def type(self):
        """Gets the type of this EventDefinition.  # noqa: E501


        :return: The type of this EventDefinition.  # noqa: E501
        :rtype: EventType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this EventDefinition.


        :param type: The type of this EventDefinition.  # noqa: E501
        :type: EventType
        """

        self._type = type

    @property
    def duration(self):
        """Gets the duration of this EventDefinition.  # noqa: E501


        :return: The duration of this EventDefinition.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this EventDefinition.


        :param duration: The duration of this EventDefinition.  # noqa: E501
        :type: int
        """

        self._duration = duration

    @property
    def source(self):
        """Gets the source of this EventDefinition.  # noqa: E501


        :return: The source of this EventDefinition.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this EventDefinition.


        :param source: The source of this EventDefinition.  # noqa: E501
        :type: str
        """

        self._source = source

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
        if not isinstance(other, EventDefinition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EventDefinition):
            return True

        return self.to_dict() != other.to_dict()
