#!/usr/bin/python

from pymongo import MongoClient
import json

# initialize globals
client = MongoClient()
db = client.DEC
pdfs = db.dec
records = {}

def datefixer(baddate):
    ascii = baddate.encode('ascii', 'ignore')
    trimmed = ascii.strip().strip('"')
    date_array = str.split(trimmed)
    day_array = date_array[0].split('/')
    time_array = date_array[1].split(':')
    ampm = date_array[2]
    mm = day_array[0] if len(day_array[0]) == 2 else '0' + day_array[0] 
    dd = day_array[1] if len(day_array[1]) == 2 else '0' + day_array[1] 
    yyyy = day_array[2]
    HH = time_array[0] if len(time_array[0]) == 2 else '0' + time_array[0] # first ensure leading zero
    HH = str(int(HH) + 12) if ampm == "PM" else HH # convert to military time
    MM = time_array[1] if len(time_array[1]) == 2 else '0' + time_array[1]
    SS = time_array[2] if len(time_array[2]) == 2 else '0' + time_array[2]
    fixed = "%s/%s/%s %s:%s:%s" %(mm,dd,yyyy,HH,MM,SS)
    return fixed


# get each record, check for Date Modified and Date Created, and make sure date format is mm/dd/yyyy HH:MM:SS
data = pdfs.find( {}, { "file_id":1, "xml_metadata.DateCreated":1, "xml_metadata.DateModified":1 })

counter = 0
for doc in data:
    id = doc["file_id"]
    date_created = datefixer( doc["xml_metadata"]["DateCreated"] )
    date_modified = datefixer( doc["xml_metadata"]["DateModified"] )

    #pdfs.update_many({"file_id" : file_id}, {"$set": { "xml_metadata.DateCreated": date_created, "xml_metadata.DateModified": date_modified} })
    counter += 1

print counter
