#!/usr/bin/python

from pymongo import MongoClient
import xml.etree.ElementTree as ET

# initialize globals
client = MongoClient()
db = client.DEC
pdfs = db.dec
records = {}

# get all records
for event, elem in ET.iterparse('ost.xml'):
    if elem.tag == 'Record':
        property_values = {}
        for pv in elem.findall('.//PropertyValue'):
            name = pv.get('name')
            text = pv.text
            if name in property_values:
                # append current value to existing values
                if type(property_values[name]) == list:
                    property_values[name].append(text)
                else:
                    property_values[name] = [property_values[name], text]
            else:
                property_values[name] = text
        # add property values to records dictionary
        file_id = property_values['File'].split('/').pop().lower()
        records[file_id] = property_values

        # clear record to save memory
        elem.clear()

        # update record in database
        result = pdfs.update_many({"file_id" : file_id}, {"$set": { "xml_metadata": property_values} })

