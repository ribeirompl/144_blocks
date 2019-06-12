"""
Functions for reading/writing from/to configuration files

Author: Marco P. L. Ribeiro
Date: June 2019

MIT License
Copyright (c) 2019 Marco P. L. Ribeiro
"""

import os
import tkinter as tk
from configobj import ConfigObj

# Load activity linked to each block
def read_saved_plan(filename):
    config = ConfigObj(filename)

    block_linking = []
    for row in range(24):
        tempList=[]
        for col in range(6):
            tempList.append(config[str(row).zfill(2)][str(col)+'0'])
        block_linking.append(tempList)
    
    return block_linking

# Write the activity linked to each block
def write_saved_plan(filename,block_linking):
    config = ConfigObj()
    config.filename = './saved_plans/'+ filename + '.ini'

    for row in range(24):
        config[str(row).zfill(2)] = {}
        for col in range(6):
            config[str(row).zfill(2)][str(col)+'0'] = block_linking[row][col]
    
    config.write()

# Function for shrinking the selected icon for use in the block
def shrinkImage(filepath, size):
    import PIL
    from PIL import Image

    basewidth = size
    img = Image.open(filepath)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    filename = os.path.basename(filepath)
    img.save('./resized/'+filename)

    return './resized/'+filename

# Read the settings file
def read_settings_file(settings_filename, tk_master):
    config = ConfigObj(settings_filename)
    
    main_text_colour=config['appearance']['main_text_colour']
    select_window_text_colour=config['appearance']['select_window_text_colour']
    background_colour=config['appearance']['background_colour']
    foreground_colour=config['appearance']['foreground_colour']
    unlinked_colour=config['appearance']['unlinked_colour']

    SIZE_SETTING = int(config['appearance']['button_size'])

    acts = {}
    for act in config['activities']: # act = 'Sleep' etc.
        act_image = tk.PhotoImage(master=tk_master, file=shrinkImage(config['activities'][act]['icon'],SIZE_SETTING))
        acts[act] = dict({'icon':act_image, 'colour':config['activities'][act]['colour'], 'productive':config['activities'][act]['productive']})

    acts['-1'] = dict({'icon':tk.PhotoImage(master=tk_master, width=SIZE_SETTING, height=SIZE_SETTING), 'colour':unlinked_colour, 'productive':'False'})
    return ([main_text_colour, select_window_text_colour, background_colour, foreground_colour, unlinked_colour], 
    SIZE_SETTING, acts)

# Recreate the default settings file
def write_settings_file(settings_filename, tk_master):
    config = ConfigObj()
    config.filename = settings_filename
    
    config['appearance'] = {}
    config['appearance']['background_colour'] = '#3d3d3d'
    config['appearance']['foreground_colour'] = '#3d3d3d'
    config['appearance']['unlinked_colour'] = '#999999'
    config['appearance']['main_text_colour'] = '#ffffff'
    config['appearance']['select_window_text_colour'] = '#ffffff'
    config['appearance']['button_size'] = 10

    activities = {
        'Sleep' : {
            'icon' : "./icons/moon.png",
            'colour' : "#000075",
            'productive' : False    
        },
        'Work' : {
            'icon' : "./icons/work.png",
            'colour' : "#808000",
            'productive' : True
        },    
        'Break' : {
            'icon' : "./icons/clock.png",
            'colour' : "#f032e6",
            'productive' : False
        },
        'Planning' : {
            'icon' : "./icons/calendar.png",
            'colour' : "#800000",
            'productive' : True
        },
        'Exercise' : {
            'icon' : "./icons/run.png",
            'colour' : "#f58231",
            'productive' : False
        },
        'Read' : {
            'icon' : "./icons/book.png",
            'colour' : "#e6194b",
            'productive' : False
        },
        'Eat' : {
            'icon' : "./icons/cutlery.png",
            'colour' : "#3cb44b",
            'productive' : False
        },
        'Shower' : {
            'icon' : "./icons/shower.png",
            'colour' : "#4363d8",
            'productive' : False
        },
        'Movie' : {
            'icon' : "./icons/clapperboard.png",
            'colour' : "#911eb4",
            'productive' : False
        },
        'Hobby' : {
            'icon' : "./icons/painter_palette.png",
            'colour' : "#9a6324",
            'productive' : False
        }
    }

    config['activities'] = activities
    
    config.write()
