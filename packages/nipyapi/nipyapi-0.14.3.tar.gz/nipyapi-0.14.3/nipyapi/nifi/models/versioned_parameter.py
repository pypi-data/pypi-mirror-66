# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.11.1-SNAPSHOT
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedParameter(object):
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
        'name': 'str',
        'description': 'str',
        'sensitive': 'bool',
        'value': 'str'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'sensitive': 'sensitive',
        'value': 'value'
    }

    def __init__(self, name=None, description=None, sensitive=None, value=None):
        """
        VersionedParameter - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._sensitive = None
        self._value = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if sensitive is not None:
          self.sensitive = sensitive
        if value is not None:
          self.value = value

    @property
    def name(self):
        """
        Gets the name of this VersionedParameter.
        The name of the parameter

        :return: The name of this VersionedParameter.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedParameter.
        The name of the parameter

        :param name: The name of this VersionedParameter.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this VersionedParameter.
        The description of the param

        :return: The description of this VersionedParameter.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this VersionedParameter.
        The description of the param

        :param description: The description of this VersionedParameter.
        :type: str
        """

        self._description = description

    @property
    def sensitive(self):
        """
        Gets the sensitive of this VersionedParameter.
        Whether or not the parameter value is sensitive

        :return: The sensitive of this VersionedParameter.
        :rtype: bool
        """
        return self._sensitive

    @sensitive.setter
    def sensitive(self, sensitive):
        """
        Sets the sensitive of this VersionedParameter.
        Whether or not the parameter value is sensitive

        :param sensitive: The sensitive of this VersionedParameter.
        :type: bool
        """

        self._sensitive = sensitive

    @property
    def value(self):
        """
        Gets the value of this VersionedParameter.
        The value of the parameter

        :return: The value of this VersionedParameter.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this VersionedParameter.
        The value of the parameter

        :param value: The value of this VersionedParameter.
        :type: str
        """

        self._value = value

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
        if not isinstance(other, VersionedParameter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
