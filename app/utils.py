# -*- coding: utf-8 -*-

import calendar
import csv
import datetime as dt

"""
This script allows to clean up the datasets
It is meant to be used once. Once the data is cleared, you must not need to use it again
"""

def juliandate_to_YYYYMMDD(y,jd,time):
    """This function tranforms julian date (yyyy-julianday) to yyyy-mm-dd date format
    Keyword arguments:
    y -- the year of the date to transform
    jd -- the julian day of the date to transform
    time -- the time of the date to transform, if known, else, type '00:00'
    time is a string 'hh:mm'
    """

    month = 1
    day = 0
    datetime = ''
    while jd - calendar.monthrange(y,month)[1] > 0 and month <= 12:
        jd = jd - calendar.monthrange(y,month)[1]
        month = month + 1

    # If the month is less than 10 and it misses a 0 from the CSV file format
    if len(str(month)) != 2:
        # Then we add the missing zero
        month = '0' + str(month)

    # Same for the day
    if len(str(jd)) != 2:
        jd = '0' + str(jd)

    datetime = str(y) + '-' + str(month) + '-' + str(jd) + ' ' + time
    return (datetime)


def DDMMYYYY_to_YYYYMMDD(date):
    """ This function tranforms a date from dd-mm-yyyy format to yyyy-mm-dd format
    Keyword arguments:
    date -- The date to transform (string)
    """

    # We split the date using the '/' caracter
    elt = date.split('/')
    mm = str(elt[1])
    dd = str(elt[0])
    yyyy = str(elt[2])

    # If the year part misses its 2 first numbers, we add them
    if len(yyyy) !=4:
        if yyyy[0] == '0' or yyyy[0] == '1':
            yyyy = '20' + yyyy
        else:
            yyyy = '19' + yyyy

    # If we know more than the year in the date
    if len(elt)>1:
        # If day and month parts miss a 0, we add it
        if len(mm) != 2:
            mm = '0' + mm
        if len(dd) != 2:
            dd = '0' + dd

        new_date = str(yyyy) + '-' + mm  + '-' + dd
        return(new_date)


def MMDDYYYY_to_YYYYMMDD(date):
    """ This function tranforms a date from mm-dd-yyyy format to yyyy-mm-dd format
    Keyword arguments:
    date -- The date to transform (string)
    """
    # We split the date using the '/' caracter
    elt = date.split('/')
    dd = str(elt[1])
    mm = str(elt[0])
    yyyy = str(elt[2])

    # If the year part misses its 2 first numbers, we add them
    if len(yyyy) !=4:
        if yyyy[0] == '8' or yyyy[0] == '9':
            yyyy = '19' + yyyy
        elif yyyy[0] == '0' or yyyy[0] == '1':
            yyyy = '20' + yyyy

    # If we know more than the year in the date
    if len(elt)>1:
        # If day and month parts miss a 0, we add it
        if len(mm) != 2:
            mm = '0' + mm
        if len(dd) != 2:
            dd = '0' + dd

        new_date = yyyy + '-' + mm  + '-' + dd
        return(new_date)

def year_to_YYYYMMDD(year):
    """ This function tranforms a date from yyyy format to yyyy-mm-dd format
    Keyword arguments:
    year -- The year to transform (string)
    """

    # If we only have the year, we put the datetime at the first day of the first month of the year
    # Time: 00:00
    if len(year) == 4 and year.find('-') == -1:
        new_date = str(year) + '-01-01 00:00'
        return (new_date)

    else:
        return None



def run_cone(input_file, output_file):
    """ This function cleans up a input cone shp file and write it in an given output_file
    Keyword arguments:
    input_file -- The input file to clean 
    output_file -- The location of the output file
    """

    # We open the output file and write the corresponding header
    writer = csv.writer(open(output_file, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['cone_id', 'name', 'accretion_date', 'info_date', 'classe_bona', 'author'])

    # We open the input file
    with open(input_file, 'r', encoding='ISO-8859-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in spamreader:
            i += 1
            # If we're not reading the header
            if i > 1:
                # We store the shapefile attributes in variables and eventually transform them
                cone_id = row[5]
                name = row[0]
                author = row[1]
                accretion_date = year_to_YYYYMMDD(row[2])
                info_date = row[3]
                classe_bona = row[4]
                # Before writing them in the output_file
                writer.writerow([cone_id, name, accretion_date, info_date, classe_bona, author])


def run_fissure(input_file, output_file):
    """ This function cleans up a input fissure shp file and write it in an given output_file
    Keyword arguments:
    input_file -- The input file to clean 
    output_file -- The location of the output file
    """

    # We open the output file and write the corresponding header
    writer = csv.writer(open(output_file, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['fissure_id', 'opentime', 'opentime_unc', 'com', 'com4', 'com5'])

    # We open the input file
    with open(input_file, 'r', encoding='ISO-8859-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in spamreader:
            i += 1
            # If we're not reading the header
            if i > 1:
                # We store the shapefile attributes in variables and eventually transform them
                fissure_id = row[0]
                com = row[4]
                com4 = row[10]
                com5 = row[12]

                opentime_unc = None
                # If we have a clue of the end time, we store it in the opentime_unc field
                if len(row[3]) > 1:
                    opentime_unc = DDMMYYYY_to_YYYYMMDD(row[3])+ ' 00:00'

                # If we have the whole date or only the year for the opentime in com3 field
                if len(row[11]) > 1 and len(row[11]) != 4:
                    opentime = DDMMYYYY_to_YYYYMMDD(row[11])+ ' 00:00'
                elif len(row[11]) > 1 and  len(row[11]) == 4:
                    opentime = year_to_YYYYMMDD(row[11])

                # If the year data is stored in any other commentary field
                elif len(row[11]) == 0 and len(row[13]) > 1:
                    opentime = year_to_YYYYMMDD(row[13])
                elif len(row[11]) == 0 and len(row[13]) == 0 and len(row[14]) > 1:
                    opentime = year_to_YYYYMMDD(row[14])
                elif len(row[11]) == 0 and len(row[13]) == 0 and len(row[14]) == 0:
                    opentime = ''
                writer.writerow([fissure_id, opentime, opentime_unc, com, com4, com5])


def run(input_file, output_file):
    """ This function cleans up an input Genevieve table csv file and write it in an given output_file
    Keyword arguments:
    input_file -- The input file to clean 
    output_file -- The location of the output file
    """
    # We open the output file and write the corresponding header
    writer = csv.writer(open(output_file, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['F', 'event_date', 'ed_stime', 'ed_etime', 'com', 'Nf', 'vol', 'flux', 'sd_stime', 'sd_etime'])

    # We open the input file
    with open(input_file, 'r', encoding='ISO-8859-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in spamreader:
            i += 1
            # If we're not reading one of the tree headerq
            if i > 3:
                datetime = row[2].split('.')
                datetime2 = row[11].split('.')
                sd_time = row[13].split(':')

  
                F = row[0]

                # If the event date exists, we convert it
                if len(row[1]) > 1:
                    event_date = MMDDYYYY_to_YYYYMMDD(row[1]) + ' 00:00' 
                else:
                    event_date=''

                # If the eruption start time is defined
                if len(datetime) != 1:   
                    ed_stime = juliandate_to_YYYYMMDD(int(datetime[0]), int(datetime[1]), str(row[3]))        

                # We put the eruption end time to the correct format
                if len(row[4]) > 1:
                    ed_parsed_etime = row[4].split('/')
                    mm = ed_parsed_etime[1]
                    yyyy = ed_parsed_etime[2]
                    if len(yyyy) !=4:
                        if yyyy[0] == '8' or yyyy[0] == '9':
                            yyyy = '19' + yyyy
                        elif yyyy[0] == '0' or yyyy[0] == '1':
                            yyyy = '20' + yyyy
                    ed_correct_etime = ed_parsed_etime[0] + '/' + mm + '/' + yyyy
                    ed_etime = DDMMYYYY_to_YYYYMMDD(ed_correct_etime) + ' ' + row[5]
                else:
                    ed_etime = ''

                # We store the csv attributes in variables and eventually transform them
                notes = row[7]
                Nf = row[8]
                vol = row[9]
                flux = row[10]

                if Nf == '':
                   Nf = None 

                if vol == '':
                   vol = None

                if flux == '':
                   flux = None

                # If the seismic crises start time is defined
                if len(datetime2) != 1:
                    sd_stime = juliandate_to_YYYYMMDD(int(datetime2[0]), int(datetime2[1]), str(row[12]))
                    date = sd_stime.split(' ')[0]
                    sd_date = date.split('-')
                    stime = row[12].split(':')
                    # If we have both the start date and time
                    if len(sd_time) != 1 and len(stime) != 1:
                        sd_etime = str(dt.datetime(int(sd_date[0]), int(sd_date[1]), int(sd_date[2]), int(stime[0]), int(stime[1])) + dt.timedelta(hours=int(sd_time[0]), minutes=int(sd_time[1])))

                writer.writerow([F, event_date, ed_stime, ed_etime, notes, Nf, vol, flux, sd_stime, sd_etime])


