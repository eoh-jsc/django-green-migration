import json

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('green_migrate_output', type=str)

    def handle(self, green_migrate_output, *args, **options):
        with connection.schema_editor() as schema_editor:
            green_migrate_output = json.loads(green_migrate_output)
            for app, removed_model_fields in green_migrate_output.items():
                for model, fields in removed_model_fields.items():
                    model_class = apps.get_model(app, model)
                    for field in fields:
                        try:
                            schema_editor.remove_field(model_class, model_class._meta.get_field(field))
                        except FieldDoesNotExist:
                            pass
