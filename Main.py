import get_data
import ui
import build
from pprint import pprint
import datetime

w,h = ui.get_screen_size()
view = ui.View(bg_color = 'white', frame = (0,0,w,h)) #main view

#forecast_dict = get_data.forecast_me() #get actual data

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

    #Header
    vis['header_x'] = vis['side_margin'] * 2
    vis['header_y'] = vis['top_margin'] / 2
    vis['header_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['header_height'] = 70

    #Image View
    vis['imageview_x'] = vis['header_x'] + (vis['side_margin'] * 2)
    vis['imageview_y'] = vis['header_y'] + vis['header_height'] + vis['spacing_margin']
    vis['imageview_width'] = vis['header_width'] - (vis['side_margin'] * 4) #w/3 - (vis['side_margin'] *8)
    vis['imageview_height'] = vis['imageview_width']

    #Title Labels
    vis['title_label_x'] = vis['side_margin']
    vis['title_label_y'] = vis['imageview_y']+vis['imageview_height']
    vis['title_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['title_label_height'] = vis['other_label_height']
    vis['title_label_margins'] = -1

    #Value Labels
    vis['value_label_x'] = vis['side_margin'] * 2
    vis['value_label_y'] = vis['imageview_y'] + vis['imageview_height'] + (vis['other_label_height']/2)
    vis['value_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['value_label_height'] = vis['other_label_height']
    vis['value_label_margins'] = vis['title_label_margins']

    #Buttons
    vis['button_height'] = 32 #above button_y
    vis['button_y'] = h - vis['button_height'] - 5 #view height minus button height plus some
    vis['button_width'] = vis['header_width']

    #Text Size?
    vis['title_label_size'] = 10
    vis['value_label_size'] = 11
    vis['header_label_size'] = 13


    return vis

vis = vis(w,h)

#need to create 6 subviews
am_1_subview = ui.View(frame=(vis['subview_x'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'black')
am_2_subview = ui.View(frame=((vis['subview_x']*2) + vis['subview_w'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'black')
am_3_subview = ui.View(frame=((vis['subview_x']*3) + (vis['subview_w']*2), vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'black')

pm_1_subview = ui.View(frame=(vis['subview_x'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'black')
pm_2_subview = ui.View(frame=((vis['subview_x']*2) + vis['subview_w'], vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'black')
pm_3_subview = ui.View(frame=((vis['subview_x']*3) + (vis['subview_w']*2), vis['subview_y'], vis['subview_w'], vis['subview_h']), background_color = 'black')

view.add_subview(am_1_subview)
view.add_subview(am_2_subview)
view.add_subview(am_3_subview)

view.present(style='sheet', hide_title_bar=True)
