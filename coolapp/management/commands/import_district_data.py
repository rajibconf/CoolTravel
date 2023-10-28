"""coolapp > management > commands > import_district_data.py"""
# PYTHON IMPORTS
import json
# DJANGO IMPORTS
from django.core.management.base import BaseCommand
# APP IMPORTS
from coolapp.models import District


class Command(BaseCommand):
    help = 'Import district data from a JSON file'

    def handle(self, *args, **options):
        json_file_path = 'fixtures/bd-districts.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for district_data in data['districts']:
            District.objects.create(
                id=district_data['id'],
                division_id=district_data['division_id'],
                name=district_data['name'],
                bn_name=district_data['bn_name'],
                lat=district_data['lat'],
                long=district_data['long']
            )

        self.stdout.write(self.style.SUCCESS(
            'District data imported successfully.'
        ))
