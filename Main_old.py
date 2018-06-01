import get_data
import ui
import build
from pprint import pprint
import datetime


w,h = ui.get_screen_size()
view = ui.View(bg_color = 'white', frame = (0,0,w,h)) #main view

forecast_dict = get_data.forecast_me() #get actual data
#pprint(forecast_dict)

def switch_pressed(self):
    #print ("Pressed "+self.name)
    if "AM" in self.name: #passed name like button_AM1
        #print("Button pressed and AM displayed")
        view_name = self.name.replace("button_","")
        view_number = view_name.replace("AM","")
        new_view_name = "PM"+view_number
        view.remove_subview(view_dict[view_name]) #view_dict contains names as keys and view objects as values
        view.remove_subview(self) #remove button
        view.add_subview(view_dict[new_view_name])

        #add back button with PM name
        button = build.switch_buttons(int(view_number),new_view_name,vis,ui) #pass cycle number, view name(data), vis library and ui element
        button.action = switch_pressed
        view.add_subview(button)

    if "PM" in self.name:
        #print("Button pressed and PM displayed")
        view_name = self.name.replace("button_","")
        view_number = view_name.replace("PM","")
        new_view_name = "AM"+view_number
        view.remove_subview(view_dict[view_name]) #view_dict contains names as keys and view objects as values
        view.remove_subview(self) #remove button
        view.add_subview(view_dict[new_view_name])

        #add back button with PM name
        button = build.switch_buttons(int(view_number),new_view_name,vis,ui) #pass cycle number, view name(data), vis library and ui element
        button.action = switch_pressed
        view.add_subview(button)

def first_run(forecast_dict,view):
    am_count = len(forecast_dict['AM'])
    pm_count = len(forecast_dict['PM'])
    print("AM Count: "+str(am_count))
    print("PM Count: "+str(pm_count))
    print()
    panel_count = 3 #limit to 3 panels regardless
    global vis
    if pm_count <= am_count:
        vis = build.vis(w,h,panel_count)
    if pm_count > am_count or datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 17 : #copy first PM key to AM key in case there is not an AM key to use
        PM_KEY = list(forecast_dict['PM'].keys())[0] #this is the correct key
        forecast_dict['AM'][PM_KEY] = forecast_dict['PM'][PM_KEY] #move from pm to AM?
        vis = build.vis(w,h,panel_count)


    #create view dictionary
    global view_dict
    view_dict = {}

    for n,day in enumerate(sorted(forecast_dict['AM'])): #create AM views
        d = n+1
        q = 'AM'+str(d)
        view_dict[q] = build.subviews(n,vis,ui,forecast_dict['AM'][day]) #build dictionary
        header = build.headers(n,vis,ui,forecast_dict['AM'][day],view_dict[q],'AM') #n, vis dict, ui object, day info, view_name
        imageview = build.imageview_local(n,vis,ui,forecast_dict['AM'][day],view_dict[q])
        view_dict[q].add_subview(imageview)
        if day.hour < 10: #if the hour is truly AM time
            title_label_list,value_label_list = build.AM_titles_and_values(forecast_dict['AM'][day])
            build.title_labels(n,vis,ui,view_dict[q],title_label_list,'AM')
            build.value_labels(n,vis,ui,view_dict[q],value_label_list,'AM')
        else: #if the time is PM time but has been copied to AM time (since there is no AM time for that day)
            title_label_list,value_label_list = build.PM_titles_and_values(forecast_dict['PM'][day])
            build.title_labels(n,vis,ui,view_dict[q],title_label_list,'PM')
            build.value_labels(n,vis,ui,view_dict[q],value_label_list,'PM')
            header.text_color = 'white' #change to white to match PM
            header.border_color = 'white' #change to white to match PM
            #view_dict[q].background_color = "#0952c6"
        view_dict[q].add_subview(header)

    for n,day in enumerate(forecast_dict['PM']): #Create PM Views
        d = n+1
        q = 'PM'+str(d)
        view_dict[q] = build.subviews(n,vis,ui,forecast_dict['PM'][day]) #build dictionary
        #view_dict[q].background_color = "#0952c6" #change for PM
        header = build.headers(n,vis,ui,forecast_dict['PM'][day],view_dict[q],'PM') #n, vis dict, ui object, day info, view_name
        view_dict[q].add_subview(header)
        imageview = build.imageview_local(n,vis,ui,forecast_dict['PM'][day],view_dict[q])
        view_dict[q].add_subview(imageview)
        title_label_list,value_label_list = build.PM_titles_and_values(forecast_dict['PM'][day])
        build.title_labels(n,vis,ui,view_dict[q],title_label_list,'PM')
        build.value_labels(n,vis,ui,view_dict[q],value_label_list,'PM')

    for c,subview in enumerate(view_dict):
        if "AM1" in subview or "AM2" in subview or "AM3" in subview: #limit to 3?
            view.add_subview(view_dict[subview])
            d = c+1 #start with button 1, not 0
            button = build.switch_buttons(d,subview,vis,ui) #pass cycle number, view name(data), vis library and ui element
            button.action = switch_pressed
            view.add_subview(button) #each view gets a button

first_run(forecast_dict,view)

view.present(style='sheet', hide_title_bar=True)
