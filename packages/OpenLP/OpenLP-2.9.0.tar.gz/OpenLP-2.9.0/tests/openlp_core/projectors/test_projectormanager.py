# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2019 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Interface tests to test the themeManager class and related methods.
"""
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from openlp.core.common.registry import Registry
from openlp.core.projectors.db import ProjectorDB
from openlp.core.projectors.editform import ProjectorEditForm
from openlp.core.projectors.manager import ProjectorManager
from tests.helpers.testmixin import TestMixin
from tests.resources.projector.data import TEST_DB


class TestProjectorManager(TestCase, TestMixin):
    """
    Test the functions in the ProjectorManager module
    """
    def setUp(self):
        """
        Create the UI and setup necessary options
        """
        self.setup_application()
        self.build_settings()
        Registry.create()
        with patch('openlp.core.projectors.db.init_url') as mocked_init_url:
            if os.path.exists(TEST_DB):
                os.unlink(TEST_DB)
            mocked_init_url.return_value = 'sqlite:///%s' % TEST_DB
            self.projectordb = ProjectorDB()
            if not hasattr(self, 'projector_manager'):
                self.projector_manager = ProjectorManager(projectordb=self.projectordb)

    def tearDown(self):
        """
        Remove test database.
        Delete all the C++ objects at the end so that we don't have a segfault.
        """
        self.projectordb.session.close()
        self.destroy_settings()
        del self.projector_manager

    def test_bootstrap_initialise(self):
        """
        Test initialize calls correct startup functions
        """
        # WHEN: we call bootstrap_initialise
        self.projector_manager.bootstrap_initialise()
        # THEN: ProjectorDB is setup
        assert type(self.projector_manager.projectordb) == ProjectorDB, \
            'Initialization should have created a ProjectorDB() instance'

    def test_bootstrap_post_set_up(self):
        """
        Test post-initialize calls proper setups
        """
        # GIVEN: setup mocks
        self.projector_manager._load_projectors = MagicMock()

        # WHEN: Call to initialize is run
        self.projector_manager.bootstrap_initialise()
        self.projector_manager.bootstrap_post_set_up()

        # THEN: verify calls to retrieve saved projectors and edit page initialized
        assert 1 == self.projector_manager._load_projectors.call_count, \
            'Initialization should have called load_projectors()'
        assert type(self.projector_manager.projector_form) == ProjectorEditForm, \
            'Initialization should have created a Projector Edit Form'
        assert self.projector_manager.projectordb is self.projector_manager.projector_form.projectordb, \
            'ProjectorEditForm should be using same ProjectorDB() instance as ProjectorManager'
