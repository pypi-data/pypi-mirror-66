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


class ReservationDefinition(object):
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
        'status': 'str',
        'start_date_time': 'float',
        'end_date_time': 'float',
        'reservation_web_v_us': 'float',
        'reservation_sapv_us': 'float',
        'controller_zone_id': 'str',
        'neoload_version': 'str',
        'lg_zones_resources_reservation': 'list[LgByZones]',
        'author': 'str',
        'owner': 'ReservationOwner',
        'name': 'str',
        'description': 'str',
        'type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'status': 'status',
        'start_date_time': 'startDateTime',
        'end_date_time': 'endDateTime',
        'reservation_web_v_us': 'reservationWebVUs',
        'reservation_sapv_us': 'reservationSAPVUs',
        'controller_zone_id': 'controllerZoneId',
        'neoload_version': 'neoloadVersion',
        'lg_zones_resources_reservation': 'lgZonesResourcesReservation',
        'author': 'author',
        'owner': 'owner',
        'name': 'name',
        'description': 'description',
        'type': 'type'
    }

    def __init__(self, id=None, status=None, start_date_time=None, end_date_time=None, reservation_web_v_us=None, reservation_sapv_us=None, controller_zone_id=None, neoload_version=None, lg_zones_resources_reservation=None, author=None, owner=None, name=None, description=None, type=None, local_vars_configuration=None):  # noqa: E501
        """ReservationDefinition - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._status = None
        self._start_date_time = None
        self._end_date_time = None
        self._reservation_web_v_us = None
        self._reservation_sapv_us = None
        self._controller_zone_id = None
        self._neoload_version = None
        self._lg_zones_resources_reservation = None
        self._author = None
        self._owner = None
        self._name = None
        self._description = None
        self._type = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if status is not None:
            self.status = status
        if start_date_time is not None:
            self.start_date_time = start_date_time
        if end_date_time is not None:
            self.end_date_time = end_date_time
        if reservation_web_v_us is not None:
            self.reservation_web_v_us = reservation_web_v_us
        if reservation_sapv_us is not None:
            self.reservation_sapv_us = reservation_sapv_us
        if controller_zone_id is not None:
            self.controller_zone_id = controller_zone_id
        if neoload_version is not None:
            self.neoload_version = neoload_version
        if lg_zones_resources_reservation is not None:
            self.lg_zones_resources_reservation = lg_zones_resources_reservation
        if author is not None:
            self.author = author
        if owner is not None:
            self.owner = owner
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if type is not None:
            self.type = type

    @property
    def id(self):
        """Gets the id of this ReservationDefinition.  # noqa: E501

        Unique identifier of the reservation.  # noqa: E501

        :return: The id of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ReservationDefinition.

        Unique identifier of the reservation.  # noqa: E501

        :param id: The id of this ReservationDefinition.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def status(self):
        """Gets the status of this ReservationDefinition.  # noqa: E501

        Status of the reservation.  # noqa: E501

        :return: The status of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ReservationDefinition.

        Status of the reservation.  # noqa: E501

        :param status: The status of this ReservationDefinition.  # noqa: E501
        :type: str
        """
        allowed_values = ["WAITING", "RUNNING", "PARTIALLY_RESERVED", "FAILED_TO_RESERVE", "RESERVED", "STOPPING", "ENDED"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def start_date_time(self):
        """Gets the start_date_time of this ReservationDefinition.  # noqa: E501

        Timestamp when the reservation begins. Number of seconds since January 1, 1970.  # noqa: E501

        :return: The start_date_time of this ReservationDefinition.  # noqa: E501
        :rtype: float
        """
        return self._start_date_time

    @start_date_time.setter
    def start_date_time(self, start_date_time):
        """Sets the start_date_time of this ReservationDefinition.

        Timestamp when the reservation begins. Number of seconds since January 1, 1970.  # noqa: E501

        :param start_date_time: The start_date_time of this ReservationDefinition.  # noqa: E501
        :type: float
        """

        self._start_date_time = start_date_time

    @property
    def end_date_time(self):
        """Gets the end_date_time of this ReservationDefinition.  # noqa: E501

        Timestamp when the reservation ends. Number of seconds since January 1, 1970.  # noqa: E501

        :return: The end_date_time of this ReservationDefinition.  # noqa: E501
        :rtype: float
        """
        return self._end_date_time

    @end_date_time.setter
    def end_date_time(self, end_date_time):
        """Sets the end_date_time of this ReservationDefinition.

        Timestamp when the reservation ends. Number of seconds since January 1, 1970.  # noqa: E501

        :param end_date_time: The end_date_time of this ReservationDefinition.  # noqa: E501
        :type: float
        """

        self._end_date_time = end_date_time

    @property
    def reservation_web_v_us(self):
        """Gets the reservation_web_v_us of this ReservationDefinition.  # noqa: E501

        The number of Web Virtual Users to be reserved.  # noqa: E501

        :return: The reservation_web_v_us of this ReservationDefinition.  # noqa: E501
        :rtype: float
        """
        return self._reservation_web_v_us

    @reservation_web_v_us.setter
    def reservation_web_v_us(self, reservation_web_v_us):
        """Sets the reservation_web_v_us of this ReservationDefinition.

        The number of Web Virtual Users to be reserved.  # noqa: E501

        :param reservation_web_v_us: The reservation_web_v_us of this ReservationDefinition.  # noqa: E501
        :type: float
        """

        self._reservation_web_v_us = reservation_web_v_us

    @property
    def reservation_sapv_us(self):
        """Gets the reservation_sapv_us of this ReservationDefinition.  # noqa: E501

        The number of SAP Virtual Users to be reserved.  # noqa: E501

        :return: The reservation_sapv_us of this ReservationDefinition.  # noqa: E501
        :rtype: float
        """
        return self._reservation_sapv_us

    @reservation_sapv_us.setter
    def reservation_sapv_us(self, reservation_sapv_us):
        """Sets the reservation_sapv_us of this ReservationDefinition.

        The number of SAP Virtual Users to be reserved.  # noqa: E501

        :param reservation_sapv_us: The reservation_sapv_us of this ReservationDefinition.  # noqa: E501
        :type: float
        """

        self._reservation_sapv_us = reservation_sapv_us

    @property
    def controller_zone_id(self):
        """Gets the controller_zone_id of this ReservationDefinition.  # noqa: E501

        Name of the zone.  # noqa: E501

        :return: The controller_zone_id of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._controller_zone_id

    @controller_zone_id.setter
    def controller_zone_id(self, controller_zone_id):
        """Sets the controller_zone_id of this ReservationDefinition.

        Name of the zone.  # noqa: E501

        :param controller_zone_id: The controller_zone_id of this ReservationDefinition.  # noqa: E501
        :type: str
        """

        self._controller_zone_id = controller_zone_id

    @property
    def neoload_version(self):
        """Gets the neoload_version of this ReservationDefinition.  # noqa: E501

        Neoload version of the selected controller.  # noqa: E501

        :return: The neoload_version of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._neoload_version

    @neoload_version.setter
    def neoload_version(self, neoload_version):
        """Sets the neoload_version of this ReservationDefinition.

        Neoload version of the selected controller.  # noqa: E501

        :param neoload_version: The neoload_version of this ReservationDefinition.  # noqa: E501
        :type: str
        """

        self._neoload_version = neoload_version

    @property
    def lg_zones_resources_reservation(self):
        """Gets the lg_zones_resources_reservation of this ReservationDefinition.  # noqa: E501


        :return: The lg_zones_resources_reservation of this ReservationDefinition.  # noqa: E501
        :rtype: list[LgByZones]
        """
        return self._lg_zones_resources_reservation

    @lg_zones_resources_reservation.setter
    def lg_zones_resources_reservation(self, lg_zones_resources_reservation):
        """Sets the lg_zones_resources_reservation of this ReservationDefinition.


        :param lg_zones_resources_reservation: The lg_zones_resources_reservation of this ReservationDefinition.  # noqa: E501
        :type: list[LgByZones]
        """

        self._lg_zones_resources_reservation = lg_zones_resources_reservation

    @property
    def author(self):
        """Gets the author of this ReservationDefinition.  # noqa: E501

        Name of the user who created the reservation.  # noqa: E501

        :return: The author of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this ReservationDefinition.

        Name of the user who created the reservation.  # noqa: E501

        :param author: The author of this ReservationDefinition.  # noqa: E501
        :type: str
        """

        self._author = author

    @property
    def owner(self):
        """Gets the owner of this ReservationDefinition.  # noqa: E501


        :return: The owner of this ReservationDefinition.  # noqa: E501
        :rtype: ReservationOwner
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this ReservationDefinition.


        :param owner: The owner of this ReservationDefinition.  # noqa: E501
        :type: ReservationOwner
        """

        self._owner = owner

    @property
    def name(self):
        """Gets the name of this ReservationDefinition.  # noqa: E501

        Title of the reservation.  # noqa: E501

        :return: The name of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ReservationDefinition.

        Title of the reservation.  # noqa: E501

        :param name: The name of this ReservationDefinition.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this ReservationDefinition.  # noqa: E501

        Description of the reservation.  # noqa: E501

        :return: The description of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ReservationDefinition.

        Description of the reservation.  # noqa: E501

        :param description: The description of this ReservationDefinition.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def type(self):
        """Gets the type of this ReservationDefinition.  # noqa: E501

        How the reservation has been created. By a user or automatically when a test started.  # noqa: E501

        :return: The type of this ReservationDefinition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ReservationDefinition.

        How the reservation has been created. By a user or automatically when a test started.  # noqa: E501

        :param type: The type of this ReservationDefinition.  # noqa: E501
        :type: str
        """
        allowed_values = ["SCHEDULED", "AUTO_RESERVATION"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if not isinstance(other, ReservationDefinition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReservationDefinition):
            return True

        return self.to_dict() != other.to_dict()
