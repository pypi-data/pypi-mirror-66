def getgdelt(year_start,month_start,day_start,year_end,month_end,day_end):
    import webbrowser

    url1 = 'http://data.gdeltproject.org/events/'
    url2 = '.export.CSV.zip'
    year = year_start
    month = month_start
    day = day_start
    num = 0
    gdeltlist = []
    while year < year_end + 1:
        if year < year_end:
            while month < 13:
                while month < 10:
                    while day < 32:
                        while day < 10:
                            url = url1 + str(year) + '0' + str(month) + '0' + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                        else:
                            url = url1 + str(year) + '0' + str(month) + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                    else:
                        month += 1
                        num += 1
                        day = 1
                else:
                    while day < 32:
                        while day < 10:
                            url = url1 + str(year)+ str(month) + '0' + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                        else:
                            url = url1 + str(year) + str(month) + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                    else:
                        month += 1
                        num += 1
                        day = 1
            else:
                year += 1
                month = 1
                day = 1
                num += 1

        else:
            if month < month_end:
                while month < 10 and month < month_end:
                    while day < 32:
                        while day < 10:
                            url = url1 + str(year) + '0' + str(month) + '0' + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                        else:
                            url = url1 + str(year) + '0' + str(month) + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                    else:
                        month += 1
                        num += 1
                        day = 1
                else:
                    while day < 32 and month < month_end:
                        while day < 10:
                            url = url1 + str(year) + str(month) + '0' + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                        else:
                            url = url1 + str(year) + str(month) + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                    else:
                        month += 1
                        num += 1
                        day = 1
            elif month == month_end:
                while month < 10 and month == month_end:
                    while day < day_end + 1:
                        while day < 10 and day < day_end + 1:
                            url = url1 + str(year) + '0' + str(month) + '0' + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                        else:
                            if day < day_end + 1:
                                url = url1 + str(year) + '0' + str(month) + str(day) + url2
                                gdeltlist.insert(num, url)
                                day += 1
                                num += 1
                                print(url)
                            else:
                                day += 1
                                num += 1
                    else:
                        month += 1
                        num += 1
                        day = 1
                else:
                    while day < day_end + 1 and day < day_end + 1 and month == month_end:
                        while day < 10:
                            url = url1 + str(year) + str(month) + '0' + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                        else:
                            url = url1 + str(year) + str(month) + str(day) + url2
                            gdeltlist.insert(num, url)
                            day += 1
                            num += 1
                            print(url)
                    else:
                        month += 1
                        num += 1
                        day = 1
            else:
                year += 1
                month = 1
                day = 1
                num += 1

    for webpage in gdeltlist:
        webbrowser.open(webpage)

def usegdelt(download_file_directory,output_file_directory):
    import pandas as pd
    import glob

    csv_list = glob.glob(download_file_directory + '/*.CSV')
    print('get %s CSV files' % len(csv_list))
    for i in csv_list:
        fr = open(i, 'r').read()
        with open(output_file_directory + '/gdelt.csv', 'a') as f:
            f.write(fr)
        print('sucess！')
    print('Done！')

    gdelt = gdelt = pd.read_csv(output_file_directory + '/gdelt.csv', '\t', error_bad_lines=False, header = None)
    gdelt.columns = ['GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate', 'Actor1Code', 'Actor1Name',\
                     'Actor1CountryCode', 'Actor1KnownGroupCode', 'Actor1EthnicCode', 'Actor1Religion1Code',\
                     'Actor1Religion2Code',	'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code',\
                     'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 'Actor2EthnicCode',\
                     'Actor2Religion1Code', 'Actor2Religion2Code', 'Actor2Type1Code', 'Actor2Type2Code',\
                     'Actor2Type3Code', 'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass',\
                     'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone', 'Actor1Geo_Type',\
                     'Actor1Geo_FullName', 'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_Lat',\
                     'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type', 'Actor2Geo_FullName',\
                     'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',\
                     'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode',\
                     'ActionGeo_ADM1Code', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED',\
                     'SOURCEURL']
    gdelt['AvgTone'] = gdelt['AvgTone'].astype(float)
    return gdelt
