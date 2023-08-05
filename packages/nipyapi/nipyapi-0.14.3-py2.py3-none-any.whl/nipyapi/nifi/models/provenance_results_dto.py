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


class ProvenanceResultsDTO(object):
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
        'provenance_events': 'list[ProvenanceEventDTO]',
        'total': 'str',
        'total_count': 'int',
        'generated': 'str',
        'oldest_event': 'str',
        'time_offset': 'int',
        'errors': 'list[str]'
    }

    attribute_map = {
        'provenance_events': 'provenanceEvents',
        'total': 'total',
        'total_count': 'totalCount',
        'generated': 'generated',
        'oldest_event': 'oldestEvent',
        'time_offset': 'timeOffset',
        'errors': 'errors'
    }

    def __init__(self, provenance_events=None, total=None, total_count=None, generated=None, oldest_event=None, time_offset=None, errors=None):
        """
        ProvenanceResultsDTO - a model defined in Swagger
        """

        self._provenance_events = None
        self._total = None
        self._total_count = None
        self._generated = None
        self._oldest_event = None
        self._time_offset = None
        self._errors = None

        if provenance_events is not None:
          self.provenance_events = provenance_events
        if total is not None:
          self.total = total
        if total_count is not None:
          self.total_count = total_count
        if generated is not None:
          self.generated = generated
        if oldest_event is not None:
          self.oldest_event = oldest_event
        if time_offset is not None:
          self.time_offset = time_offset
        if errors is not None:
          self.errors = errors

    @property
    def provenance_events(self):
        """
        Gets the provenance_events of this ProvenanceResultsDTO.
        The provenance events that matched the search criteria.

        :return: The provenance_events of this ProvenanceResultsDTO.
        :rtype: list[ProvenanceEventDTO]
        """
        return self._provenance_events

    @provenance_events.setter
    def provenance_events(self, provenance_events):
        """
        Sets the provenance_events of this ProvenanceResultsDTO.
        The provenance events that matched the search criteria.

        :param provenance_events: The provenance_events of this ProvenanceResultsDTO.
        :type: list[ProvenanceEventDTO]
        """

        self._provenance_events = provenance_events

    @property
    def total(self):
        """
        Gets the total of this ProvenanceResultsDTO.
        The total number of results formatted.

        :return: The total of this ProvenanceResultsDTO.
        :rtype: str
        """
        return self._total

    @total.setter
    def total(self, total):
        """
        Sets the total of this ProvenanceResultsDTO.
        The total number of results formatted.

        :param total: The total of this ProvenanceResultsDTO.
        :type: str
        """

        self._total = total

    @property
    def total_count(self):
        """
        Gets the total_count of this ProvenanceResultsDTO.
        The total number of results.

        :return: The total_count of this ProvenanceResultsDTO.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """
        Sets the total_count of this ProvenanceResultsDTO.
        The total number of results.

        :param total_count: The total_count of this ProvenanceResultsDTO.
        :type: int
        """

        self._total_count = total_count

    @property
    def generated(self):
        """
        Gets the generated of this ProvenanceResultsDTO.
        Then the search was performed.

        :return: The generated of this ProvenanceResultsDTO.
        :rtype: str
        """
        return self._generated

    @generated.setter
    def generated(self, generated):
        """
        Sets the generated of this ProvenanceResultsDTO.
        Then the search was performed.

        :param generated: The generated of this ProvenanceResultsDTO.
        :type: str
        """

        self._generated = generated

    @property
    def oldest_event(self):
        """
        Gets the oldest_event of this ProvenanceResultsDTO.
        The oldest event available in the provenance repository.

        :return: The oldest_event of this ProvenanceResultsDTO.
        :rtype: str
        """
        return self._oldest_event

    @oldest_event.setter
    def oldest_event(self, oldest_event):
        """
        Sets the oldest_event of this ProvenanceResultsDTO.
        The oldest event available in the provenance repository.

        :param oldest_event: The oldest_event of this ProvenanceResultsDTO.
        :type: str
        """

        self._oldest_event = oldest_event

    @property
    def time_offset(self):
        """
        Gets the time_offset of this ProvenanceResultsDTO.
        The time offset of the server that's used for event time.

        :return: The time_offset of this ProvenanceResultsDTO.
        :rtype: int
        """
        return self._time_offset

    @time_offset.setter
    def time_offset(self, time_offset):
        """
        Sets the time_offset of this ProvenanceResultsDTO.
        The time offset of the server that's used for event time.

        :param time_offset: The time_offset of this ProvenanceResultsDTO.
        :type: int
        """

        self._time_offset = time_offset

    @property
    def errors(self):
        """
        Gets the errors of this ProvenanceResultsDTO.
        Any errors that occurred while performing the provenance request.

        :return: The errors of this ProvenanceResultsDTO.
        :rtype: list[str]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """
        Sets the errors of this ProvenanceResultsDTO.
        Any errors that occurred while performing the provenance request.

        :param errors: The errors of this ProvenanceResultsDTO.
        :type: list[str]
        """

        self._errors = errors

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
        if not isinstance(other, ProvenanceResultsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
