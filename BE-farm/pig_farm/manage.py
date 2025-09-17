#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pig_farm.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def hard_delete_medicine(med_id):
    from core import sql_models
    sql_models.Medicine.objects.filter(id=med_id).delete()

def hard_delete_pig(pig_id):
    from core import sql_models
    sql_models.Pig.objects.filter(id=pig_id).delete()


if __name__ == '__main__':
    main()
