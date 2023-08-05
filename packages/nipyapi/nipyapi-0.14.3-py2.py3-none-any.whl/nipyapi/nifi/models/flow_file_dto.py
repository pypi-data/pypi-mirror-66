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


class FlowFileDTO(object):
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
        'uri': 'str',
        'uuid': 'str',
        'filename': 'str',
        'position': 'int',
        'size': 'int',
        'queued_duration': 'int',
        'lineage_duration': 'int',
        'penalty_expires_in': 'int',
        'cluster_node_id': 'str',
        'cluster_node_address': 'str',
        'attributes': 'dict(str, str)',
        'content_claim_section': 'str',
        'content_claim_container': 'str',
        'content_claim_identifier': 'str',
        'content_claim_offset': 'int',
        'content_claim_file_size': 'str',
        'content_claim_file_size_bytes': 'int',
        'penalized': 'bool'
    }

    attribute_map = {
        'uri': 'uri',
        'uuid': 'uuid',
        'filename': 'filename',
        'position': 'position',
        'size': 'size',
        'queued_duration': 'queuedDuration',
        'lineage_duration': 'lineageDuration',
        'penalty_expires_in': 'penaltyExpiresIn',
        'cluster_node_id': 'clusterNodeId',
        'cluster_node_address': 'clusterNodeAddress',
        'attributes': 'attributes',
        'content_claim_section': 'contentClaimSection',
        'content_claim_container': 'contentClaimContainer',
        'content_claim_identifier': 'contentClaimIdentifier',
        'content_claim_offset': 'contentClaimOffset',
        'content_claim_file_size': 'contentClaimFileSize',
        'content_claim_file_size_bytes': 'contentClaimFileSizeBytes',
        'penalized': 'penalized'
    }

    def __init__(self, uri=None, uuid=None, filename=None, position=None, size=None, queued_duration=None, lineage_duration=None, penalty_expires_in=None, cluster_node_id=None, cluster_node_address=None, attributes=None, content_claim_section=None, content_claim_container=None, content_claim_identifier=None, content_claim_offset=None, content_claim_file_size=None, content_claim_file_size_bytes=None, penalized=None):
        """
        FlowFileDTO - a model defined in Swagger
        """

        self._uri = None
        self._uuid = None
        self._filename = None
        self._position = None
        self._size = None
        self._queued_duration = None
        self._lineage_duration = None
        self._penalty_expires_in = None
        self._cluster_node_id = None
        self._cluster_node_address = None
        self._attributes = None
        self._content_claim_section = None
        self._content_claim_container = None
        self._content_claim_identifier = None
        self._content_claim_offset = None
        self._content_claim_file_size = None
        self._content_claim_file_size_bytes = None
        self._penalized = None

        if uri is not None:
          self.uri = uri
        if uuid is not None:
          self.uuid = uuid
        if filename is not None:
          self.filename = filename
        if position is not None:
          self.position = position
        if size is not None:
          self.size = size
        if queued_duration is not None:
          self.queued_duration = queued_duration
        if lineage_duration is not None:
          self.lineage_duration = lineage_duration
        if penalty_expires_in is not None:
          self.penalty_expires_in = penalty_expires_in
        if cluster_node_id is not None:
          self.cluster_node_id = cluster_node_id
        if cluster_node_address is not None:
          self.cluster_node_address = cluster_node_address
        if attributes is not None:
          self.attributes = attributes
        if content_claim_section is not None:
          self.content_claim_section = content_claim_section
        if content_claim_container is not None:
          self.content_claim_container = content_claim_container
        if content_claim_identifier is not None:
          self.content_claim_identifier = content_claim_identifier
        if content_claim_offset is not None:
          self.content_claim_offset = content_claim_offset
        if content_claim_file_size is not None:
          self.content_claim_file_size = content_claim_file_size
        if content_claim_file_size_bytes is not None:
          self.content_claim_file_size_bytes = content_claim_file_size_bytes
        if penalized is not None:
          self.penalized = penalized

    @property
    def uri(self):
        """
        Gets the uri of this FlowFileDTO.
        The URI that can be used to access this FlowFile.

        :return: The uri of this FlowFileDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this FlowFileDTO.
        The URI that can be used to access this FlowFile.

        :param uri: The uri of this FlowFileDTO.
        :type: str
        """

        self._uri = uri

    @property
    def uuid(self):
        """
        Gets the uuid of this FlowFileDTO.
        The FlowFile UUID.

        :return: The uuid of this FlowFileDTO.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """
        Sets the uuid of this FlowFileDTO.
        The FlowFile UUID.

        :param uuid: The uuid of this FlowFileDTO.
        :type: str
        """

        self._uuid = uuid

    @property
    def filename(self):
        """
        Gets the filename of this FlowFileDTO.
        The FlowFile filename.

        :return: The filename of this FlowFileDTO.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """
        Sets the filename of this FlowFileDTO.
        The FlowFile filename.

        :param filename: The filename of this FlowFileDTO.
        :type: str
        """

        self._filename = filename

    @property
    def position(self):
        """
        Gets the position of this FlowFileDTO.
        The FlowFile's position in the queue.

        :return: The position of this FlowFileDTO.
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this FlowFileDTO.
        The FlowFile's position in the queue.

        :param position: The position of this FlowFileDTO.
        :type: int
        """

        self._position = position

    @property
    def size(self):
        """
        Gets the size of this FlowFileDTO.
        The FlowFile file size.

        :return: The size of this FlowFileDTO.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this FlowFileDTO.
        The FlowFile file size.

        :param size: The size of this FlowFileDTO.
        :type: int
        """

        self._size = size

    @property
    def queued_duration(self):
        """
        Gets the queued_duration of this FlowFileDTO.
        How long this FlowFile has been enqueued.

        :return: The queued_duration of this FlowFileDTO.
        :rtype: int
        """
        return self._queued_duration

    @queued_duration.setter
    def queued_duration(self, queued_duration):
        """
        Sets the queued_duration of this FlowFileDTO.
        How long this FlowFile has been enqueued.

        :param queued_duration: The queued_duration of this FlowFileDTO.
        :type: int
        """

        self._queued_duration = queued_duration

    @property
    def lineage_duration(self):
        """
        Gets the lineage_duration of this FlowFileDTO.
        Duration since the FlowFile's greatest ancestor entered the flow.

        :return: The lineage_duration of this FlowFileDTO.
        :rtype: int
        """
        return self._lineage_duration

    @lineage_duration.setter
    def lineage_duration(self, lineage_duration):
        """
        Sets the lineage_duration of this FlowFileDTO.
        Duration since the FlowFile's greatest ancestor entered the flow.

        :param lineage_duration: The lineage_duration of this FlowFileDTO.
        :type: int
        """

        self._lineage_duration = lineage_duration

    @property
    def penalty_expires_in(self):
        """
        Gets the penalty_expires_in of this FlowFileDTO.
        How long in milliseconds until the FlowFile penalty expires.

        :return: The penalty_expires_in of this FlowFileDTO.
        :rtype: int
        """
        return self._penalty_expires_in

    @penalty_expires_in.setter
    def penalty_expires_in(self, penalty_expires_in):
        """
        Sets the penalty_expires_in of this FlowFileDTO.
        How long in milliseconds until the FlowFile penalty expires.

        :param penalty_expires_in: The penalty_expires_in of this FlowFileDTO.
        :type: int
        """

        self._penalty_expires_in = penalty_expires_in

    @property
    def cluster_node_id(self):
        """
        Gets the cluster_node_id of this FlowFileDTO.
        The id of the node where this FlowFile resides.

        :return: The cluster_node_id of this FlowFileDTO.
        :rtype: str
        """
        return self._cluster_node_id

    @cluster_node_id.setter
    def cluster_node_id(self, cluster_node_id):
        """
        Sets the cluster_node_id of this FlowFileDTO.
        The id of the node where this FlowFile resides.

        :param cluster_node_id: The cluster_node_id of this FlowFileDTO.
        :type: str
        """

        self._cluster_node_id = cluster_node_id

    @property
    def cluster_node_address(self):
        """
        Gets the cluster_node_address of this FlowFileDTO.
        The label for the node where this FlowFile resides.

        :return: The cluster_node_address of this FlowFileDTO.
        :rtype: str
        """
        return self._cluster_node_address

    @cluster_node_address.setter
    def cluster_node_address(self, cluster_node_address):
        """
        Sets the cluster_node_address of this FlowFileDTO.
        The label for the node where this FlowFile resides.

        :param cluster_node_address: The cluster_node_address of this FlowFileDTO.
        :type: str
        """

        self._cluster_node_address = cluster_node_address

    @property
    def attributes(self):
        """
        Gets the attributes of this FlowFileDTO.
        The FlowFile attributes.

        :return: The attributes of this FlowFileDTO.
        :rtype: dict(str, str)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this FlowFileDTO.
        The FlowFile attributes.

        :param attributes: The attributes of this FlowFileDTO.
        :type: dict(str, str)
        """

        self._attributes = attributes

    @property
    def content_claim_section(self):
        """
        Gets the content_claim_section of this FlowFileDTO.
        The section in which the content claim lives.

        :return: The content_claim_section of this FlowFileDTO.
        :rtype: str
        """
        return self._content_claim_section

    @content_claim_section.setter
    def content_claim_section(self, content_claim_section):
        """
        Sets the content_claim_section of this FlowFileDTO.
        The section in which the content claim lives.

        :param content_claim_section: The content_claim_section of this FlowFileDTO.
        :type: str
        """

        self._content_claim_section = content_claim_section

    @property
    def content_claim_container(self):
        """
        Gets the content_claim_container of this FlowFileDTO.
        The container in which the content claim lives.

        :return: The content_claim_container of this FlowFileDTO.
        :rtype: str
        """
        return self._content_claim_container

    @content_claim_container.setter
    def content_claim_container(self, content_claim_container):
        """
        Sets the content_claim_container of this FlowFileDTO.
        The container in which the content claim lives.

        :param content_claim_container: The content_claim_container of this FlowFileDTO.
        :type: str
        """

        self._content_claim_container = content_claim_container

    @property
    def content_claim_identifier(self):
        """
        Gets the content_claim_identifier of this FlowFileDTO.
        The identifier of the content claim.

        :return: The content_claim_identifier of this FlowFileDTO.
        :rtype: str
        """
        return self._content_claim_identifier

    @content_claim_identifier.setter
    def content_claim_identifier(self, content_claim_identifier):
        """
        Sets the content_claim_identifier of this FlowFileDTO.
        The identifier of the content claim.

        :param content_claim_identifier: The content_claim_identifier of this FlowFileDTO.
        :type: str
        """

        self._content_claim_identifier = content_claim_identifier

    @property
    def content_claim_offset(self):
        """
        Gets the content_claim_offset of this FlowFileDTO.
        The offset into the content claim where the flowfile's content begins.

        :return: The content_claim_offset of this FlowFileDTO.
        :rtype: int
        """
        return self._content_claim_offset

    @content_claim_offset.setter
    def content_claim_offset(self, content_claim_offset):
        """
        Sets the content_claim_offset of this FlowFileDTO.
        The offset into the content claim where the flowfile's content begins.

        :param content_claim_offset: The content_claim_offset of this FlowFileDTO.
        :type: int
        """

        self._content_claim_offset = content_claim_offset

    @property
    def content_claim_file_size(self):
        """
        Gets the content_claim_file_size of this FlowFileDTO.
        The file size of the content claim formatted.

        :return: The content_claim_file_size of this FlowFileDTO.
        :rtype: str
        """
        return self._content_claim_file_size

    @content_claim_file_size.setter
    def content_claim_file_size(self, content_claim_file_size):
        """
        Sets the content_claim_file_size of this FlowFileDTO.
        The file size of the content claim formatted.

        :param content_claim_file_size: The content_claim_file_size of this FlowFileDTO.
        :type: str
        """

        self._content_claim_file_size = content_claim_file_size

    @property
    def content_claim_file_size_bytes(self):
        """
        Gets the content_claim_file_size_bytes of this FlowFileDTO.
        The file size of the content claim in bytes.

        :return: The content_claim_file_size_bytes of this FlowFileDTO.
        :rtype: int
        """
        return self._content_claim_file_size_bytes

    @content_claim_file_size_bytes.setter
    def content_claim_file_size_bytes(self, content_claim_file_size_bytes):
        """
        Sets the content_claim_file_size_bytes of this FlowFileDTO.
        The file size of the content claim in bytes.

        :param content_claim_file_size_bytes: The content_claim_file_size_bytes of this FlowFileDTO.
        :type: int
        """

        self._content_claim_file_size_bytes = content_claim_file_size_bytes

    @property
    def penalized(self):
        """
        Gets the penalized of this FlowFileDTO.
        If the FlowFile is penalized.

        :return: The penalized of this FlowFileDTO.
        :rtype: bool
        """
        return self._penalized

    @penalized.setter
    def penalized(self, penalized):
        """
        Sets the penalized of this FlowFileDTO.
        If the FlowFile is penalized.

        :param penalized: The penalized of this FlowFileDTO.
        :type: bool
        """

        self._penalized = penalized

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
        if not isinstance(other, FlowFileDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
