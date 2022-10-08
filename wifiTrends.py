import argparse
import math
import time
import os
import zipfile
import json
import pathlib
import shutil
import csv
from string import ascii_uppercase
from pprint import pprint

"""
Majority of script written by François Vergès, modified by Rowell Dionicio (@rowelldionicio)
https://rowelldionicio.com
Created on: October 7, 2022
Description: This Python python script was something put together quickly. It iterates through Ekahau files and creates
a CSV file with the following information, filename, AP name, channel, channel width, and protocol. 

A CSV file was created in advanced which contained the following headers: File, AP Name, Channel, Channel Width, Protocol
"""

CHANNELS = {
    "5180" : "36",
    "5200" : "40",
    "5220" : "44",
    "5240" : "48",
    "5260" : "52",
    "5280" : "56",
    "5300" : "60",
    "5320" : "64",
    "5500" : "100",
    "5520" : "104",
    "5540" : "108",
    "5560" : "112",
    "5580" : "116",
    "5600" : "120",
    "5620" : "124",
    "5640" : "128",
    "5660" : "132",
    "5680" : "136",
    "5700" : "140",
    "5720" : "144",
    "5745" : "149",
    "5765" : "153",
    "5785" : "157",
    "5805" : "161",
    "5825" : "165",
    "2412" : "1",
    "2437" : "6",
    "2462" : "11"
}

CHANNEL_W = {
    "1": "20",
    "2": "40",
    "4": "80"
}

PROTOCOL = {
    "['A', 'N', 'AC']" : "AC",
    "['A', 'AC', 'N']" : "AC",
    "['A']" : "A",
    "['A', 'N']" : "N",
    "['A', 'AX', 'N', 'AC']" : "AX"
}


def retreive_ap_information(survey_file: str):
    aps = []
    current_filename = pathlib.PurePath(survey_file).stem
    working_directory = os.getcwd()
    projectFile = survey_file


    # Load & Unzip the Ekahau Project File
    with zipfile.ZipFile(survey_file, 'r') as myzip:
        myzip.extractall(current_filename)

        # Load the accessPoints.json file into the accessPoints dictionary
        with myzip.open('accessPoints.json') as json_file:
            accessPoints = json.load(json_file)

        # Rowell's addition, Load measuredRadios.json file into measuredRadios dictionary
        with myzip.open('measuredRadios.json') as json_file:
            measuredRadios = json.load(json_file)

        # Rowell's addition, Load accessPointMeasurements.json file into the accessPointMeasurements dictionary
        with myzip.open('accessPointMeasurements.json') as json_file:
            accessPointMeasurements = json.load(json_file)

        # Loop through the AP to retreive Data

        for ap in accessPoints['accessPoints']:
            if ap['mine'] is True:
                for measuredRadio in measuredRadios['measuredRadios']:
                    if measuredRadio['accessPointId'] == ap['id']:
                        for measurement in accessPointMeasurements['accessPointMeasurements']:
                            if measurement['id'] == measuredRadio['accessPointMeasurementIds'][0]:
                                if (measurement['channelByCenterFrequencyDefinedNarrowChannels'][0]) >= 5000:
                                    channel = CHANNELS[str(measurement['channelByCenterFrequencyDefinedNarrowChannels'][0])]
                                    channel_width = CHANNEL_W[str(len(measurement['channelByCenterFrequencyDefinedNarrowChannels']))]
                                    protocol = PROTOCOL[str(measurement['technologies'])]
                                    apName = ap['name']
                            
                                    row = projectFile,apName,channel,channel_width,protocol
                                    trend_writer(row)
                                    

def trend_writer(row):
    with open('wifitrends.csv', 'a', newline='') as csvfile:
        trendwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL))
        trendwriter.writerow(row)

    #print(open('wifitrends.csv', 'rt').read())


def main():
    path = os.getcwd()
    files = os.listdir(path)
    for file in files:
        if file[-4:] == ".esx":
            aps = retreive_ap_information(file)
    


if __name__ == "__main__":
    start_time = time.time()
    print('** Creating trends...\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))
