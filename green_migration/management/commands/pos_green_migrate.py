import json

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('green_migrate_output_file', type=str)

    def handle(self, green_migrate_output_file, *args, **options):
        with open(green_migrate_output_file) as f:
            green_migrate_output = json.load(f)
        with connection.schema_editor() as schema_editor:
            for app, removed_model_fields in green_migrate_output.items():
                for model, fields in removed_model_fields.items():
                    model_class = apps.get_model(app, model)
                    for field in fields:
                        try:
                            schema_editor.remove_field(model_class, model_class._meta.get_field(field))
                        except FieldDoesNotExist:
                            pass
