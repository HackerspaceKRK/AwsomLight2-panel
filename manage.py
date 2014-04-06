#!/usr/bin/python3
import os
import sys

sys.path.append('/usr/share/pyshared/')

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panel.settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
