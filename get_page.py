#!/usr/bin/python3.6
# coding: utf-8

import requests
import re

class GetPage:
    def __init__(self):
        self.catalog = {}

    def get_page(self, page, file_name):
        page_code = requests.get(page)
        file = open(file_name, 'w')
        file.write(page_code.text)
        file.close()

        file = open(file_name, 'r')
        file_code = file.read()
        file.close()

        file_code = file_code.split('<')
        file = open(file_name, 'w')
        for i in range(len(file_code)):
            file_code[i] = '<' + file_code[i]
            file.write(file_code[i]+'\n')
        file.close()

    def choose_first_catalog_string(self, addr, file_name):
        self.get_page(addr, file_name)
        file = open(file_name, 'r')
        parseFile = file.readlines()
        file.close()

        catalogString = 0

        for i in range(len(parseFile)):
            catalog = re.findall(r'div class=\'itemsBlock cornerBox\'', parseFile[i])
            if len(catalog) != 0:
                catalogString = i

        return catalogString

    def parse_file(self, addr):
        file_name = 'catalog.html'
        stringNum = self.choose_first_catalog_string(addr, file_name)

        file = open(file_name, 'r')
        parseFile = file.readlines()
        file.close()

        for i in range(stringNum, len(parseFile)):
            productName = re.findall(r'div class=\'itemCaption\'', parseFile[i])
            if len(productName) != 0:
                productName = parseFile[i].split('>')
                productName = productName[1]
                self.catalog[productName] = {}
                startLine = 0
                stopLine = 0
                for j in range(i, len(parseFile)):
                    charactersStart = re.findall(r'<div class=\'item-info\'>', parseFile[j])
                    charactersStop = re.findall(r'<div class=\'itemPrice\'>', parseFile[j])
                    if len(charactersStart) != 0:
                        startLine = j
                    elif len(charactersStop) != 0:
                        stopLine = j
                    elif startLine != 0 and stopLine != 0:
                        break
                characters = self.choose_characters(startLine, stopLine, parseFile)
                self.catalog[productName]['characters'] = characters
                for j in range(i, len(parseFile)):
                    price = re.findall(r'<div class=\'itemPrice\'>', parseFile[i])
                    if len(price) != 0:
                        price = parseFile[j+1].split('>')
                        self.catalog[productName]['price'] = price[1]
                        break

                for j in range(i, len(parseFile)):
                    item = re.findall(r'<div class=\'btnQuick\' item=', parseFile[i])
                    if len(item) != 0:
                        item = re.findall(r'[0-9]+', item[0])
                        if len(item) != 0:
                            item = item[0]
                            self.catalog[productName]['item'] = item
                            break
                try:
                    productAddr = self.set_product_addr(i, parseFile, addr)
                except TypeError:
                    break
                description = self.choose_product_description(productAddr)
                self.catalog[productName]['description'] = description
                sort = self.get_product_img('-1000x1340.jpg', '-105x140.jpg')
                self.catalog[productName]['sort'] = sort[0]
                self.catalog[productName]['images'] = sort[1]
                manufacturer = self.get_manufacturer_id(self.catalog[productName]['characters'])
                self.catalog[productName]['manufacturer'] = manufacturer

        return self.catalog

    def choose_characters(self, start, stop, file):
        characters = {}
        for i in range(start, stop):
            if "<div class=''>" in file[i]:
                character = file[i].split('>')
                character = character[1].split(':')
                characters[character[0]] = character[1]

        return characters

    def choose_product_id(self, start, file):
        for i in range(start, len(file)):
            id = re.findall(r'<a href=\'/store.aspx\?', file[i])
            if len(id) != 0:
                id = re.findall(r'&id=[0-9]+', file[i])
                return id[0]

    def set_product_addr(self, start, file, addr):
        id = self.choose_product_id(start, file)
        addr = addr.split('&')
        product_addr = str()
        product_addr = addr[0] + id

        return product_addr

    def choose_product_description(self, productAddr):
        fileName = 'product.html'
        self.get_page(productAddr, fileName)
        file = open(fileName, 'r')
        parseFile = file.readlines()
        file.close()

        stop = False

        for i in range(len(parseFile)):
            description = re.findall(r'<div itemprop=\'description\'', parseFile[i])
            if len(description) != 0:
                for j in range(i, len(parseFile)):
                    description = re.findall(r'<span style=', parseFile[j])
                    if len(description) != 0:
                        description = str()
                        for k in range(j, len(parseFile)):
                            if parseFile[k] == '</span>\n':
                                break
                            description = description + parseFile[k]
                        break
                break

        descriptionList = description.split('<br />')
        description = str()
        for i in range(len(descriptionList)):
            if '<span style="font-size: 16px;">' in descriptionList[i]:
                descriptionList[i] = descriptionList[i].split('>')
                descriptionList[i] = descriptionList[i][1]
            elif '&nbsp' in descriptionList[i]:
                descriptionString = str()
                for j in range(len(descriptionList[i])):
                    if descriptionList[i][j] not in ['&', 'n', 'b', 's', 'p', ';']:
                        descriptionString = descriptionString + descriptionList[i][j]
                if len(descriptionString) != 0:
                    descriptionList[i] = descriptionString
            description = description + descriptionList[i]

        return description

    def get_product_img(self, imgNameBig, imgNameSmall):
        fileName = 'product.html'
        file = open(fileName, 'r')
        parseFile = file.readlines()
        file.close()

        imgCount = 1
        imgName = []

        for i in range(len(parseFile)):
            img = re.findall(r'href=\"/foto/[0-9]+\w+\.jpg', parseFile[i])
            if len(img) != 0:
                img = re.findall(r'/foto/[0-9]+', img[0])

                addr = 'https://evateks.ru' + img + 'b.jpg'
                img = requests.get(addr)
                imgName = '../httpdocs/catalog/' + img + imgNameBig
                imgFile = open(imgName, 'wb')
                imgFile.write(img.content)
                imgFile.close()

                addr = ('https://evateks.ru' + img + 's.jpg')
                img = requests.get(addr)
                imgName = '../httpdocs/catalog/' + img + imgNameSmall
                imgFile = open(imgName, 'wb')
                imgFile.write(img.content)
                imgFile.close()

                imgCount = imgCount + 1

        return (imgCount, imgName)

    def get_manufacturer_id(self, characters):
        manufacturer = ''
        for i in range(len(characters)):
            if 'Бренд' in characters[i]:
                manufacturer = characters[i].split(':')
                manufacturer = manufacturer[1][1:]

        return manufacturer