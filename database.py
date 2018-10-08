#!/usr/bin/python3.6
# coding: utf-8

import mysql.connector
import datetime

class ChooseDBFields:
    def __init__(self, user, password, database, host):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.connect = mysql.connector.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               database=self.database)

    def choose_product(self, product_name):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM oc_product_description")
        data = cursor.fetchall()

        result = False
        for i in data:
            if product_name in i:
                result = True
                break

        cursor.close()

        return result

    def add_product(self, name, title, description):
        cursor = self.connect.cursor()
        cursor.execute("SELECT MAX(product_id) FROM oc_product_description")
        lastId = cursor.fetchall()
        id = lastId[0][0] + 1

        cursor.execute("INSERT INTO oc_product_description(product_id, language_id, name, description, tag, "
                       "meta_title, meta_h1, meta_description, meta_keyword) "
                       "VALUES ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(id, 1,
                                                                    name, description, '', title, '', '', ''))

        cursor.close()
        self.connect.close()

        return id

    def add_attribute(self, id, characters):
        cursor = self.connect.cursor()
        key = list(characters.keys())
        for i in range(len(key)):

            if key == 'Бренд':
                cursor.execute("INSERT INTO oc_product_attribute(product_id, attribute_id, text) VALUES ({}, {}, '{}')".format(
                    id, 14, characters[key]))
                cursor.execute("INSERT INTO oc_product_option VALUES ({}, {}, '', 1)".format(id, 14))
                product_option_id = cursor.execute("SELECT MAX(product_option_id) FROM oc_product_option")
                option_id = product_option_id[0][0]
                cursor.execute("INSERT INTO oc_option_value VALUES ({}, '{}', {})".format(option_id, '', 0))
                select_option_value_id = cursor.execute("SELECT MAX(option_value_id) FROM oc_option_value")
                option_value_id = select_option_value_id[0][0]
                cursor.execute("INSERT INTO oc_product_option_value VALUES ({}, {}, {}, {}, {}, {}, {}, '{}', {}, "
                               "'{}', '{}', {})").format(option_id, id, 14, option_value_id, 100, 1, 0.0000, '+',
                                                         0, '+', 0.00, '+')
            elif key == 'Состав':
                cursor.execute("INSERT INTO oc_product_attribute(product_id, attribute_id, text) VALUES ({}, {}, '{}')".format(
                    id, 12, characters[key]))
                cursor.execute("INSERT INTO oc_product_option VALUES ({}, {}, '', 1)".format(id, 12))
                product_option_id = cursor.execute("SELECT MAX(product_option_id) FROM oc_product_option")
                option_id = product_option_id[0][0]
                cursor.execute("INSERT INTO oc_option_value VALUES ({}, '{}', {})".format(option_id, '', 0))
                select_option_value_id = cursor.execute("SELECT MAX(option_value_id) FROM oc_option_value")
                option_value_id = select_option_value_id[0][0]
                cursor.execute("INSERT INTO oc_product_option_value VALUES ({}, {}, {}, {}, {}, {}, {}, '{}', {}, "
                               "'{}', '{}', {})").format(option_id, id, 11, option_value_id, 100, 1, 0.0000, '+',
                                                         0, '+', 0.00, '+')
            elif key == 'Страна производитель':
                cursor.execute("INSERT INTO oc_product_attribute(product_id, attribute_id, text) VALUES ({}, {}, '{}')".format(
                    id, 13, characters[key]))
                cursor.execute("INSERT INTO oc_product_option VALUES ({}, {}, '', 1)".format(id, 13))
                product_option_id = cursor.execute("SELECT MAX(product_option_id) FROM oc_product_option")
                option_id = product_option_id[0][0]
                cursor.execute("INSERT INTO oc_option_value VALUES ({}, '{}', {})".format(option_id, '', 0))
                select_option_value_id = cursor.execute("SELECT MAX(option_value_id) FROM oc_option_value")
                option_value_id = select_option_value_id[0][0]
                cursor.execute("INSERT INTO oc_product_option_value VALUES ({}, {}, {}, {}, {}, {}, {}, '{}', {}, "
                               "'{}', '{}', {})").format(option_id, id, 13, option_value_id, 100, 1, 0.0000, '+',
                                                         0, '+', 0.00, '+')

        cursor.close()
        self.connect.close()

    def add_image(self, productID, imgName, sort):
        cursor = self.connect.cursor()
        cursor.execute("SELECT MAX(product_image_id) FROM oc_product_image")
        selectImageID = cursor.fetchall()
        imageID = selectImageID[0][0] + 1
        cursor.execute("INSERT INTO oc_product_image(product_image_id, product_id, image, sort_order) "
                       "VALUES ({}, {}, '{}', {})".format(productID, imageID, imgName, sort))

        cursor.close()
        self.connect.close()

    def add_product_first(self, product_id, model, image, manufacturer_id, price, date_now):
        cursor = self.connect.cursor()
        cursor.execute("INSERT INTO oc_product VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, "
                       "'{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}')".format(
            product_id, model, '', '', '', '', '', '', '', 500, 7, image, manufacturer_id, 1, price, 0, 0,
            date_now.date(), 0.00, 1, 0.00, 0.00, 0.00, 1, 1, 1, 100, 1, 0, date_now,
            datetime.datetime.strptime('0000-00-00', '%Y-%m-%d'), ''))

        cursor.close()
        self.connect.close()

    def get_manufacturer_id(self, manufacturer):
        cursor = self.connect.cursor()
        cursor.execute("SELECT manufacturer_id FROM oc_manufacturer WHERE name='{}'".format(manufacturer))
        manufacturer_id = cursor.fetchall()

        cursor.close()
        self.connect.close()

        return manufacturer_id

    def add_product_category(self, product_id, category_id):
        cursor = self.connect.cursor()
        cursor.execute("INSERT INTO oc_product_to_category VALUES ({}, {}, 0)".format(product_id, category_id))

        cursor.close()
        self.connect.close()