import json
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from tests.management.commands.fake_temp_model import FakeTempModelTest


class PosGreenMigrateTest(FakeTempModelTest, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.connection_mock = mock.patch('green_migration.management.commands.pos_green_migrate.connection')
        connection = self.connection_mock.start()
        schema_editor_context = connection.schema_editor.return_value
        self.schema_editor = schema_editor_context.__enter__.return_value
        self.start_fake_temp_model('green_migration.management.commands.pos_green_migrate.apps')

    def tearDown(self) -> None:
        super().tearDown()
        self.connection_mock.stop()
        self.stop_fake_temp_model()

    def test_pos_green_migrate_remove_field(self):
        with open('/tmp/green_migrate.json', 'w') as f:
            json.dump({'green_migration': {'temp_model': ['config']}}, f)
        call_command('pos_green_migrate', '/tmp/green_migrate.json')
        self.schema_editor.remove_field.assert_called_with(self.temp_model, self.config_field)

    def test_pos_green_migrate_remove_field_not_exists(self):
        with open('/tmp/green_migrate.json', 'w') as f:
            json.dump({'green_migration': {'temp_model': ['xxx']}}, f)
        call_command('pos_green_migrate', '/tmp/green_migrate.json')
        self.schema_editor.remove_field.assert_not_called()
