# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for methods in the interaction registry."""

__author__ = 'Sean Lip'

import os

from core.domain import interaction_registry
from core.tests import test_utils
from extensions.interactions import base
import feconf


class InteractionDependencyTests(test_utils.GenericTestBase):
    """Tests for the calculation of dependencies for interactions."""

    def test_deduplication_of_dependency_ids(self):
        self.assertItemsEqual(
            interaction_registry.Registry.get_deduplicated_dependency_ids(
                ['CodeRepl']),
            ['jsrepl', 'codemirror'])

        self.assertItemsEqual(
            interaction_registry.Registry.get_deduplicated_dependency_ids(
                ['CodeRepl', 'CodeRepl', 'CodeRepl']),
            ['jsrepl', 'codemirror'])

        self.assertItemsEqual(
            interaction_registry.Registry.get_deduplicated_dependency_ids(
                ['CodeRepl', 'LogicProof']),
            ['jsrepl', 'codemirror', 'logic_proof'])


class InteractionRegistryUnitTests(test_utils.GenericTestBase):
    """Test for the interaction registry."""

    def test_allowed_interactions_and_counts(self):
        """Do sanity checks on the ALLOWED_INTERACTIONS dict in feconf.py."""
        self.assertEqual(
            len(interaction_registry.Registry.get_all_interactions()),
            len(feconf.ALLOWED_INTERACTIONS))

        for (interaction_name, interaction_definition) in (
                feconf.ALLOWED_INTERACTIONS.iteritems()):
            contents = os.listdir(
                os.path.join(os.getcwd(), interaction_definition['dir']))
            self.assertIn('%s.py' % interaction_name, contents)

    def test_get_all_configs(self):
        """Test the get_all_configs() method."""
        EXPECTED_TERMINAL_INTERACTIONS_COUNT = 1

        configs_dict = interaction_registry.Registry.get_all_configs()
        self.assertEqual(
            len(configs_dict.keys()), len(feconf.ALLOWED_INTERACTIONS))

        terminal_interactions_count = 0
        for item in configs_dict.values():
            self.assertIn(item['display_mode'], base.ALLOWED_DISPLAY_MODES)
            self.assertTrue(isinstance(item['is_terminal'], bool))
            if item['is_terminal']:
                terminal_interactions_count += 1

        self.assertEqual(
            terminal_interactions_count, EXPECTED_TERMINAL_INTERACTIONS_COUNT)