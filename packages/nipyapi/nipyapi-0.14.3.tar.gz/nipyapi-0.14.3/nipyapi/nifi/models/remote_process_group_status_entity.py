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


class RemoteProcessGroupStatusEntity(object):
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
        'remote_process_group_status': 'RemoteProcessGroupStatusDTO',
        'can_read': 'bool'
    }

    attribute_map = {
        'remote_process_group_status': 'remoteProcessGroupStatus',
        'can_read': 'canRead'
    }

    def __init__(self, remote_process_group_status=None, can_read=None):
        """
        RemoteProcessGroupStatusEntity - a model defined in Swagger
        """

        self._remote_process_group_status = None
        self._can_read = None

        if remote_process_group_status is not None:
          self.remote_process_group_status = remote_process_group_status
        if can_read is not None:
          self.can_read = can_read

    @property
    def remote_process_group_status(self):
        """
        Gets the remote_process_group_status of this RemoteProcessGroupStatusEntity.

        :return: The remote_process_group_status of this RemoteProcessGroupStatusEntity.
        :rtype: RemoteProcessGroupStatusDTO
        """
        return self._remote_process_group_status

    @remote_process_group_status.setter
    def remote_process_group_status(self, remote_process_group_status):
        """
        Sets the remote_process_group_status of this RemoteProcessGroupStatusEntity.

        :param remote_process_group_status: The remote_process_group_status of this RemoteProcessGroupStatusEntity.
        :type: RemoteProcessGroupStatusDTO
        """

        self._remote_process_group_status = remote_process_group_status

    @property
    def can_read(self):
        """
        Gets the can_read of this RemoteProcessGroupStatusEntity.
        Indicates whether the user can read a given resource.

        :return: The can_read of this RemoteProcessGroupStatusEntity.
        :rtype: bool
        """
        return self._can_read

    @can_read.setter
    def can_read(self, can_read):
        """
        Sets the can_read of this RemoteProcessGroupStatusEntity.
        Indicates whether the user can read a given resource.

        :param can_read: The can_read of this RemoteProcessGroupStatusEntity.
        :type: bool
        """

        self._can_read = can_read

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
        if not isinstance(other, RemoteProcessGroupStatusEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
