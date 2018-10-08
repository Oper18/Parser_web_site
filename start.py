#!/usr/bin/python3.6
# coding: utf-8

import time
import json
import datetime
from get_page import GetPage
from database import ChooseDBFields

def start_parser():
    with open('settings.json') as f:
        dbset = json.load(f)

    with open('pages.json') as f:
        pages = json.load(f)

    with open('categoryID.json') as f:
        category_ids = json.load(f)

    for i in range(len(list(pages.keys()))):
        key = list(pages.keys())[i]
        for j in range(len(list(pages[key].keys()))):
            key2 = list(pages[key].keys())[j]
            catalog = GetPage().parse_file(pages[key][key2])

            for k in range(len(list(catalog.keys()))):
                key = list(catalog.keys())[k]
                category_id = category_ids[key][key2]
                result = ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).choose_product(key)
                if result is True:
                    continue
                else:
                    if 'description' in list(catalog[key].keys()):
                        description = catalog[key]['description']
                        description = description.split('>')
                        if len(description) > 1:
                            description = description[1]
                        else:
                            description = description[0]
                    else:
                        description = ''
                    id = ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).add_product(
                        key, key, description)

                    ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).add_attribute(
                        id, catalog[key]['characters'])

                    for n in range(catalog[key]['sort']):
                        ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).add_image(
                            id, catalog[key]['images'][n], i+1)

                    manufacturer_id = ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).get_manufacturer_id(
                        catalog[key]['manufacturer'])

                    ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).add_product_first(
                        id, catalog[key]['item'], catalog[key]['images'][0], manufacturer_id, catalog[key]['price'],
                        datetime.datetime.today().date())

                    ChooseDBFields(dbset['user'], dbset['password'], dbset['database'], dbset['host']).add_product_category(
                        id, category_id)