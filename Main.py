#Working darksy version
import get_data
import ui
import Image
import io
from pprint import pprint
import datetime
import os
import calendar

def pil2ui(ui,imgIn):
    with io.BytesIO() as bIO:
        imgIn.save(bIO, 'PNG')
        imgOut = ui.Image.from_data(bIO.getvalue())
        del bIO
    return imgOut

def percent(input):
    return "{0:.0%}".format(input)

def vis(w,h):

    vis = {}
    vis['side_margin'] = 3
    vis['w_adjusted'] = w-vis['side_margin']
    vis['top_margin'] = 35
    vis['other_label_height'] = 32
    vis['spacing_margin'] = 0

    #Subview
    vis['subview_w'] = (w-(vis['side_margin']*4))/3#(w/3)-(vis['side_margin']*2)
    vis['subview_h'] = h-(vis['top_margin']*2.75) #this is whats actually used
    vis['subview_y'] = vis['top_margin']
    vis['subview_x'] = vis['side_margin']
    vis['subview_scroll_size_w'] = vis['subview_w']
    vis['subview_scroll_size_h'] = vis['subview_h'] * 1.25

    #Header
    vis['header_x'] = vis['side_margin'] * 2
    vis['header_y'] = vis['top_margin'] / 2
    vis['header_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['header_height'] = 70

    #Timeset View
    vis['timesetview_x'] = vis['header_x'] + (vis['side_margin'] * 2)
    vis['timesetview_y'] = vis['header_y'] + vis['header_height'] + vis['spacing_margin']
    vis['timesetview_width'] = vis['header_width'] - (vis['side_margin'] * 4) #w/3 - (vis['side_margin'] *8)
    vis['timesetview_height'] = vis['timesetview_width']

    #Image View
    vis['imageview_x'] = vis['header_x'] + (vis['side_margin'] * 2)
    vis['imageview_y'] = vis['header_y'] + vis['header_height'] + vis['spacing_margin']
    vis['imageview_width'] = vis['header_width'] - (vis['side_margin'] * 4) #w/3 - (vis['side_margin'] *8)
    vis['imageview_height'] = vis['imageview_width']

    #Title Labels
    vis['title_label_x'] = vis['side_margin']
    vis['title_label_y'] = vis['imageview_y']+(vis['imageview_height'])
    vis['title_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['title_label_height'] = vis['other_label_height']
    vis['title_label_margins'] = -1

    #Value Labels
    vis['value_label_x'] = vis['side_margin'] * 2
    vis['value_label_y'] = vis['imageview_y'] + (vis['imageview_height']) + (vis['other_label_height']/2)
    vis['value_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['value_label_height'] = vis['other_label_height']
    vis['value_label_margins'] = vis['title_label_margins']

    #Buttons
    vis['button_height'] = 32 #above button_y
    vis['button_y'] = h - vis['button_height'] - 15 #view height minus button height plus some
    vis['button_width'] = vis['header_width']

    #Text Size?
    vis['title_label_size'] = 14
    vis['value_label_size'] = 16
    vis['header_label_size'] = 16


    return vis

def eval_text_color(value,type):
    value = float(value)

    good = 'black'#'#006d17'
    not_good = 'white'#'#FCAB10'#'#e60000'
    okay = 'white'#"#ff884d"

    #TEMPERATURE
    if type == 'temp':
        if value < 20:
            status = 'Temp of '+str(value)+' is pretty cold'
            return not_good, status
        if value > 90:
            status = 'Temp of '+str(value)+' is pretty hot'
            return not_good
        else:
            return good,None

    if type == 'windchill':
        if value < 10:
            if value == -9999:
                return good,None
            status = 'Windchill of '+str(value)+' is damn cold'
            return not_good, status
        if value < 20:
            status = 'Windchill of '+str(value)+' is too cold'
            return not_good
        else:
            return good,None

    #PERCIPITATION
    if type == 'pop':
        if value == 0:
            status = 'Chance of precipitation '+str(value)+' is SUPER LOW'
            return good, status
        if value > 25:
            status = 'Chance of precipitation '+str(value)+' is kinda high'
            return okay, status
        if value > 50:
            status = 'Chance of precipitation '+str(value)+' is pretty high'
            return not_good, status
        else:
            return good,None
    #HUMIDITY
    if type == 'humidity':
        if value > 70:
            status = 'Humidity of '+str(value)+' is pretty high'
            return okay, status
        if value > 80:
            status = 'Humidity of '+str(value)+' is really high'
            return not_good, status
        else:
            return good,None

def evaluate_conditions(day):

    good = '#5cd65c'
    bad = '#F8333C'
    warning = "#FCAB10"
    bg_color = good
    warning_list = []
    bad_list = []

    #percent of rain chance
    if float(day['weather']['precipProbability']) > 60:
        bg_color = bad
        bad_list.append('precipProbability') #add to bad list
        return bg_color, bad_list, warning_list #return on bad
    if float(day['weather']['precipProbability']) > 30:
        warning_list.append('precipProbability')
        bg_color = warning

    #temperature
    if float(day['weather']['apparentTemperature']) < 9 or float(day['weather']['apparentTemperature']) > 90:
        bg_color = bad
        bad_list.append('apparentTemperature')
        return bg_color, bad_list, warning_list #return on bad
    if float(day['weather']['apparentTemperature']) < 20 or float(day['weather']['apparentTemperature']) > 80:
        warning_list.append('apparentTemperature')
        bg_color = warning

    return bg_color, bad_list, warning_list
    # #STATUS
    # #SNOW
    # if (int(day['weather']['fctcode']) >= 21 or #snowing
    #     int(day['weather']['fctcode']) == 19 or #show showers
    #     int(day['weather']['fctcode']) == 9 or #blowing snow
    #     int(day['weather']['fctcode']) == 16): #flurries
    #
    #     print("SNOW - eval_conditions")
    #     bg_color = not_good
    #     return bg_color
    #
    # #RAIN
    # if (int(day['weather']['fctcode']) == 11 or #Showers
    #     int(day['weather']['fctcode']) == 13): #Rain
    #     print("RAIN - eval_conditions")
    #     bg_color = not_good
    #     return bg_color
    #
    # if (int(day['weather']['fctcode']) == 14 or #Chance of TStorms
    #     int(day['weather']['fctcode']) == 15): #Thunderstorm
    #     print("TSTORMS - eval_conditions")
    #     bg_color = not_good
    #     return bg_color
    #
    # if (int(day['weather']['fctcode']) == 7 or #very hot
    #     int(day['weather']['fctcode']) == 8): #very cold
    #     print("Temp Extremes - eval_conditions")
    #     bg_color = okay
    #
    #
    # #TEMPERATURE
    # if float(day['weather']['feelslike']['english']) < 20 or float(day['weather']['feelslike']['english']) > 90:
    #     bg_color = not_good
    #     return bg_color #temp that extreme sends it
    #
    # if float(day['weather']['feelslike']['english']) < 20 or float(day['weather']['feelslike']['english']) > 90:
    #     bg_color = okay
    #
    # #PERCIPITATION
    # if float(day['weather']['pop']) > 50:
    #     bg_color = not_good
    #     return bg_color
    #
    # if float(day['weather']['pop']) > 25:
    #     bg_color = okay
    #
    # #HUMIDITY
    # if float(day['weather']['humidity']) > 70:
    #     bg_color = okay

def build_data(forecast_dict):
    for peroid in forecast_dict:
        for day in forecast_dict[peroid]:
            regular = 'black'#'#5cd65c'

            forecast_dict[peroid][day]['data'] = {}


            #BG and text eval
            forecast_dict[peroid][day]['bg_color'],bad_list,warning_list = evaluate_conditions(forecast_dict[peroid][day])

            print("Warning:")
            print(warning_list)
            print("Bad:")
            print(bad_list)
            #CONDITION
            forecast_dict[peroid][day]['data']['condition'] = {}
            forecast_dict[peroid][day]['data']['condition']['title'] = 'Condition:'
            forecast_dict[peroid][day]['data']['condition']['value'] = forecast_dict[peroid][day]['weather']['summary']#['condition']
            forecast_dict[peroid][day]['data']['condition']['text_color'] = regular

            #TEMPERATURE
            forecast_dict[peroid][day]['data']['temperature'] = {}
            forecast_dict[peroid][day]['data']['temperature']['title'] = 'Temp:'
            forecast_dict[peroid][day]['data']['temperature']['value'] = forecast_dict[peroid][day]['weather']['temperature']#['temp']['english']
            text_color = 'black' #eval_text_color(forecast_dict[peroid][day]['weather']['temp']['english'],'temp')
            forecast_dict[peroid][day]['data']['temperature']['text_color'] = text_color

            #REAL FEEL
            forecast_dict[peroid][day]['data']['real_feel'] = {}
            forecast_dict[peroid][day]['data']['real_feel']['title'] = 'Feels Like:'
            forecast_dict[peroid][day]['data']['real_feel']['value'] = forecast_dict[peroid][day]['weather']['apparentTemperature']#['feelslike']['english']
            if 'apparentTemperature' in warning_list:
                text_color = 'red'
            if 'apparentTemperature' in bad_list:
                text_color = 'red'
            else:
                text_color= 'black'
            forecast_dict[peroid][day]['data']['real_feel']['text_color'] = text_color

            #'precipType'
            forecast_dict[peroid][day]['data']['precipType'] = {}
            forecast_dict[peroid][day]['data']['precipType']['title'] = 'Precip Type:'
            try:
                forecast_dict[peroid][day]['data']['precipType']['value'] = forecast_dict[peroid][day]['weather']['precipType'].title()#capitalize
            except Exception:
                forecast_dict[peroid][day]['data']['precipType']['value'] = "N/A"
            forecast_dict[peroid][day]['data']['precipType']['text_color'] = text_color

            #POP
            forecast_dict[peroid][day]['data']['pop'] = {}
            forecast_dict[peroid][day]['data']['pop']['title'] = '% Precipitation:'
            forecast_dict[peroid][day]['data']['pop']['value'] = percent(forecast_dict[peroid][day]['weather']['precipProbability'])#['pop']
            if 'precipProbability' in warning_list:
                text_color = 'red'
            if 'precipProbability' in bad_list:
                text_color = 'red'
            else:
                text_color= 'black'
            forecast_dict[peroid][day]['data']['pop']['text_color'] = text_color

            #HUMIDITY
            forecast_dict[peroid][day]['data']['humidity'] = {}
            forecast_dict[peroid][day]['data']['humidity']['title'] = 'Humidity:'
            forecast_dict[peroid][day]['data']['humidity']['value'] = percent(forecast_dict[peroid][day]['weather']['humidity'])
            text_color = 'black' #eval_text_color(forecast_dict[peroid][day]['weather']['humidity'],'humidity')
            forecast_dict[peroid][day]['data']['humidity']['text_color'] = text_color

            # #DEWPOINT
            # forecast_dict[peroid][day]['data']['dewpoint'] = {}
            # forecast_dict[peroid][day]['data']['dewpoint']['title'] = 'Dewpoint:'
            # forecast_dict[peroid][day]['data']['dewpoint']['value'] = forecast_dict[peroid][day]['weather']['dewPoint']#['dewpoint']['english']
            # forecast_dict[peroid][day]['data']['dewpoint']['text_color'] = regular

            #UVI
            forecast_dict[peroid][day]['data']['uvi'] = {}
            forecast_dict[peroid][day]['data']['uvi']['title'] = 'UV Index:'
            forecast_dict[peroid][day]['data']['uvi']['value'] = forecast_dict[peroid][day]['weather']['uvIndex']
            forecast_dict[peroid][day]['data']['uvi']['text_color'] = regular

            #WINDSPEED
            forecast_dict[peroid][day]['data']['windspeed'] = {}
            forecast_dict[peroid][day]['data']['windspeed']['title'] = 'Wind Speed:'
            forecast_dict[peroid][day]['data']['windspeed']['value'] = forecast_dict[peroid][day]['weather']['windSpeed']#['wspd']['english']
            forecast_dict[peroid][day]['data']['windspeed']['text_color'] = regular

            #WINDGUST
            forecast_dict[peroid][day]['data']['windGust'] = {}
            forecast_dict[peroid][day]['data']['windGust']['title'] = 'Wind Gust:'
            forecast_dict[peroid][day]['data']['windGust']['value'] = forecast_dict[peroid][day]['weather']['windGust']#['wspd']['english']
            forecast_dict[peroid][day]['data']['windGust']['text_color'] = regular

            #'cloudCover'
            forecast_dict[peroid][day]['data']['cloudCover'] = {}
            forecast_dict[peroid][day]['data']['cloudCover']['title'] = 'Cloud Cover:'
            try:
                forecast_dict[peroid][day]['data']['cloudCover']['value'] = percent(forecast_dict[peroid][day]['weather']['cloudCover'])#.title()#capitalize
            except Exception:
                forecast_dict[peroid][day]['data']['cloudCover']['value'] = "N/A"
            text_color = 'black'
            forecast_dict[peroid][day]['data']['cloudCover']['text_color'] = text_color

            # #WINDCHILL
            # forecast_dict[peroid][day]['data']['windchill'] = {}
            # forecast_dict[peroid][day]['data']['windchill']['title'] = 'Windchill:'
            # forecast_dict[peroid][day]['data']['windchill']['value'] = forecast_dict[peroid][day]['weather']['apparentTemperature']
            # text_color,windchill_status = 'black', None# eval_text_color(forecast_dict[peroid][day]['weather']['windchill']['english'],'windchill')
            # forecast_dict[peroid][day]['data']['windchill']['text_color'] = text_color
            # if windchill_status != None: status_list.append(windchill_status)

            if peroid == 'AM':
                #Astro
                forecast_dict[peroid][day]['data']['astronomical_twilight'] = {}
                forecast_dict[peroid][day]['data']['astronomical_twilight']['title'] = 'Astro:'
                forecast_dict[peroid][day]['data']['astronomical_twilight']['value'] = forecast_dict[peroid][day]['twilight']['astronomical_twilight_begin_time']
                forecast_dict[peroid][day]['data']['astronomical_twilight']['text_color'] = regular

                #Nautical
                forecast_dict[peroid][day]['data']['nautical_twilight'] = {}
                forecast_dict[peroid][day]['data']['nautical_twilight']['title'] = 'Nautical:'
                forecast_dict[peroid][day]['data']['nautical_twilight']['value'] = forecast_dict[peroid][day]['twilight']['nautical_twilight_begin_time']
                forecast_dict[peroid][day]['data']['nautical_twilight']['text_color'] = regular

                #Civil
                forecast_dict[peroid][day]['data']['civil_twilight'] = {}
                forecast_dict[peroid][day]['data']['civil_twilight']['title'] = 'Civil:'
                forecast_dict[peroid][day]['data']['civil_twilight']['value'] = forecast_dict[peroid][day]['twilight']['civil_twilight_begin_time']
                forecast_dict[peroid][day]['data']['civil_twilight']['text_color'] = regular

                #sunrise
                forecast_dict[peroid][day]['data']['sunrise_time'] = {}
                forecast_dict[peroid][day]['data']['sunrise_time']['title'] = 'Sunrise:'
                forecast_dict[peroid][day]['data']['sunrise_time']['value'] = forecast_dict[peroid][day]['twilight']['sunrise_time']
                forecast_dict[peroid][day]['data']['sunrise_time']['text_color'] = regular

            if peroid == 'PM':

                forecast_dict[peroid][day]['data']['sunset_time'] = {}
                forecast_dict[peroid][day]['data']['sunset_time']['title'] = 'Sunset:'
                forecast_dict[peroid][day]['data']['sunset_time']['value'] = forecast_dict[peroid][day]['twilight']['sunset_time']
                forecast_dict[peroid][day]['data']['sunset_time']['text_color'] = regular

                #Civil
                forecast_dict[peroid][day]['data']['civil_twilight'] = {}
                forecast_dict[peroid][day]['data']['civil_twilight']['title'] = 'Civil:'
                forecast_dict[peroid][day]['data']['civil_twilight']['value'] = forecast_dict[peroid][day]['twilight']['civil_twilight_begin_time']
                forecast_dict[peroid][day]['data']['civil_twilight']['text_color'] = regular

                #Nautical
                forecast_dict[peroid][day]['data']['nautical_twilight'] = {}
                forecast_dict[peroid][day]['data']['nautical_twilight']['title'] = 'Nautical:'
                forecast_dict[peroid][day]['data']['nautical_twilight']['value'] = forecast_dict[peroid][day]['twilight']['nautical_twilight_begin_time']
                forecast_dict[peroid][day]['data']['nautical_twilight']['text_color'] = regular

                #Astro
                forecast_dict[peroid][day]['data']['astronomical_twilight'] = {}
                forecast_dict[peroid][day]['data']['astronomical_twilight']['title'] = 'Astro:'
                forecast_dict[peroid][day]['data']['astronomical_twilight']['value'] = forecast_dict[peroid][day]['twilight']['astronomical_twilight_begin_time']
                forecast_dict[peroid][day]['data']['astronomical_twilight']['text_color'] = regular


            #STATUS - bottom of the view
            # working_status = '\n'.join(status_list)
            # #working_status.append("\n".join(forecast_dict[peroid][day]['data']['status']))
            # forecast_dict[peroid][day]['data']['status'] = {}
            # forecast_dict[peroid][day]['data']['status']['title'] = '' #'Status:'
            # forecast_dict[peroid][day]['data']['status']['value'] = working_status
            # forecast_dict[peroid][day]['data']['status']['text_color'] = regular


    return forecast_dict

def headers(day,timeset,view_name):
    #Headers
    label_name = "header_"+str(view_name)
    header = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['header_x'], vis['header_y'], vis['header_width'], vis['header_height']))
    if timeset == 'AM':
        header.text_color = 'black'
        header.border_color = 'black'
        timeset = 'Morning'
    if timeset == 'PM':
        header.text_color = 'white'
        header.border_color = 'white'
        timeset = 'Afternoon'
    #header.border_color = 'white'
    #header.text_color = 'white'
    #header.tint_color = 'black'
    header.corner_radius = 15
    header.border_width = 5
    header.alignment = 1 #1 is center, 0 is left justified
    header.font = ('<system-bold>',vis['header_label_size'])
    header.number_of_lines = 3
    header.text = calendar.day_name[day['time'].weekday()]+"\n"+str(day['time'].hour)+":00\n"+timeset #['mon_abbrev']+" "+day['time']['mday']+"\n"+day['time']['weekday_name']+" "+day['time']['civil']

    return header

def gen_imageview(day,timeset,view_name):

    #Image View
    image_view_name = "imageview_"+str(view_name)
    imageview = ui.ImageView(name=image_view_name, bg_color='transparent', frame=(vis['imageview_x'], vis['imageview_y'], vis['imageview_width'], vis['imageview_height']))
    my_image_path = './resources/ds/'+ str(day['weather']['icon']) + ".png"
    my_image = Image.open(my_image_path)
    imageview.image = pil2ui(ui,my_image)
    #imageview.border_width = 1
    imageview.border_color = "grey"
    return imageview

    # #Headers
    # label_name = "header_"+str(view_name)
    # header = ui.Label(name = label_name, bg_color ='transparent', frame=(vis['imageview_x'], vis['imageview_y'], vis['imageview_width'], vis['imageview_height']))
    # if timeset == 'AM':
    #     header.text_color = 'black'
    #     header.border_color = 'black'
    # if timeset == 'PM':
    #     header.text_color = 'white'
    #     header.border_color = 'white'
    # #header.border_color = 'white'
    # #header.text_color = 'white'
    # #header.tint_color = 'black'
    # header.corner_radius = 15
    # header.border_width = 0
    # header.alignment = 1 #1 is center, 0 is left justified
    # header.font = ('<system-bold>',vis['header_label_size'])
    # header.number_of_lines = 3
    # header.text = str(day['weather']['summary'])#['mon_abbrev']+" "+day['time']['mday']+"\n"+day['time']['weekday_name']+" "+day['time']['civil']

    # return header


def gen_timeset_view(day,timeset,view_name):
    #Image View
    image_view_name = "timesetview_"+str(view_name)
    imageview = ui.ImageView(name=image_view_name, bg_color='transparent', frame=(vis['timesetview_x'], vis['timesetview_y'], vis['timesetview_width'], vis['timesetview_height']))
    my_image_path = './resources/'+ timeset + ".png"
    my_image = Image.open(my_image_path)
    imageview.image = pil2ui(ui,my_image)

    #imageview.border_width = 1
    imageview.border_color = "grey"

    return imageview

def gen_title_label(c,data,view_name):

    adjusted_label_y = vis['title_label_y'] +( c*( vis['other_label_height'] + vis['title_label_margins'] ) )
    c = c+1
    label_name = "tlabel"+str(view_name)+str(c)
    label = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['title_label_x'], adjusted_label_y, vis['title_label_width'], vis['title_label_height']))
    label.border_color = 'black'
    label.text_color = data['text_color']
    label.border_width = 0
    label.alignment = 0 #1 is center, #0 is left justified
    label.font = ('<system-bold>',vis['title_label_size'])
    label.number_of_lines = 1
    label.text = str(data['title'])
    return label

def gen_value_label(c,data,view_name):
    adjusted_label_y = vis['value_label_y'] +( c*(vis['value_label_height']+vis['title_label_margins']) )
    c = c+1
    label_name = "vlabel"+str(view_name)+str(c)
    if data['title'] == 'Status:' : #make status label taller
        label_height = vis['value_label_height'] * 4
        #vis['value_label_height'] = vis['value_label_height'] * 4
    else:
        label_height = vis['value_label_height']
    label = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['value_label_x'], adjusted_label_y, vis['value_label_width'], label_height))
    label.text_color = data['text_color']
    label.border_width = 0
    label.alignment = 3 #1 is center, #0 is left justified
    label.font = ('<system>',vis['value_label_size'])
    label.number_of_lines = 0
    label.text = str(data['value'])
    return label

def gen_status_label(c,data,view_name):
    adjusted_label_y = vis['value_label_y'] +( c*(vis['value_label_height']+vis['title_label_margins']) )
    c = c+1
    label_name = "vlabel"+str(view_name)+str(c)
    label = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['value_label_x'], adjusted_label_y, vis['value_label_width'], vis['value_label_height']))
    label.text_color = data['text_color']
    label.border_width = 0
    label.alignment = 3 #1 is center, #0 is left justified
    label.font = ('<system>',vis['value_label_size'])
    label.number_of_lines = 1
    label.text = str(data['value'])
    return label

def gen_switch_buttons(c,view_name):
    #Buttons
    button_x = vis['header_x'] + vis['side_margin'] + ( ( vis['w_adjusted'] / 3 ) * (c-1)) #has to be dynamic
    button_name = "button_"+str(view_name)
    button = ui.Button(name = button_name, bg_color ='white', frame = (button_x, vis['button_y'], vis['button_width'], vis['button_height']))
    button.border_color = 'black'
    button.tint_color = 'blue'
    button.border_width = 1
    button.alignment = 1 #1 is center, 0 is left justified
    button.font = ('<system>',12)
    button.number_of_lines = 1
    button.title = "AM/PM"
    return button

def switch_pressed(self):
    #print ("Pressed "+self.name)
    if "am" in self.name: #passed name like button_AM1
        #print("Button pressed and AM displayed")
        view_name = self.name.replace("button_","")
        view_number = view_name.replace("am","")
        new_view_name = "pm"+view_number
        view.remove_subview(view_dict[view_name]) #view_dict contains names as keys and view objects as values
        view.remove_subview(self) #remove button
        view.add_subview(view_dict[new_view_name])

        #add back button with PM name
        button = gen_switch_buttons(int(view_number),new_view_name) #pass cycle number, view name(data), vis library and ui element
        button.action = switch_pressed
        view.add_subview(button)

    if "pm" in self.name:
        #print("Button pressed and PM displayed")
        view_name = self.name.replace("button_","")
        view_number = view_name.replace("pm","")
        new_view_name = "am"+view_number
        view.remove_subview(view_dict[view_name]) #view_dict contains names as keys and view objects as values
        view.remove_subview(self) #remove button
        view.add_subview(view_dict[new_view_name])

        #add back button with PM name
        button = gen_switch_buttons(int(view_number),new_view_name) #pass cycle number, view name(data), vis library and ui element
        button.action = switch_pressed
        view.add_subview(button)

w,h = ui.get_screen_size()
view = ui.View(bg_color = 'white', frame = (0,0,w,h)) #main view

forecast_dict = get_data.forecast_me_2() #get actual data

am_count = len(forecast_dict['AM'])
pm_count = len(forecast_dict['PM'])
print("AM Count: "+str(am_count))
print("PM Count: "+str(pm_count))
print()


while am_count == 0 or pm_count == 0:
    print("Someone equals 0")
    os.remove('History.dict')
    forecast_dict = get_data.forecast_me()
    am_count = len(forecast_dict['AM'])
    pm_count = len(forecast_dict['PM'])
    print("AM Count: "+str(am_count))
    print("PM Count: "+str(pm_count))
    print()

forecast_dict = build_data(forecast_dict) #modify data

vis = vis(w,h)

#need to create 6 subviews
view_dict = {}

frame_1 = (vis['subview_x'], vis['subview_y'], vis['subview_w'], vis['subview_h'])
frame_2 = (vis['subview_x']*2 + vis['subview_w'], vis['subview_y'], vis['subview_w'], vis['subview_h'])
frame_3 = (vis['subview_x']*3 + vis['subview_w']*2, vis['subview_y'], vis['subview_w'], vis['subview_h'])

am_subview_list = []
bg_color = 'black'#'#5cd65c'
am1 = ui.View(title='am1', frame=frame_1, background_color = bg_color,\
        corner_radius = 10, content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
am2 = ui.View(title='am2', frame=frame_2, background_color = bg_color, \
        corner_radius = 10, content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
am3 = ui.View(title='am3', frame=frame_3, background_color = bg_color, \
        corner_radius = 10, content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))

bg_color = 'black'#'#F8333C'
pm_subview_list = []
pm1 = ui.View(title='pm1', frame=frame_1, background_color = bg_color,\
        corner_radius = 10, content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
pm2 = ui.View(title='pm2', frame=frame_2, background_color = bg_color,\
        corner_radius = 10, content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
pm3 = ui.View(title='pm3', frame=frame_3, background_color = bg_color,\
        corner_radius = 10, content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))

am_subview_list.append(am1)
am_subview_list.append(am2)
am_subview_list.append(am3)

pm_subview_list.append(pm1)
pm_subview_list.append(pm2)
pm_subview_list.append(pm3)

#need this for the button_pressed function only
for x in am_subview_list:
    view_dict[x.title] = x
for x in pm_subview_list:
    view_dict[x.title] = x

# print()
# pprint(view_dict)
# print()

#AM
for working_subview,day in zip(am_subview_list,forecast_dict['AM']): #for each am day, build objects to add to subview and add them
    header = headers(forecast_dict['AM'][day],'AM',working_subview)
    working_subview.add_subview(header)
    #timeset_view = gen_timeset_view(forecast_dict['AM'][day],'AM',working_subview)
    #working_subview.add_subview(timeset_view)
    imageview = gen_imageview(forecast_dict['AM'][day],'AM',working_subview)
    working_subview.add_subview(imageview)
    bg_color = forecast_dict['AM'][day]['bg_color']#evaluate_conditions(forecast_dict['AM'][day])
    working_subview.background_color = bg_color

    for c,item in enumerate(forecast_dict['AM'][day]['data']):
        #if item != 'status':
            #title = gen_title_label()
        value_title = gen_title_label(c,forecast_dict['AM'][day]['data'][item],working_subview)
        value_label = gen_value_label(c,forecast_dict['AM'][day]['data'][item],working_subview)
        working_subview.add_subview(value_title)
        working_subview.add_subview(value_label)

    #BUTTONS
    #figure out number of view
    subview_name = str(working_subview.title)
    view_number = int(subview_name.replace("am",""))

    #pass to button creation
    button = gen_switch_buttons(view_number,working_subview.title) #pass cycle number, view name(data), vis library and ui element
    button.action = switch_pressed
    view.add_subview(button) #each view gets a button

#PM
for working_subview,day in zip(pm_subview_list,forecast_dict['PM']): #for each am day, build objects to add to subview and add them
    header = headers(forecast_dict['PM'][day],'PM',working_subview)
    working_subview.add_subview(header)
    #timeset_view = gen_timeset_view(forecast_dict['PM'][day],'AM',working_subview)
    #working_subview.add_subview(timeset_view)
    imageview = gen_imageview(forecast_dict['PM'][day],'PM',working_subview)
    working_subview.add_subview(imageview)
    bg_color = forecast_dict['PM'][day]['bg_color']#evaluate_conditions(forecast_dict['PM'][day])
    working_subview.background_color = bg_color

    for c,item in enumerate(forecast_dict['PM'][day]['data']):
        #if item != 'status':
            #title = gen_title_label()
        value_title = gen_title_label(c,forecast_dict['PM'][day]['data'][item],working_subview)
        value_label = gen_value_label(c,forecast_dict['PM'][day]['data'][item],working_subview)
        working_subview.add_subview(value_title)
        working_subview.add_subview(value_label)

if datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 17 :
    print()
    print('Time is after 5AM and before 5PM')
    print('Running different time operation')
    view.remove_subview(view['button_am1']) #remove first button
    view.remove_subview(view['button_am2']) #remove second button
    view.remove_subview(view['button_am3']) #remove third button
    view.add_subview(pm1) #add pm subview to first slot
    #move am1 to am2
    #and am 2 to am 3
    am2.frame=frame_3 #move frame
    am2.title = 'am3' #change title
    view_dict['am3'] = view_dict['am2'] #move in dictionary (button uses)

    am1.frame=frame_2
    am1.title = 'am2'
    view_dict['am2'] = view_dict['am1'] #then move 1 to 2
    #pprint(view_dict)

    #BUTTONS
    button = gen_switch_buttons(2,'am2') #generate second button
    button.action = switch_pressed
    view.add_subview(button)

    button = gen_switch_buttons(3,'am3') #generate third button
    button.action = switch_pressed
    view.add_subview(button)

    view.add_subview(am1) #add newly moved subviews
    view.add_subview(am2)

else:
    view.add_subview(am1)
    view.add_subview(am2)
    view.add_subview(am3)


view.present(style='sheet', hide_title_bar=True)
