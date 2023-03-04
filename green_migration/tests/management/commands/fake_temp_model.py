from unittest import mock

from django.core.exceptions import FieldDoesNotExist


class FakeTempModelTest:
    def start_fake_temp_model(self, path):
        self.apps_mock = mock.patch(f'{path}.get_model')
        get_model = self.apps_mock.start()
        self.temp_model = get_model.return_value
        self.config_field = mock.MagicMock()

        def get_field(field_name):
            if field_name == 'config':
                return self.config_field
            raise FieldDoesNotExist()

        self.temp_model._meta.get_field = get_field

    def stop_fake_temp_model(self):
        self.apps_mock.stop()
