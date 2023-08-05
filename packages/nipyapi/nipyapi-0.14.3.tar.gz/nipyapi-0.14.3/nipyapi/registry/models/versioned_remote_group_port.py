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


class VersionedRemoteGroupPort(object):
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
        'identifier': 'str',
        'name': 'str',
        'comments': 'str',
        'position': 'Position',
        'remote_group_id': 'str',
        'concurrently_schedulable_task_count': 'int',
        'use_compression': 'bool',
        'batch_size': 'BatchSize',
        'component_type': 'str',
        'target_id': 'str',
        'scheduled_state': 'str',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'remote_group_id': 'remoteGroupId',
        'concurrently_schedulable_task_count': 'concurrentlySchedulableTaskCount',
        'use_compression': 'useCompression',
        'batch_size': 'batchSize',
        'component_type': 'componentType',
        'target_id': 'targetId',
        'scheduled_state': 'scheduledState',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, name=None, comments=None, position=None, remote_group_id=None, concurrently_schedulable_task_count=None, use_compression=None, batch_size=None, component_type=None, target_id=None, scheduled_state=None, group_identifier=None):
        """
        VersionedRemoteGroupPort - a model defined in Swagger
        """

        self._identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._remote_group_id = None
        self._concurrently_schedulable_task_count = None
        self._use_compression = None
        self._batch_size = None
        self._component_type = None
        self._target_id = None
        self._scheduled_state = None
        self._group_identifier = None

        if identifier is not None:
          self.identifier = identifier
        if name is not None:
          self.name = name
        if comments is not None:
          self.comments = comments
        if position is not None:
          self.position = position
        if remote_group_id is not None:
          self.remote_group_id = remote_group_id
        if concurrently_schedulable_task_count is not None:
          self.concurrently_schedulable_task_count = concurrently_schedulable_task_count
        if use_compression is not None:
          self.use_compression = use_compression
        if batch_size is not None:
          self.batch_size = batch_size
        if component_type is not None:
          self.component_type = component_type
        if target_id is not None:
          self.target_id = target_id
        if scheduled_state is not None:
          self.scheduled_state = scheduled_state
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedRemoteGroupPort.
        The component's unique identifier

        :return: The identifier of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedRemoteGroupPort.
        The component's unique identifier

        :param identifier: The identifier of this VersionedRemoteGroupPort.
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedRemoteGroupPort.
        The component's name

        :return: The name of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedRemoteGroupPort.
        The component's name

        :param name: The name of this VersionedRemoteGroupPort.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedRemoteGroupPort.
        The user-supplied comments for the component

        :return: The comments of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedRemoteGroupPort.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedRemoteGroupPort.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedRemoteGroupPort.
        The component's position on the graph

        :return: The position of this VersionedRemoteGroupPort.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedRemoteGroupPort.
        The component's position on the graph

        :param position: The position of this VersionedRemoteGroupPort.
        :type: Position
        """

        self._position = position

    @property
    def remote_group_id(self):
        """
        Gets the remote_group_id of this VersionedRemoteGroupPort.
        The id of the remote process group that the port resides in.

        :return: The remote_group_id of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._remote_group_id

    @remote_group_id.setter
    def remote_group_id(self, remote_group_id):
        """
        Sets the remote_group_id of this VersionedRemoteGroupPort.
        The id of the remote process group that the port resides in.

        :param remote_group_id: The remote_group_id of this VersionedRemoteGroupPort.
        :type: str
        """

        self._remote_group_id = remote_group_id

    @property
    def concurrently_schedulable_task_count(self):
        """
        Gets the concurrently_schedulable_task_count of this VersionedRemoteGroupPort.
        The number of task that may transmit flowfiles to the target port concurrently.

        :return: The concurrently_schedulable_task_count of this VersionedRemoteGroupPort.
        :rtype: int
        """
        return self._concurrently_schedulable_task_count

    @concurrently_schedulable_task_count.setter
    def concurrently_schedulable_task_count(self, concurrently_schedulable_task_count):
        """
        Sets the concurrently_schedulable_task_count of this VersionedRemoteGroupPort.
        The number of task that may transmit flowfiles to the target port concurrently.

        :param concurrently_schedulable_task_count: The concurrently_schedulable_task_count of this VersionedRemoteGroupPort.
        :type: int
        """

        self._concurrently_schedulable_task_count = concurrently_schedulable_task_count

    @property
    def use_compression(self):
        """
        Gets the use_compression of this VersionedRemoteGroupPort.
        Whether the flowfiles are compressed when sent to the target port.

        :return: The use_compression of this VersionedRemoteGroupPort.
        :rtype: bool
        """
        return self._use_compression

    @use_compression.setter
    def use_compression(self, use_compression):
        """
        Sets the use_compression of this VersionedRemoteGroupPort.
        Whether the flowfiles are compressed when sent to the target port.

        :param use_compression: The use_compression of this VersionedRemoteGroupPort.
        :type: bool
        """

        self._use_compression = use_compression

    @property
    def batch_size(self):
        """
        Gets the batch_size of this VersionedRemoteGroupPort.
        The batch settings for data transmission.

        :return: The batch_size of this VersionedRemoteGroupPort.
        :rtype: BatchSize
        """
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size):
        """
        Sets the batch_size of this VersionedRemoteGroupPort.
        The batch settings for data transmission.

        :param batch_size: The batch_size of this VersionedRemoteGroupPort.
        :type: BatchSize
        """

        self._batch_size = batch_size

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedRemoteGroupPort.

        :return: The component_type of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedRemoteGroupPort.

        :param component_type: The component_type of this VersionedRemoteGroupPort.
        :type: str
        """
        allowed_values = ["CONNECTION", "PROCESSOR", "PROCESS_GROUP", "REMOTE_PROCESS_GROUP", "INPUT_PORT", "OUTPUT_PORT", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "FUNNEL", "LABEL", "CONTROLLER_SERVICE"]
        if component_type not in allowed_values:
            raise ValueError(
                "Invalid value for `component_type` ({0}), must be one of {1}"
                .format(component_type, allowed_values)
            )

        self._component_type = component_type

    @property
    def target_id(self):
        """
        Gets the target_id of this VersionedRemoteGroupPort.
        The ID of the port on the target NiFi instance

        :return: The target_id of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this VersionedRemoteGroupPort.
        The ID of the port on the target NiFi instance

        :param target_id: The target_id of this VersionedRemoteGroupPort.
        :type: str
        """

        self._target_id = target_id

    @property
    def scheduled_state(self):
        """
        Gets the scheduled_state of this VersionedRemoteGroupPort.
        The scheduled state of the component

        :return: The scheduled_state of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._scheduled_state

    @scheduled_state.setter
    def scheduled_state(self, scheduled_state):
        """
        Sets the scheduled_state of this VersionedRemoteGroupPort.
        The scheduled state of the component

        :param scheduled_state: The scheduled_state of this VersionedRemoteGroupPort.
        :type: str
        """
        allowed_values = ["ENABLED", "DISABLED"]
        if scheduled_state not in allowed_values:
            raise ValueError(
                "Invalid value for `scheduled_state` ({0}), must be one of {1}"
                .format(scheduled_state, allowed_values)
            )

        self._scheduled_state = scheduled_state

    @property
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedRemoteGroupPort.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedRemoteGroupPort.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedRemoteGroupPort.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedRemoteGroupPort.
        :type: str
        """

        self._group_identifier = group_identifier

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
        if not isinstance(other, VersionedRemoteGroupPort):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
