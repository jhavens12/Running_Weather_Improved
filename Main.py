import get_data
import ui
#import build
import Image
import io
from pprint import pprint
import datetime

def pil2ui(ui,imgIn):
    with io.BytesIO() as bIO:
        imgIn.save(bIO, 'PNG')
        imgOut = ui.Image.from_data(bIO.getvalue())
        del bIO
    return imgOut

def vis(w,h):

    vis = {}
    vis['side_margin'] = 3
    vis['w_adjusted'] = w-vis['side_margin']
    vis['top_margin'] = 20
    vis['other_label_height'] = 32
    vis['spacing_margin'] = 0

    #Subview
    vis['subview_w'] = (w/3)-(vis['side_margin']*2)
    vis['subview_h'] = h-(vis['top_margin']*3) #this is whats actually used
    vis['subview_y'] = vis['top_margin']
    vis['subview_x'] = vis['side_margin']
    vis['subview_scroll_size_w'] = vis['subview_w']
    vis['subview_scroll_size_h'] = vis['subview_h'] * 1.1

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
    vis['imageview_y'] = vis['timesetview_y'] + vis['header_height'] + vis['spacing_margin']
    vis['imageview_width'] = vis['header_width'] - (vis['side_margin'] * 4) #w/3 - (vis['side_margin'] *8)
    vis['imageview_height'] = vis['imageview_width']

    #Title Labels
    vis['title_label_x'] = vis['side_margin']
    vis['title_label_y'] = vis['imageview_y']+(vis['imageview_height']/1.9)
    vis['title_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['title_label_height'] = vis['other_label_height']
    vis['title_label_margins'] = -1

    #Value Labels
    vis['value_label_x'] = vis['side_margin'] * 2
    vis['value_label_y'] = vis['imageview_y'] + (vis['imageview_height']/1.9) + (vis['other_label_height']/2)
    vis['value_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['value_label_height'] = vis['other_label_height']
    vis['value_label_margins'] = vis['title_label_margins']

    #Buttons
    vis['button_height'] = 32 #above button_y
    vis['button_y'] = h - vis['button_height'] - 5 #view height minus button height plus some
    vis['button_width'] = vis['header_width']

    #Text Size?
    vis['title_label_size'] = 14
    vis['value_label_size'] = 12
    vis['header_label_size'] = 16


    return vis

def eval_text_color(value,type):
    value = float(value)

    good = '#5cd65c'
    not_good = '#e60000'
    okay = 'black'#"#ff884d"

    if type == 'temp':
        if value < 20:
            status = 'Temp of '+str(value)+' is pretty cold'
            return not_good, status
        if value > 80:
            status = 'Temp of '+str(value)+' is pretty hot'
            return not_good
        else:
            return good,None

    if type == 'windchill':
        if value < 10:
            status = 'Windchill of '+str(value)+' is damn cold'
            return not_good, status
        if value < 20:
            status = 'Windchill of '+str(value)+' is too cold'
            return not_good
        else:
            return good,None

    if type == 'pop':
        if value == 0:
            status = 'Chance of precipitation '+str(value)+' is SUPER LOW'
            return good, status
        if value > 40:
            status = 'Chance of precipitation '+str(value)+' is kinda high'
            return okay, status
        if value > 60:
            status = 'Chance of precipitation '+str(value)+' is pretty high'
            return not_good, status
        else:
            return good,None

    if type == 'humidity':
        if value > 70:
            status = 'Humidity of '+str(value)+' is pretty high'
            return okay, status
        if value > 80:
            status = 'Humidity of '+str(value)+' is really high'
            return not_good, status
        else:
            return good,None

def build_data(forecast_dict):
    for peroid in forecast_dict:
        for day in forecast_dict[peroid]:
            regular = 'black'#'#5cd65c'

            forecast_dict[peroid][day]['data'] = {}
            status_list = []

            #CONDITION
            forecast_dict[peroid][day]['data']['condition'] = {}
            forecast_dict[peroid][day]['data']['condition']['title'] = 'Condition:'
            forecast_dict[peroid][day]['data']['condition']['value'] = forecast_dict[peroid][day]['weather']['condition']
            forecast_dict[peroid][day]['data']['condition']['text_color'] = regular

            #TEMPERATURE
            forecast_dict[peroid][day]['data']['temperature'] = {}
            forecast_dict[peroid][day]['data']['temperature']['title'] = 'Temp:'
            forecast_dict[peroid][day]['data']['temperature']['value'] = forecast_dict[peroid][day]['weather']['temp']['english']
            text_color,temperature_status = eval_text_color(forecast_dict[peroid][day]['weather']['temp']['english'],'temp')
            forecast_dict[peroid][day]['data']['temperature']['text_color'] = text_color
            if temperature_status != None: status_list.append(temperature_status)

            #REAL FEEL
            forecast_dict[peroid][day]['data']['real_feel'] = {}
            forecast_dict[peroid][day]['data']['real_feel']['title'] = 'Feels Like:'
            forecast_dict[peroid][day]['data']['real_feel']['value'] = forecast_dict[peroid][day]['weather']['feelslike']['english']
            text_color,real_feel_status = eval_text_color(forecast_dict[peroid][day]['weather']['temp']['english'],'temp')
            forecast_dict[peroid][day]['data']['real_feel']['text_color'] = text_color
            if real_feel_status != None: status_list.append(real_feel_status)

            #DEWPOINT
            forecast_dict[peroid][day]['data']['dewpoint'] = {}
            forecast_dict[peroid][day]['data']['dewpoint']['title'] = 'Dewpoint:'
            forecast_dict[peroid][day]['data']['dewpoint']['value'] = forecast_dict[peroid][day]['weather']['dewpoint']['english']
            forecast_dict[peroid][day]['data']['dewpoint']['text_color'] = regular

            #POP
            forecast_dict[peroid][day]['data']['pop'] = {}
            forecast_dict[peroid][day]['data']['pop']['title'] = '% Precipitation:'
            forecast_dict[peroid][day]['data']['pop']['value'] = forecast_dict[peroid][day]['weather']['pop']
            text_color,pop_status = eval_text_color(forecast_dict[peroid][day]['weather']['pop'],'pop')
            forecast_dict[peroid][day]['data']['pop']['text_color'] = text_color
            if pop_status != None: status_list.append(pop_status)

            #HUMIDITY
            forecast_dict[peroid][day]['data']['humidity'] = {}
            forecast_dict[peroid][day]['data']['humidity']['title'] = 'Humidity:'
            forecast_dict[peroid][day]['data']['humidity']['value'] = forecast_dict[peroid][day]['weather']['humidity']
            text_color,humidity_status = eval_text_color(forecast_dict[peroid][day]['weather']['humidity'],'humidity')
            forecast_dict[peroid][day]['data']['humidity']['text_color'] = text_color
            if humidity_status != None: status_list.append(humidity_status)

            #UVI
            forecast_dict[peroid][day]['data']['uvi'] = {}
            forecast_dict[peroid][day]['data']['uvi']['title'] = 'UV Index:'
            forecast_dict[peroid][day]['data']['uvi']['value'] = forecast_dict[peroid][day]['weather']['uvi']
            forecast_dict[peroid][day]['data']['uvi']['text_color'] = regular

            #WINDSPEED
            forecast_dict[peroid][day]['data']['windspeed'] = {}
            forecast_dict[peroid][day]['data']['windspeed']['title'] = 'Windspeed:'
            forecast_dict[peroid][day]['data']['windspeed']['value'] = forecast_dict[peroid][day]['weather']['wspd']['english']
            forecast_dict[peroid][day]['data']['windspeed']['text_color'] = regular

            #WINDCHILL
            forecast_dict[peroid][day]['data']['windchill'] = {}
            forecast_dict[peroid][day]['data']['windchill']['title'] = 'Windchill:'
            forecast_dict[peroid][day]['data']['windchill']['value'] = forecast_dict[peroid][day]['weather']['windchill']['english']
            text_color,windchill_status = eval_text_color(forecast_dict[peroid][day]['weather']['windchill']['english'],'windchill')
            forecast_dict[peroid][day]['data']['windchill']['text_color'] = text_color
            if windchill_status != None: status_list.append(windchill_status)

            #STATUS
            working_status = '\n'.join(status_list)
            #working_status.append("\n".join(forecast_dict[peroid][day]['data']['status']))

            forecast_dict[peroid][day]['data']['status'] = {}
            forecast_dict[peroid][day]['data']['status']['title'] = 'Status:'
            forecast_dict[peroid][day]['data']['status']['value'] = working_status
            forecast_dict[peroid][day]['data']['status']['text_color'] = regular

            if peroid == 'AM':
                #Astro
                forecast_dict[peroid][day]['data']['astronomical_twilight'] = {}
                forecast_dict[peroid][day]['data']['astronomical_twilight']['title'] = 'Astro Twilight:'
                forecast_dict[peroid][day]['data']['astronomical_twilight']['value'] = forecast_dict[peroid][day]['twilight']['astronomical_twilight_begin_time']
                forecast_dict[peroid][day]['data']['astronomical_twilight']['text_color'] = regular

                #Nautical
                forecast_dict[peroid][day]['data']['nautical_twilight'] = {}
                forecast_dict[peroid][day]['data']['nautical_twilight']['title'] = 'Nautical Twilight:'
                forecast_dict[peroid][day]['data']['nautical_twilight']['value'] = forecast_dict[peroid][day]['twilight']['nautical_twilight_begin_time']
                forecast_dict[peroid][day]['data']['nautical_twilight']['text_color'] = regular

                #Civil
                forecast_dict[peroid][day]['data']['civil_twilight'] = {}
                forecast_dict[peroid][day]['data']['civil_twilight']['title'] = 'Civil Twilight:'
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

    return forecast_dict

def headers(day,timeset,view_name):
    #Headers
    label_name = "header_"+str(view_name)
    header = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['header_x'], vis['header_y'], vis['header_width'], vis['header_height']))
    if timeset == 'AM':
        header.text_color = 'black'
        header.border_color = 'black'
    if timeset == 'PM':
        header.text_color = 'white'
        header.border_color = 'white'
    #header.border_color = 'white'
    #header.text_color = 'white'
    #header.tint_color = 'black'
    header.corner_radius = 15
    header.border_width = 5
    header.alignment = 1 #1 is center, 0 is left justified
    header.font = ('<system-bold>',vis['header_label_size'])
    header.number_of_lines = 3
    header.text = day['time']['mon_abbrev']+" "+day['time']['mday']+"\n"+day['time']['weekday_name']+" "+day['time']['civil']

    return header

def gen_imageview(day,timeset,view_name):
    #Image View
    image_view_name = "imageview_"+str(view_name)
    imageview = ui.ImageView(name=image_view_name, bg_color='transparent', frame=(vis['imageview_x'], vis['imageview_y'], vis['imageview_width'], vis['imageview_height']))
    my_image_path = './resources/mdi/'+ str(day['weather']['fctcode']) + ".png"
    my_image = Image.open(my_image_path)
    imageview.image = pil2ui(ui,my_image)

    #imageview.border_width = 1
    imageview.border_color = "grey"

    return imageview

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
    label = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['value_label_x'], adjusted_label_y, vis['value_label_width'], vis['value_label_height']))
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
    print ("Pressed "+self.name)
    if "am" in self.name: #passed name like button_AM1
        print("Button pressed and AM displayed")
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
        print("Button pressed and PM displayed")
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

forecast_dict = get_data.forecast_me() #get actual data
forecast_dict = build_data(forecast_dict) #modify data

vis = vis(w,h)

#need to create 6 subviews
view_dict = {}

am_subview_list = []
am1 = ui.ScrollView(title='am1', frame=(vis['subview_x'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'pink', content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
am2 = ui.ScrollView(title='am2', frame=((vis['subview_x']*2) + vis['subview_w'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'pink', content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
am3 = ui.ScrollView(title='am3', frame=((vis['subview_x']*3) + (vis['subview_w']*2), vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'pink', content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))

pm_subview_list = []
pm1 = ui.ScrollView(title='pm1', frame=(vis['subview_x'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'blue', content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
pm2 = ui.ScrollView(title='pm2', frame=((vis['subview_x']*2) + vis['subview_w'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'blue', content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))
pm3 = ui.ScrollView(title='pm3', frame=((vis['subview_x']*3) + (vis['subview_w']*2), vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'blue', content_size = (vis['subview_scroll_size_w'], vis['subview_scroll_size_h']))

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

#Compenstation if time is after 5AM, need to display the PM subview instead of tomorrows AM subview
#Basically cut off one of the AM subviews, and only show two


#AM
for working_subview,day in zip(am_subview_list,forecast_dict['AM']): #for each am day, build objects to add to subview and add them
    header = headers(forecast_dict['AM'][day],'AM',working_subview)
    working_subview.add_subview(header)
    timeset_view = gen_timeset_view(forecast_dict['AM'][day],'AM',working_subview)
    working_subview.add_subview(timeset_view)
    imageview = gen_imageview(forecast_dict['AM'][day],'AM',working_subview)
    working_subview.add_subview(imageview)

    for c,item in enumerate(forecast_dict['AM'][day]['data']):
        if item != 'status':
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
    timeset_view = gen_timeset_view(forecast_dict['PM'][day],'AM',working_subview)
    working_subview.add_subview(timeset_view)
    imageview = gen_imageview(forecast_dict['PM'][day],'PM',working_subview)
    working_subview.add_subview(imageview)

    for c,item in enumerate(forecast_dict['PM'][day]['data']):
        if item != 'status':
            #title = gen_title_label()
            value_title = gen_title_label(c,forecast_dict['PM'][day]['data'][item],working_subview)
            value_label = gen_value_label(c,forecast_dict['PM'][day]['data'][item],working_subview)
            working_subview.add_subview(value_title)
            working_subview.add_subview(value_label)

if datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 17 :
    view.remove_subview(view['button_am1']) #remove first button
    view.remove_subview(view['button_am2']) #remove first button
    view.remove_subview(view['button_am3']) #remove first button
    view.add_subview(pm1) #add pm subview to first slot
    #move am1 to am2
    #and am 2 to am 3
    am2.frame=((vis['subview_x']*3) + (vis['subview_w']*2), vis['subview_y'], vis['subview_w'], vis['subview_h'])
    am2.title = 'am3'
     =  #move 2 to 3
    view_dict['am3'] = view_dict['am2']

    am1.frame=((vis['subview_x']*2) + vis['subview_w'], vis['subview_y'], vis['subview_w'], vis['subview_h'])
    am1.title = 'am2'
    view_dict['am2'] = view_dict['am1'] #then move 1 to 2
    pprint(view_dict)

    #BUTTONS
    button = gen_switch_buttons(2,'am2')
    button.action = switch_pressed
    view.add_subview(button)

    button = gen_switch_buttons(3,'am3')
    button.action = switch_pressed
    view.add_subview(button)

    view.add_subview(am1)
    view.add_subview(am2)

else:
    view.add_subview(am1)
    view.add_subview(am2)
    view.add_subview(am3)


view.present(style='sheet', hide_title_bar=True)
