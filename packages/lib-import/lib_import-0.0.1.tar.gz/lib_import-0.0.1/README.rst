lib_import
==================

django_lib_import is a Django library for importing data (file -> database).
It is based on django-import-export


Two possible types of import are defined :

- Create only
   New objects are created, but existing objects are not updated, and
   corresponding rows are skipped.

- Create and update
   New objects are created, existing objects are updated.
