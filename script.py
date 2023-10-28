"""script.py"""
# PYTHON IMPORTS
import json
# APP IMPORTS
from coolapp.models import District


def import_district_data():
    # Specify the encoding as 'utf-8' when opening the JSON file
    with open('fixtures/bd-districts.json', 'r', encoding='utf-8') as file:
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

# import_district_data()
