# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.5.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class AllowableValue(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'value': 'str',
        'display_name': 'str',
        'description': 'str'
    }

    attribute_map = {
        'value': 'value',
        'display_name': 'displayName',
        'description': 'description'
    }

    def __init__(self, value=None, display_name=None, description=None):
        """
        AllowableValue - a model defined in Swagger
        """

        self._value = None
        self._display_name = None
        self._description = None

        if value is not None:
          self.value = value
        if display_name is not None:
          self.display_name = display_name
        if description is not None:
          self.description = description

    @property
    def value(self):
        """
        Gets the value of this AllowableValue.
        The value of the allowable value

        :return: The value of this AllowableValue.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AllowableValue.
        The value of the allowable value

        :param value: The value of this AllowableValue.
        :type: str
        """

        self._value = value

    @property
    def display_name(self):
        """
        Gets the display_name of this AllowableValue.
        The display name of the allowable value

        :return: The display_name of this AllowableValue.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this AllowableValue.
        The display name of the allowable value

        :param display_name: The display_name of this AllowableValue.
        :type: str
        """

        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this AllowableValue.
        The description of the allowable value

        :return: The description of this AllowableValue.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AllowableValue.
        The description of the allowable value

        :param description: The description of this AllowableValue.
        :type: str
        """

        self._description = description

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, AllowableValue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
