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


class V1ProjectEntityResourceRequest(object):
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
    openapi_types = {"owner": "str", "project": "str", "uuid": "str"}

    attribute_map = {"owner": "owner", "project": "project", "uuid": "uuid"}

    def __init__(
        self, owner=None, project=None, uuid=None, local_vars_configuration=None
    ):  # noqa: E501
        """V1ProjectEntityResourceRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._owner = None
        self._project = None
        self._uuid = None
        self.discriminator = None

        if owner is not None:
            self.owner = owner
        if project is not None:
            self.project = project
        if uuid is not None:
            self.uuid = uuid

    @property
    def owner(self):
        """Gets the owner of this V1ProjectEntityResourceRequest.  # noqa: E501


        :return: The owner of this V1ProjectEntityResourceRequest.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this V1ProjectEntityResourceRequest.


        :param owner: The owner of this V1ProjectEntityResourceRequest.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def project(self):
        """Gets the project of this V1ProjectEntityResourceRequest.  # noqa: E501


        :return: The project of this V1ProjectEntityResourceRequest.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this V1ProjectEntityResourceRequest.


        :param project: The project of this V1ProjectEntityResourceRequest.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def uuid(self):
        """Gets the uuid of this V1ProjectEntityResourceRequest.  # noqa: E501


        :return: The uuid of this V1ProjectEntityResourceRequest.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this V1ProjectEntityResourceRequest.


        :param uuid: The uuid of this V1ProjectEntityResourceRequest.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

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
        if not isinstance(other, V1ProjectEntityResourceRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1ProjectEntityResourceRequest):
            return True

        return self.to_dict() != other.to_dict()
