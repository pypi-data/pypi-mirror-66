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
Package to test the openlp.core.ui.firsttimeform package.
"""
import os
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, call, patch, DEFAULT

from PyQt5 import QtWidgets

from openlp.core.common.registry import Registry
from openlp.core.ui.firsttimeform import FirstTimeForm, ThemeListWidgetItem
from tests.helpers.testmixin import TestMixin


INVALID_CONFIG = """
{
  "_comments": "The most recent version should be added to https://openlp.org/files/frw/download_3.0.json",
  "_meta": {
}
"""


class TestThemeListWidgetItem(TestCase):
    """
    Test the :class:`ThemeListWidgetItem` class
    """

    def setUp(self):
        self.sample_theme_data = {'file_name': 'BlueBurst.otz', 'sha256': 'sha_256_hash',
                                  'thumbnail': 'BlueBurst.png', 'title': 'Blue Burst'}
        download_worker_patcher = patch('openlp.core.ui.firsttimeform.DownloadWorker')
        self.addCleanup(download_worker_patcher.stop)
        self.mocked_download_worker = download_worker_patcher.start()
        run_thread_patcher = patch('openlp.core.ui.firsttimeform.run_thread')
        self.addCleanup(run_thread_patcher.stop)
        self.mocked_run_thread = run_thread_patcher.start()

    def test_init_sample_data(self):
        """
        Test that the theme data is loaded correctly in to a ThemeListWidgetItem object when instantiated
        """
        # GIVEN: A sample theme dictionary object
        # WHEN: Creating an instance of `ThemeListWidgetItem`
        instance = ThemeListWidgetItem('url', self.sample_theme_data, MagicMock())

        # THEN: The data should have been set correctly
        assert instance.file_name == 'BlueBurst.otz'
        assert instance.sha256 == 'sha_256_hash'
        assert instance.text() == 'Blue Burst'
        assert instance.toolTip() == 'Blue Burst'
        self.mocked_download_worker.assert_called_once_with('url', 'BlueBurst.png')

    def test_init_download_worker(self):
        """
        Test that the `DownloadWorker` worker is set up correctly and that the thread is started.
        """
        # GIVEN: A sample theme dictionary object
        mocked_ftw = MagicMock(spec=FirstTimeForm)
        mocked_ftw.thumbnail_download_threads = []

        # WHEN: Creating an instance of `ThemeListWidgetItem`
        instance = ThemeListWidgetItem('url', self.sample_theme_data, mocked_ftw)

        # THEN: The `DownloadWorker` should have been set up with the appropriate data
        self.mocked_download_worker.assert_called_once_with('url', 'BlueBurst.png')
        self.mocked_download_worker.download_failed.connect.called_once_with(instance._on_download_failed())
        self.mocked_download_worker.download_succeeded.connect.called_once_with(instance._on_thumbnail_downloaded)
        self.mocked_run_thread.assert_called_once_with(
            self.mocked_download_worker(), 'thumbnail_download_BlueBurst.png')
        assert mocked_ftw.thumbnail_download_threads == ['thumbnail_download_BlueBurst.png']


class TestFirstTimeForm(TestCase, TestMixin):

    def setUp(self):
        self.setup_application()
        self.app.setApplicationVersion('0.0')
        # Set up a fake "set_normal_cursor" method since we're not dealing with an actual OpenLP application object
        self.app.set_normal_cursor = lambda: None
        self.app.process_events = lambda: None
        Registry.create()
        Registry().register('application', self.app)
        self.tempfile = os.path.join(tempfile.gettempdir(), 'testfile')

    def tearDown(self):
        if os.path.isfile(self.tempfile):
            os.remove(self.tempfile)

    def test_initialise(self):
        """
        Test if we can intialise the FirstTimeForm
        """
        # GIVEN: A First Time Wizard and an expected screen object
        frw = FirstTimeForm(None)
        expected_screens = MagicMock()

        # WHEN: The First Time Wizard is initialised
        frw.initialize(expected_screens)

        # THEN: The screens should be set up, and the default values initialised
        assert expected_screens == frw.screens, 'The screens should be correct'
        assert frw.web_access is True, 'The default value of self.web_access should be True'
        assert [] == frw.thumbnail_download_threads, 'The list of threads should be empty'
        assert frw.has_run_wizard is False, 'has_run_wizard should be False'

    @patch('openlp.core.ui.firsttimeform.QtWidgets.QWizard.exec')
    def test_exec(self, mocked_qwizard_exec):

        # GIVEN: An instance of FirstTimeForm
        frw = FirstTimeForm(None)
        with patch.object(frw, 'set_defaults') as mocked_set_defaults:

            # WHEN: exec is called
            frw.exec()

            # THEN: The wizard should be reset and the exec methon on the super class should have been called
            mocked_set_defaults.assert_called_once()
            mocked_qwizard_exec.assert_called_once()

    def test_set_defaults(self):
        """
        Test that the default values are set when set_defaults() is run
        """
        # GIVEN: An initialised FRW and a whole lot of stuff mocked out
        frw = FirstTimeForm(None)
        frw.initialize(MagicMock())
        mocked_settings = MagicMock()
        mocked_settings.value.side_effect = lambda key: {'core/has run wizard': False}[key]
        with patch.object(frw, 'restart') as mocked_restart, \
                patch.object(frw, 'currentIdChanged') as mocked_currentIdChanged, \
                patch.object(frw, 'theme_combo_box') as mocked_theme_combo_box, \
                patch.object(frw, 'songs_check_box') as mocked_songs_check_box, \
                patch.object(Registry, 'register_function') as mocked_register_function, \
                patch('openlp.core.ui.firsttimeform.Settings', return_value=mocked_settings), \
                patch('openlp.core.ui.firsttimeform.gettempdir', return_value='temp') as mocked_gettempdir, \
                patch('openlp.core.ui.firsttimeform.create_paths') as mocked_create_paths, \
                patch.object(frw.application, 'set_normal_cursor'):
            mocked_theme_manager = MagicMock()
            Registry().register('theme_manager', mocked_theme_manager)

            # WHEN: The set_defaults() method is run
            frw.set_defaults()

            # THEN: The default values should have been set
            mocked_restart.assert_called_once()
            assert 'https://get.openlp.org/ftw/' == frw.web, 'The default URL should be set'
            mocked_currentIdChanged.connect.assert_called_once_with(frw.on_current_id_changed)
            mocked_register_function.assert_called_once_with('config_screen_changed', frw.screen_selection_widget.load)
            mocked_settings.value.assert_has_calls([call('core/has run wizard')])
            mocked_gettempdir.assert_called_once()
            mocked_create_paths.assert_called_once_with(Path('temp', 'openlp'))
            mocked_theme_combo_box.clear.assert_called_once()
            mocked_theme_manager.assert_not_called()
            mocked_songs_check_box.assert_not_called()

    def test_set_defaults_rerun(self):
        """
        Test that the default values are set when set_defaults() is run
        """
        # GIVEN: An initialised FRW and a whole lot of stuff mocked out
        frw = FirstTimeForm(None)
        frw.initialize(MagicMock())
        mocked_settings = MagicMock()
        mocked_settings.value.side_effect = \
            lambda key: {'core/has run wizard': True, 'themes/global theme': 'Default Theme'}[key]
        with patch.object(frw, 'restart') as mocked_restart, \
                patch.object(frw, 'currentIdChanged') as mocked_currentIdChanged, \
                patch.object(frw, 'theme_combo_box', **{'findText.return_value': 3}) as mocked_theme_combo_box, \
                patch.multiple(frw, songs_check_box=DEFAULT, bible_check_box=DEFAULT, presentation_check_box=DEFAULT,
                               image_check_box=DEFAULT, media_check_box=DEFAULT, custom_check_box=DEFAULT,
                               song_usage_check_box=DEFAULT, alert_check_box=DEFAULT), \
                patch.object(Registry, 'register_function') as mocked_register_function, \
                patch('openlp.core.ui.firsttimeform.Settings', return_value=mocked_settings), \
                patch('openlp.core.ui.firsttimeform.gettempdir', return_value='temp') as mocked_gettempdir, \
                patch('openlp.core.ui.firsttimeform.create_paths') as mocked_create_paths, \
                patch.object(frw.application, 'set_normal_cursor'):
            mocked_plugin_manager = MagicMock()
            mocked_theme_manager = MagicMock(**{'get_theme_names.return_value': ['b', 'a', 'c']})
            Registry().register('plugin_manager', mocked_plugin_manager)
            Registry().register('theme_manager', mocked_theme_manager)

            # WHEN: The set_defaults() method is run
            frw.set_defaults()

            # THEN: The default values should have been set
            mocked_restart.assert_called_once()
            assert 'https://get.openlp.org/ftw/' == frw.web, 'The default URL should be set'
            mocked_currentIdChanged.connect.assert_called_once_with(frw.on_current_id_changed)
            mocked_register_function.assert_called_once_with('config_screen_changed', frw.screen_selection_widget.load)
            mocked_settings.value.assert_has_calls([call('core/has run wizard'), call('themes/global theme')])
            mocked_gettempdir.assert_called_once()
            mocked_create_paths.assert_called_once_with(Path('temp', 'openlp'))
            mocked_theme_manager.get_theme_names.assert_called_once()
            mocked_theme_combo_box.clear.assert_called_once()
            mocked_plugin_manager.get_plugin_by_name.assert_has_calls(
                [call('songs'), call('bibles'), call('presentations'), call('images'), call('media'), call('custom'),
                 call('songusage'), call('alerts')], any_order=True)
            mocked_plugin_manager.get_plugin_by_name.assert_has_calls([call().is_active()] * 8, any_order=True)
            mocked_theme_combo_box.addItems.assert_called_once_with(['a', 'b', 'c'])
            mocked_theme_combo_box.findText.assert_called_once_with('Default Theme')
            mocked_theme_combo_box.setCurrentIndex(3)

    @patch('openlp.core.ui.firsttimeform.Settings')
    @patch('openlp.core.ui.firsttimeform.QtWidgets.QWizard.accept')
    def test_accept_method(self, mocked_qwizard_accept, *args):
        """
        Test the FirstTimeForm.accept method
        """
        # GIVEN: An instance of FirstTimeForm
        frw = FirstTimeForm(None)
        with patch.object(frw, '_set_plugin_status') as mocked_set_plugin_status, \
                patch.multiple(frw, songs_check_box=DEFAULT, bible_check_box=DEFAULT, presentation_check_box=DEFAULT,
                               image_check_box=DEFAULT, media_check_box=DEFAULT, custom_check_box=DEFAULT,
                               song_usage_check_box=DEFAULT, alert_check_box=DEFAULT) as mocked_check_boxes, \
                patch.object(frw, 'screen_selection_widget') as mocked_screen_selection_widget:

            # WHEN: Calling accept
            frw.accept()

            # THEN: The selected plugins should be enabled, the screen selection saved and the super method called
            mocked_set_plugin_status.assert_has_calls([
                call(mocked_check_boxes['songs_check_box'], 'songs/status'),
                call(mocked_check_boxes['bible_check_box'], 'bibles/status'),
                call(mocked_check_boxes['presentation_check_box'], 'presentations/status'),
                call(mocked_check_boxes['image_check_box'], 'images/status'),
                call(mocked_check_boxes['media_check_box'], 'media/status'),
                call(mocked_check_boxes['custom_check_box'], 'custom/status'),
                call(mocked_check_boxes['song_usage_check_box'], 'songusage/status'),
                call(mocked_check_boxes['alert_check_box'], 'alerts/status')])
            mocked_screen_selection_widget.save.assert_called_once()
            mocked_qwizard_accept.assert_called_once()

    @patch('openlp.core.ui.firsttimeform.Settings')
    def test_accept_method_theme_not_selected(self, mocked_settings):
        """
        Test the FirstTimeForm.accept method when there is no default theme selected
        """
        # GIVEN: An instance of FirstTimeForm
        frw = FirstTimeForm(None)
        with patch.object(frw, '_set_plugin_status'), patch.object(frw, 'screen_selection_widget'), \
                patch.object(frw, 'theme_combo_box', **{'currentIndex.return_value': -1}):

            # WHEN: Calling accept and the currentIndex method of the theme_combo_box returns -1
            frw.accept()

            # THEN: OpenLP should not try to save a theme name
            mocked_settings().setValue.assert_not_called()

    @patch('openlp.core.ui.firsttimeform.Settings')
    def test_accept_method_theme_selected(self, mocked_settings):
        """
        Test the FirstTimeForm.accept method when a default theme is selected
        """
        # GIVEN: An instance of FirstTimeForm
        frw = FirstTimeForm(None)
        with patch.object(frw, '_set_plugin_status'), \
                patch.object(frw, 'screen_selection_widget'), \
                patch.object(
                frw, 'theme_combo_box', **{'currentIndex.return_value': 0, 'currentText.return_value': 'Test Item'}):

            # WHEN: Calling accept and the currentIndex method of the theme_combo_box returns 0
            frw.accept()

            # THEN: The 'currentItem' in the combobox should have been set as the default theme.
            mocked_settings().setValue.assert_called_once_with('themes/global theme', 'Test Item')

    @patch('openlp.core.ui.firsttimeform.QtWidgets.QWizard.reject')
    @patch('openlp.core.ui.firsttimeform.time')
    @patch('openlp.core.ui.firsttimeform.get_thread_worker')
    @patch('openlp.core.ui.firsttimeform.is_thread_finished')
    def test_reject_method(
            self, mocked_is_thread_finished, mocked_get_thread_worker, mocked_time, mocked_qwizard_reject):
        """
        Test that the reject method shuts down the threads correctly
        """
        # GIVEN: A FRW, some mocked threads and workers (that isn't quite done) and other mocked stuff
        mocked_worker = MagicMock()
        mocked_get_thread_worker.return_value = mocked_worker
        mocked_is_thread_finished.side_effect = [False, True]
        frw = FirstTimeForm(None)
        frw.initialize(MagicMock())
        frw.thumbnail_download_threads = ['test_thread']
        with patch.object(frw.application, 'set_normal_cursor') as mocked_set_normal_cursor:

            # WHEN: the reject method is called
            frw.reject()

            # THEN: The right things should be called in the right order
            mocked_get_thread_worker.assert_called_once_with('test_thread')
            mocked_worker.cancel_download.assert_called_once()
            mocked_is_thread_finished.assert_called_with('test_thread')
            assert mocked_is_thread_finished.call_count == 2, 'isRunning() should have been called twice'
            mocked_time.sleep.assert_called_once_with(0.1)
            mocked_set_normal_cursor.assert_called_once()
            mocked_qwizard_reject.assert_called_once()

    @patch('openlp.core.ui.firsttimeform.ProxyDialog')
    def test_on_custom_button_clicked(self, mocked_proxy_dialog):
        """
        Test _on_custom_button when it is called whe the 'internet settings' (CustomButton1) button is not clicked.
        """
        # GIVEN: An instance of the FirstTimeForm
        frw = FirstTimeForm(None)

        # WHEN: Calling _on_custom_button_clicked with a different button to the 'internet settings button.
        frw._on_custom_button_clicked(QtWidgets.QWizard.CustomButton2)

        # THEN: The ProxyDialog should not be shown.
        mocked_proxy_dialog.assert_not_called()

    @patch('openlp.core.ui.firsttimeform.ProxyDialog')
    def test_on_custom_button_clicked_internet_settings(self, mocked_proxy_dialog):
        """
        Test _on_custom_button when it is called when the 'internet settings' (CustomButton1) button is clicked.
        """
        # GIVEN: An instance of the FirstTimeForm
        frw = FirstTimeForm(None)

        # WHEN: Calling _on_custom_button_clicked with the constant for the 'internet settings' button (CustomButton1)
        frw._on_custom_button_clicked(QtWidgets.QWizard.CustomButton1)

        # THEN: The ProxyDialog should be shown.
        mocked_proxy_dialog.assert_called_with(frw)
        mocked_proxy_dialog().retranslate_ui.assert_called_once()
        mocked_proxy_dialog().exec.assert_called_once()

    @patch('openlp.core.ui.firsttimeform.critical_error_message_box')
    def test__parse_config_invalid_config(self, mocked_critical_error_message_box):
        """
        Test `FirstTimeForm._parse_config` when called with invalid data
        """
        # GIVEN: An instance of `FirstTimeForm`
        first_time_form = FirstTimeForm(None)

        # WHEN: Calling _parse_config with a string containing invalid data
        result = first_time_form._parse_config(INVALID_CONFIG)

        # THEN: _parse_data should return False and the user should have should have been informed.
        assert result is False
        mocked_critical_error_message_box.assert_called_once()

    @patch('openlp.core.ui.firsttimeform.get_web_page')
    @patch('openlp.core.ui.firsttimeform.QtWidgets.QMessageBox')
    def test_network_error(self, mocked_message_box, mocked_get_web_page):
        """
        Test we catch a network error in First Time Wizard - bug 1409627
        """
        # GIVEN: Initial setup and mocks
        first_time_form = FirstTimeForm(None)
        first_time_form.initialize(MagicMock())
        mocked_get_web_page.side_effect = ConnectionError('')
        mocked_message_box.Ok = 'OK'

        # WHEN: the First Time Wizard calls to get the initial configuration
        first_time_form._download_index()

        # THEN: the critical_error_message_box should have been called
        mocked_message_box.critical.assert_called_once_with(
            first_time_form, 'Network Error',
            'There was a network error attempting to connect to retrieve initial configuration information', 'OK')

    @patch('openlp.core.ui.firsttimeform.Settings')
    def test_on_projectors_check_box_checked(self, MockSettings):
        """
        Test that the projector panel is shown when the checkbox in the first time wizard is checked
        """
        # GIVEN: A First Time Wizard and a mocked settings object
        frw = FirstTimeForm(None)
        mocked_settings = MagicMock()
        mocked_settings.value.return_value = True
        MockSettings.return_value = mocked_settings

        # WHEN: on_projectors_check_box_clicked() is called
        frw.on_projectors_check_box_clicked()

        # THEN: The visibility of the projects panel should have been set
        mocked_settings.value.assert_called_once_with('projector/show after wizard')
        mocked_settings.setValue.assert_called_once_with('projector/show after wizard', False)

    @patch('openlp.core.ui.firsttimeform.Settings')
    def test_on_projectors_check_box_unchecked(self, MockSettings):
        """
        Test that the projector panel is shown when the checkbox in the first time wizard is checked
        """
        # GIVEN: A First Time Wizard and a mocked settings object
        frw = FirstTimeForm(None)
        mocked_settings = MagicMock()
        mocked_settings.value.return_value = False
        MockSettings.return_value = mocked_settings

        # WHEN: on_projectors_check_box_clicked() is called
        frw.on_projectors_check_box_clicked()

        # THEN: The visibility of the projects panel should have been set
        mocked_settings.value.assert_called_once_with('projector/show after wizard')
        mocked_settings.setValue.assert_called_once_with('projector/show after wizard', True)
