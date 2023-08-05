#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

    Polyaxon SDKs and REST API specification.  # noqa: E501

    The version of the OpenAPI document: 1.0.79
    Contact: contact@polyaxon.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from polyaxon_sdk.configuration import Configuration


class V1StatusCondition(object):
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
        "type": "V1Statuses",
        "status": "str",
        "reason": "str",
        "message": "str",
        "last_update_time": "datetime",
        "last_transition_time": "datetime",
    }

    attribute_map = {
        "type": "type",
        "status": "status",
        "reason": "reason",
        "message": "message",
        "last_update_time": "last_update_time",
        "last_transition_time": "last_transition_time",
    }

    def __init__(
        self,
        type=None,
        status=None,
        reason=None,
        message=None,
        last_update_time=None,
        last_transition_time=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """V1StatusCondition - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._status = None
        self._reason = None
        self._message = None
        self._last_update_time = None
        self._last_transition_time = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if status is not None:
            self.status = status
        if reason is not None:
            self.reason = reason
        if message is not None:
            self.message = message
        if last_update_time is not None:
            self.last_update_time = last_update_time
        if last_transition_time is not None:
            self.last_transition_time = last_transition_time

    @property
    def type(self):
        """Gets the type of this V1StatusCondition.  # noqa: E501


        :return: The type of this V1StatusCondition.  # noqa: E501
        :rtype: V1Statuses
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this V1StatusCondition.


        :param type: The type of this V1StatusCondition.  # noqa: E501
        :type: V1Statuses
        """

        self._type = type

    @property
    def status(self):
        """Gets the status of this V1StatusCondition.  # noqa: E501


        :return: The status of this V1StatusCondition.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this V1StatusCondition.


        :param status: The status of this V1StatusCondition.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def reason(self):
        """Gets the reason of this V1StatusCondition.  # noqa: E501


        :return: The reason of this V1StatusCondition.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this V1StatusCondition.


        :param reason: The reason of this V1StatusCondition.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def message(self):
        """Gets the message of this V1StatusCondition.  # noqa: E501


        :return: The message of this V1StatusCondition.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this V1StatusCondition.


        :param message: The message of this V1StatusCondition.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def last_update_time(self):
        """Gets the last_update_time of this V1StatusCondition.  # noqa: E501


        :return: The last_update_time of this V1StatusCondition.  # noqa: E501
        :rtype: datetime
        """
        return self._last_update_time

    @last_update_time.setter
    def last_update_time(self, last_update_time):
        """Sets the last_update_time of this V1StatusCondition.


        :param last_update_time: The last_update_time of this V1StatusCondition.  # noqa: E501
        :type: datetime
        """

        self._last_update_time = last_update_time

    @property
    def last_transition_time(self):
        """Gets the last_transition_time of this V1StatusCondition.  # noqa: E501


        :return: The last_transition_time of this V1StatusCondition.  # noqa: E501
        :rtype: datetime
        """
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, last_transition_time):
        """Sets the last_transition_time of this V1StatusCondition.


        :param last_transition_time: The last_transition_time of this V1StatusCondition.  # noqa: E501
        :type: datetime
        """

        self._last_transition_time = last_transition_time

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
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
        if not isinstance(other, V1StatusCondition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1StatusCondition):
            return True

        return self.to_dict() != other.to_dict()
