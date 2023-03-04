import json
from collections import defaultdict
from io import StringIO

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        stdout = StringIO()
        call_command('migrate', plan=True, stdout=stdout, no_color=True)
        output = stdout.getvalue()
        lines = output.splitlines()

        # todo Bang: handle case remove field, then add back, then remove again
        migration_files = [x.split('.') for x in lines if not x.startswith(' ') and '.' in x]
        for migration_file in migration_files[:]:
            app_name, filename = migration_file
            app_path = apps.get_app_config(app_name).path
            if not app_path.startswith(settings.BASE_DIR):  # pragma: nocover for library app
                migration_files.remove(migration_file)
            else:
                migration_file.append(app_path)

        migration_files = [{'file': f'{x[2]}/migrations/{x[1]}.py', 'app': x[0]} for x in migration_files]
        removed_apps_fields = defaultdict(lambda: defaultdict(list))
        for migration_file in migration_files:
            removed_fields = self.modify_migration(migration_file)
            if removed_fields:
                for model, removed_field_names in self.get_removed_field_and_model(removed_fields).items():
                    removed_apps_fields[migration_file['app']][model] += removed_field_names

        self.stdout.write('------------------deleted_fields------------------')
        self.stdout.write(json.dumps(removed_apps_fields))

    def get_removed_field_and_model(self, removed_fields):
        removed_app_fields = defaultdict(list)
        for removed_field in removed_fields:
            model = removed_field['model']
            field = removed_field['field']
            removed_app_fields[model].append(field)

        return removed_app_fields

    def get_removed_fields(self, content):
        lines = content.splitlines()
        line_nos = []
        for index, line in enumerate(lines):
            if line.endswith('migrations.RemoveField('):
                line_nos.append({
                    'line': index,
                    'model': lines[index + 1].strip().split("'")[1],
                    'field': lines[index + 2].strip().split("'")[1],
                })

        line_nos.reverse()
        return line_nos

    def replace_remove_by_char_blank_null_field(self, content, removed_field):
        line_no = removed_field['line']
        new_field = 'models.CharField(blank=True, null=True, max_length=254)'

        lines = content.splitlines()
        lines[line_no] = lines[line_no].replace('migrations.RemoveField', 'migrations.AlterField')
        lines.insert(line_no + 3, ' ' * 12 + f'field={new_field},')
        return '\n'.join(lines)

    def modify_migration(self, migration_file):
        filename = migration_file['file']
        with open(filename) as f:
            content = f.read()

        if 'migrations.RemoveField(' not in content:
            return

        if 'models.' not in content:
            content = content.replace('from django.db import migrations', 'from django.db import migrations, models')

        removed_fields = self.get_removed_fields(content)

        for removed_field in removed_fields:
            content = self.replace_remove_by_char_blank_null_field(content, removed_field)

        with open(filename, 'w') as f:
            f.write(content)

        return removed_fields
