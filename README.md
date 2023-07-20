# django-green-migrations

While the server is running,
if you deploy a new version which contains a migration that drop a field, it will make your production down. 
This is because the migration will be executed before the new code is deployed.
This package will help you to avoid this problem.

## Normal deployment
1. Deploy new code to server
2. Keep server running
3. Run migrations
4. Switch to new code
5. Destroy old code

At step 3, if the migration contains a field drop, the server will be down.

## Green deployment
1. Deploy new code to server
2. Keep server running
3. Run green migration ```python manage.py green_migrate > output.json```
4. Run migrations
5. Switch to new code
6. Destroy old code
7. Run pos green migration ```python manage.py pos_green_migrate output.json```

At step 3, it will modify `drop` migration to `nullable and blankable` migration, this will help both old and new code to work.

At step 7, it will read the output from step 3 to drop fields, this will help to clean up the database.

## Installation
1. Install package
```pip install django-green-migration```
2. Add `green_migration` to `INSTALLED_APPS`
3. Setup deployment like above explanation (make sure don't commit changes at step 3 to git)

## Usage
Run this before running `python manage.py migrate`
```python manage.py green_migrate > output.json```

Run this after running `python manage.py migrate`
```python manage.py pos_green_migrate output.json```

## Skip migration
### Skip file
Add `# gm: ignore` to the top of the file

### Skip field
Add `# gm: ignore` to the end of the line
```python
migrations.RemoveField(  # gm: ignore
```
