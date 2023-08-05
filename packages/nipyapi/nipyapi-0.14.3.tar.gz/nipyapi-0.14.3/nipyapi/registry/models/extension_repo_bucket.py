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


class ExtensionRepoBucket(object):
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
        'link': 'JaxbLink',
        'bucket_name': 'str'
    }

    attribute_map = {
        'link': 'link',
        'bucket_name': 'bucketName'
    }

    def __init__(self, link=None, bucket_name=None):
        """
        ExtensionRepoBucket - a model defined in Swagger
        """

        self._link = None
        self._bucket_name = None

        if link is not None:
          self.link = link
        if bucket_name is not None:
          self.bucket_name = bucket_name

    @property
    def link(self):
        """
        Gets the link of this ExtensionRepoBucket.
        An WebLink to this entity.

        :return: The link of this ExtensionRepoBucket.
        :rtype: JaxbLink
        """
        return self._link

    @link.setter
    def link(self, link):
        """
        Sets the link of this ExtensionRepoBucket.
        An WebLink to this entity.

        :param link: The link of this ExtensionRepoBucket.
        :type: JaxbLink
        """

        self._link = link

    @property
    def bucket_name(self):
        """
        Gets the bucket_name of this ExtensionRepoBucket.
        The name of the bucket

        :return: The bucket_name of this ExtensionRepoBucket.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this ExtensionRepoBucket.
        The name of the bucket

        :param bucket_name: The bucket_name of this ExtensionRepoBucket.
        :type: str
        """

        self._bucket_name = bucket_name

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
        if not isinstance(other, ExtensionRepoBucket):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
