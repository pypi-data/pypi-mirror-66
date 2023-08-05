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


class SnippetDTO(object):
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
        'id': 'str',
        'uri': 'str',
        'parent_group_id': 'str',
        'process_groups': 'dict(str, RevisionDTO)',
        'remote_process_groups': 'dict(str, RevisionDTO)',
        'processors': 'dict(str, RevisionDTO)',
        'input_ports': 'dict(str, RevisionDTO)',
        'output_ports': 'dict(str, RevisionDTO)',
        'connections': 'dict(str, RevisionDTO)',
        'labels': 'dict(str, RevisionDTO)',
        'funnels': 'dict(str, RevisionDTO)'
    }

    attribute_map = {
        'id': 'id',
        'uri': 'uri',
        'parent_group_id': 'parentGroupId',
        'process_groups': 'processGroups',
        'remote_process_groups': 'remoteProcessGroups',
        'processors': 'processors',
        'input_ports': 'inputPorts',
        'output_ports': 'outputPorts',
        'connections': 'connections',
        'labels': 'labels',
        'funnels': 'funnels'
    }

    def __init__(self, id=None, uri=None, parent_group_id=None, process_groups=None, remote_process_groups=None, processors=None, input_ports=None, output_ports=None, connections=None, labels=None, funnels=None):
        """
        SnippetDTO - a model defined in Swagger
        """

        self._id = None
        self._uri = None
        self._parent_group_id = None
        self._process_groups = None
        self._remote_process_groups = None
        self._processors = None
        self._input_ports = None
        self._output_ports = None
        self._connections = None
        self._labels = None
        self._funnels = None

        if id is not None:
          self.id = id
        if uri is not None:
          self.uri = uri
        if parent_group_id is not None:
          self.parent_group_id = parent_group_id
        if process_groups is not None:
          self.process_groups = process_groups
        if remote_process_groups is not None:
          self.remote_process_groups = remote_process_groups
        if processors is not None:
          self.processors = processors
        if input_ports is not None:
          self.input_ports = input_ports
        if output_ports is not None:
          self.output_ports = output_ports
        if connections is not None:
          self.connections = connections
        if labels is not None:
          self.labels = labels
        if funnels is not None:
          self.funnels = funnels

    @property
    def id(self):
        """
        Gets the id of this SnippetDTO.
        The id of the snippet.

        :return: The id of this SnippetDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SnippetDTO.
        The id of the snippet.

        :param id: The id of this SnippetDTO.
        :type: str
        """

        self._id = id

    @property
    def uri(self):
        """
        Gets the uri of this SnippetDTO.
        The URI of the snippet.

        :return: The uri of this SnippetDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this SnippetDTO.
        The URI of the snippet.

        :param uri: The uri of this SnippetDTO.
        :type: str
        """

        self._uri = uri

    @property
    def parent_group_id(self):
        """
        Gets the parent_group_id of this SnippetDTO.
        The group id for the components in the snippet.

        :return: The parent_group_id of this SnippetDTO.
        :rtype: str
        """
        return self._parent_group_id

    @parent_group_id.setter
    def parent_group_id(self, parent_group_id):
        """
        Sets the parent_group_id of this SnippetDTO.
        The group id for the components in the snippet.

        :param parent_group_id: The parent_group_id of this SnippetDTO.
        :type: str
        """

        self._parent_group_id = parent_group_id

    @property
    def process_groups(self):
        """
        Gets the process_groups of this SnippetDTO.
        The ids of the process groups in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The process_groups of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._process_groups

    @process_groups.setter
    def process_groups(self, process_groups):
        """
        Sets the process_groups of this SnippetDTO.
        The ids of the process groups in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param process_groups: The process_groups of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._process_groups = process_groups

    @property
    def remote_process_groups(self):
        """
        Gets the remote_process_groups of this SnippetDTO.
        The ids of the remote process groups in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The remote_process_groups of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._remote_process_groups

    @remote_process_groups.setter
    def remote_process_groups(self, remote_process_groups):
        """
        Sets the remote_process_groups of this SnippetDTO.
        The ids of the remote process groups in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param remote_process_groups: The remote_process_groups of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._remote_process_groups = remote_process_groups

    @property
    def processors(self):
        """
        Gets the processors of this SnippetDTO.
        The ids of the processors in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The processors of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._processors

    @processors.setter
    def processors(self, processors):
        """
        Sets the processors of this SnippetDTO.
        The ids of the processors in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param processors: The processors of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._processors = processors

    @property
    def input_ports(self):
        """
        Gets the input_ports of this SnippetDTO.
        The ids of the input ports in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The input_ports of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._input_ports

    @input_ports.setter
    def input_ports(self, input_ports):
        """
        Sets the input_ports of this SnippetDTO.
        The ids of the input ports in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param input_ports: The input_ports of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._input_ports = input_ports

    @property
    def output_ports(self):
        """
        Gets the output_ports of this SnippetDTO.
        The ids of the output ports in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The output_ports of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._output_ports

    @output_ports.setter
    def output_ports(self, output_ports):
        """
        Sets the output_ports of this SnippetDTO.
        The ids of the output ports in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param output_ports: The output_ports of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._output_ports = output_ports

    @property
    def connections(self):
        """
        Gets the connections of this SnippetDTO.
        The ids of the connections in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The connections of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """
        Sets the connections of this SnippetDTO.
        The ids of the connections in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param connections: The connections of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._connections = connections

    @property
    def labels(self):
        """
        Gets the labels of this SnippetDTO.
        The ids of the labels in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The labels of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the labels of this SnippetDTO.
        The ids of the labels in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param labels: The labels of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._labels = labels

    @property
    def funnels(self):
        """
        Gets the funnels of this SnippetDTO.
        The ids of the funnels in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :return: The funnels of this SnippetDTO.
        :rtype: dict(str, RevisionDTO)
        """
        return self._funnels

    @funnels.setter
    def funnels(self, funnels):
        """
        Sets the funnels of this SnippetDTO.
        The ids of the funnels in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests).

        :param funnels: The funnels of this SnippetDTO.
        :type: dict(str, RevisionDTO)
        """

        self._funnels = funnels

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
        if not isinstance(other, SnippetDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
