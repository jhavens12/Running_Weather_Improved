import credentials
import requests
from pprint import pprint
import datetime
import pickle
from pathlib import Path

wu_key = credentials.wu_key
my_lat = credentials.my_lat
my_long = credentials.my_long

UTC_adjust = datetime.timedelta(hours=4)

def open_file():
    dictionary_file = Path('./History.dict')
    if dictionary_file.is_file():
        pickle_in = open(dictionary_file,"rb")
        forecast_dict = pickle.load(pickle_in)
        #dictionary already has a timestamp key
    else:
        f=open(dictionary_file,"w+") #create file
        f.close()
        forecast_dict = {}
        forecast_dict['timestamp'] = datetime.datetime(1900, 1, 1)

    return forecast_dict

def close_file(forecast_dict):
    forecast_dict['timestamp'] = datetime.datetime.now()
    dictionary_file = Path('./History.dict')
    with open(dictionary_file, 'w') as outfile:
        #json.dump(history_dict, outfile)
        pickle_out = open(dictionary_file,"wb")
        pickle.dump(forecast_dict, pickle_out) #save old_dict as it has all of the data
        pickle_out.close()

def format_time(date_input,UTC_adjust,time):
    temp_date = date_input+" "+time
    datetime_object = datetime.datetime.strptime(temp_date, "%Y-%m-%d %I:%M:%S %p")
    return datetime_object - UTC_adjust

def nice_time(time):
    #return str(time.hour)+":"+str(time.minute)+":"+str(time.second)
    return str(time.time().strftime("%I:%M:%S"))

def twilight(date_input):
    sunrise_dict = {}
    url = "https://api.sunrise-sunset.org/json?lat="+my_lat+"&lng="+my_long+"&date="+date_input
    try:
        sunrise_data = requests.get(url).json()
    except:
        print("error getting astro data")

    sunrise_dict['astronomical_twilight_begin'] = format_time(date_input,UTC_adjust,sunrise_data['results']['astronomical_twilight_begin'])
    sunrise_dict['astronomical_twilight_begin_time'] = nice_time(sunrise_dict['astronomical_twilight_begin'])
    sunrise_dict['astronomical_twilight_end'] = format_time(date_input,UTC_adjust,sunrise_data['results']['astronomical_twilight_end'])
    sunrise_dict['astronomical_twilight_end_time'] = nice_time(sunrise_dict['astronomical_twilight_end'])

    sunrise_dict['nautical_twilight_begin'] = format_time(date_input,UTC_adjust,sunrise_data['results']['nautical_twilight_begin'])
    sunrise_dict['nautical_twilight_begin_time'] = nice_time(sunrise_dict['nautical_twilight_begin'])
    sunrise_dict['nautical_twilight_end'] = format_time(date_input,UTC_adjust,sunrise_data['results']['nautical_twilight_end'])
    sunrise_dict['nautical_twilight_end_time'] = nice_time(sunrise_dict['nautical_twilight_end'])

    sunrise_dict['civil_twilight_begin'] = format_time(date_input,UTC_adjust,sunrise_data['results']['civil_twilight_begin'])
    sunrise_dict['civil_twilight_begin_time'] = nice_time(sunrise_dict['civil_twilight_begin'])
    sunrise_dict['civil_twilight_end'] = format_time(date_input,UTC_adjust,sunrise_data['results']['civil_twilight_end'])
    sunrise_dict['civil_twilight_end_time'] = nice_time(sunrise_dict['civil_twilight_end'])

    sunrise_dict['sunrise'] = format_time(date_input,UTC_adjust,sunrise_data['results']['sunrise'])
    sunrise_dict['sunrise_time'] = nice_time(sunrise_dict['sunrise'])
    sunrise_dict['sunset'] = format_time(date_input,UTC_adjust,sunrise_data['results']['sunset'])
    sunrise_dict['sunset_time'] = nice_time(sunrise_dict['sunset'])

    return sunrise_dict

def forecast_me():
    #forecast_dict = {}
    forecast_dict = open_file()
    current_timestamp = datetime.datetime.now()
    if forecast_dict['timestamp'] < current_timestamp-datetime.timedelta(hours=1):
        print("Gathering new information")

        forecast_dict = {} #reset the dictionary
        term = 'hourly10day'
        url = "http://api.wunderground.com/api/"+wu_key+"/"+term+"/q/VT/Essex.json"
        try:
            hforecast = requests.get(url).json()
        except:
            print("error getting weather data")

        forecast_dict['PM'] = {}
        forecast_dict['AM'] = {}

        for hour in hforecast['hourly_forecast']:
            if hour['FCTTIME']['hour_padded'] == '05':# or hour['FCTTIME']['hour_padded'] == '17': AM

                #if hour['FCTTIME']['weekday_name'] == 'Tuesday' or hour['FCTTIME']['weekday_name'] == 'Thursday':# or hour['FCTTIME']['weekday_name'] == 'Saturday':

                temp_date = hour['FCTTIME']['year'] +"-"+ hour['FCTTIME']['mon'] +"-"+ hour['FCTTIME']['mday']
                temp_time = hour['FCTTIME']['hour_padded'] +":"+ hour['FCTTIME']['min']+":"+"00"
                date_key = datetime.datetime.strptime(temp_date+" "+temp_time, '%Y-%m-%d %H:%M:%S')
                if date_key < current_timestamp + datetime.timedelta(days=3): #if date is within three days

                    forecast_dict['AM'][date_key] = {}
                    forecast_dict['AM'][date_key]['twilight'] = twilight(temp_date)
                    forecast_dict['AM'][date_key]['time'] = hour['FCTTIME']
                    forecast_dict['AM'][date_key]['weather'] = hour


            if hour['FCTTIME']['hour_padded'] == '17':

                #if hour['FCTTIME']['weekday_name'] == 'Tuesday' or hour['FCTTIME']['weekday_name'] == 'Thursday':# or hour['FCTTIME']['weekday_name'] == 'Saturday':

                temp_date = hour['FCTTIME']['year'] +"-"+ hour['FCTTIME']['mon'] +"-"+ hour['FCTTIME']['mday']
                temp_time = hour['FCTTIME']['hour_padded'] +":"+ hour['FCTTIME']['min']+":"+"00"
                date_key = datetime.datetime.strptime(temp_date+" "+temp_time, '%Y-%m-%d %H:%M:%S')

                if date_key < current_timestamp + datetime.timedelta(days=3): #if date is within three days

                    forecast_dict['PM'][date_key] = {}
                    forecast_dict['PM'][date_key]['twilight'] = twilight(temp_date)
                    forecast_dict['PM'][date_key]['time'] = hour['FCTTIME']
                    forecast_dict['PM'][date_key]['weather'] = hour


        close_file(forecast_dict) #save the dictionary
        del forecast_dict['timestamp'] #delete timestamp after saving, before passing along
        return forecast_dict

    else:
        del forecast_dict['timestamp'] #delete timestamp so it does not interfere
        return forecast_dict

    #dont print
