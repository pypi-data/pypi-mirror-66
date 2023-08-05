# Copyright (c) 2019 - The Procedural Generation for Gazebo authors
# For information on the respective copyright owner see the NOTICE file
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..types import XMLBase
from .restitution_coefficient import RestitutionCoefficient
from .threshold import Threshold


class Bounce(XMLBase):
    _NAME = 'bounce'
    _TYPE = 'sdf'
    _CHILDREN_CREATORS = dict(
        restitution_coefficient=dict(
            creator=RestitutionCoefficient, default=[0]), threshold=dict(
            creator=Threshold, default=[100000]))

    def __init__(self):
        XMLBase.__init__(self)
        self.reset()

    @property
    def restitution_coefficient(self):
        return self._get_child_element('restitution_coefficient')

    @restitution_coefficient.setter
    def restitution_coefficient(self, value):
        assert value >= 0
        self._add_child_element('restitution_coefficient', value)

    @property
    def threshold(self):
        return self._get_child_element('threshold')

    @threshold.setter
    def threshold(self, value):
        self._add_child_element('threshold', value)
