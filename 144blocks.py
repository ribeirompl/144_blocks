"""
144 Blocks - Focused time planner
Inspiration from:   Tim Urban's (https://waitbutwhy.com/2016/10/100-blocks-day.html)
                    144blocks.com

Author: Marco P. L. Ribeiro
Date: June 2019

MIT License
Copyright (c) 2019 Marco P. L. Ribeiro
"""

import os
import subprocess
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from functools import partial

from read_write import read_settings_file, write_settings_file, read_saved_plan, write_saved_plan
from my_tkinter_settings import configure_window


class App:
    """Main Application for 144 Blocks"""
    def __init__(self, master, block_size, activities, colour_settings):
        """
        Parameters:
        -----------
            master : Tk object
            block_size : int
                Size of buttons (pixels), also used for font size
            activities :  {{icon : str of path,
                            colour : str,
                            productive : bool}}
                Dictionary (key is the activity name) of dictionaries containing the various activity details
            colour_settings : [col_txt_primary, col_txt_secondary, col_bg, col_fg, col_unlinked]
                List of colour appearance settings
        """
        
        self.master = master
        self.block_size = block_size
        self.acts = activities
        [self.col_txt_primary, self.col_txt_secondary, self.col_bg, self.col_fg, self.col_unlinked]  = colour_settings       
        self.img_blank_block = tk.PhotoImage(master=self.master,width=self.block_size,height=self.block_size)

        # link between activity and block: value is '-1' if unlinked, or the name of the activity
        self.block_linking = [['-1' for _ in range(6)] for _ in range(24)]

        configure_window(master=self.master, title="144 Blocks", width=170, height=610, resizable=True, centred=False, bg=self.col_bg)

        block_frame = tk.Frame(self.master, borderwidth=1, bg=self.col_bg)
        for i in range(7):
            block_frame.columnconfigure(i, pad=1)
        for i in range(25):
            block_frame.rowconfigure(i, pad=1)
        block_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=0, anchor=tk.N)
        
        # Horizontal time indicators at the top
        font_size_scaling = block_size*5//7
        for i in range(1,6):
            tk.Label(block_frame, text=":"+str(i)+"0", bg=self.col_bg, fg=self.col_txt_primary, font=("Courier", font_size_scaling)).grid(row=0, column=i, columnspan=2,pady=1)

        # Place the side time label, and the 6 buttons for each row
        self.btn = []
        for row in range(24):
            tk.Label(block_frame, text=str(row).zfill(2)+":00", bg=self.col_bg, fg=self.col_txt_primary, font=("Courier", font_size_scaling)).grid(row=row+1, column=0, pady=1)
            temp_list = []
            for col in range(6):
                btncolour = self.col_unlinked if self.block_linking[row][col] == '-1' else acts[self.block_linking[row][col]]['colour']
                btnimg = self.img_blank_block if self.block_linking[row][col] == '-1' else acts[self.block_linking[row][col]]['icon']
                
                temp_list.append(tk.Button(block_frame, bg=btncolour, activebackground=btncolour, image=btnimg, command=partial(self.display_activity_options_window, row, col), borderwidth=2,relief=tk.FLAT))
                temp_list[-1].grid(row=row+1,column=col+1, pady=1, padx=1, sticky=tk.E) #set recent element grid

            self.btn.append(temp_list)

        # Productive activity counter
        self.counter_var = tk.StringVar(self.master)
        self.counter_var.set("")
        self.counter_label = tk.Label(self.master, bg=self.col_bg, fg=self.col_txt_primary, textvariable=self.counter_var)
        self.counter_label.pack()
        
        # Settings button
        tk.Button(self.master, text="Settings", bg=self.col_fg, activebackground=self.col_fg, activeforeground=self.col_txt_primary, fg=self.col_txt_primary, command=self.display_save_load_window).pack(pady=10)

        # Edit checkbox
        self.check_var = tk.IntVar(self.master)
        cb = tk.Checkbutton(self.master, text="Edit", variable=self.check_var, bg=self.col_fg, activebackground=self.col_fg) 
        cb.config(fg=self.col_txt_primary, activeforeground=self.col_txt_primary, selectcolor=self.col_fg, command = self.toggle_display_setting)
        cb.pack()
        cb.select()

        # Load saved plans if available
        savedFilenamesOptions = os.listdir("./saved_plans/")
        if len(savedFilenamesOptions)==1:
            saved_filename = "./saved_plans/" + savedFilenamesOptions[0]
            self.block_linking = read_saved_plan(saved_filename)
            self.update_block_edit_display(self.block_linking, self.acts)
            messagebox.showinfo("Loaded Plan","Loaded " + savedFilenamesOptions[0])
        elif len(savedFilenamesOptions)==0:
            pass
        else:
            self.display_save_load_window()

    # Update the block colours and icons for editing mode
    def update_block_edit_display(self, block_linking, acts):
        for row in range(24):
            for col in range(6):
                if block_linking[row][col] == '-1':
                    btncolour=self.col_unlinked
                    btnimg=self.img_blank_block
                else:
                    btncolour=acts[block_linking[row][col]]['colour']
                    btnimg=acts[block_linking[row][col]]['icon']

                self.btn[row][col].config(bg=btncolour, activebackground=btncolour, image=btnimg)

    # Update the block colours and icons for time mode (black blocks indicate past activity)
    def update_block_time_display(self, block_linking, acts):
        num_blocks = self.curBlocks()
        changed = False
        for row in range(24):
            for col in range(6):
                if row*6+col+1 <= num_blocks:
                    btncolour='#000000'
                    btnimg=self.img_blank_block
                else:
                    if block_linking[row][col] == '-1':
                        btncolour=self.col_unlinked
                        btnimg=self.img_blank_block
                    else:
                        btncolour=acts[block_linking[row][col]]['colour']
                        btnimg=acts[block_linking[row][col]]['icon']
                if self.btn[row][col].cget('bg') != btncolour:
                    changed = True
                    self.btn[row][col].config(bg=btncolour, activebackground=btncolour, image=btnimg)
        return changed

    # Update the productive activity counter
    def update_productive_display(self):
        num_blocks = self.curBlocks()
        total_count = 0
        current_elapsed_count = 0
        for row in range(24):
            for col in range(6):
                if self.acts[self.block_linking[row][col]]['productive'] == "True":
                    total_count += 1
                    if row*6+col+1 <= num_blocks:
                        current_elapsed_count += 1

        self.counter_var.set(str(current_elapsed_count) + "/" + str(total_count))

    # Show the window for changing a blocks linked activity
    def display_activity_options_window(self, row, col):
        if self.check_var.get() == 1:
            act_opt_root = tk.Tk()
            
            act_opt = Activity_Options_Window(act_opt_root, row, col,
            [self.col_txt_primary, self.col_txt_secondary, self.col_bg, self.col_fg, self.col_unlinked],
            self)

            act_opt_root.mainloop()
    
    # Show the window for loading a plan, or saving the current plan
    def display_save_load_window(self):
        save_load_root = tk.Tk()

        save_load = Save_Load_Window(save_load_root, 
        [self.col_txt_primary, self.col_txt_secondary, self.col_bg, self.col_fg, self.col_unlinked],
        self)

        save_load_root.mainloop()
    
    # Toggle between editing mode and time mode
    def toggle_display_setting(self):
        if self.check_var.get() == 1:
            if hasattr(self, 'cur_timer'):
                self.master.after_cancel(self.cur_timer)
            self.counter_label.config(fg=self.col_bg) # hidden
            self.update_block_edit_display(self.block_linking, self.acts)
        else:
            self.counter_label.config(fg=self.col_txt_primary) # show
            self.timer_update_function(do_play_tune=False)
    
    # Timer function for updating the blocks when in time mode
    def timer_update_function(self, do_play_tune=True):
        self.update_productive_display()
        
        if self.update_block_time_display(self.block_linking, self.acts) and do_play_tune:
            self.play_tune()
        
        cur_minute = datetime.now().time().minute
        cur_second = datetime.now().time().second
        time_delay = int((10-cur_minute%10)*60 -60 + (60-cur_second) +1)
        if time_delay <= 0:
            time_delay = 1

        self.cur_timer = self.master.after(time_delay*1000, self.timer_update_function)

    # Play random tune from 'tunes' directory
    def play_tune(self):
        tune_options = []
        for filename in os.listdir("./tunes/"):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                tune_options.append(filename)
        
        if len(tune_options)==0:
            return
        else:
            tune_filename = "./tunes/" + random.choice(tune_options)
        subprocess.call(["ffplay", "-loglevel", "panic", "-nodisp", "-autoexit", tune_filename])

    # Return number of blocks completed today
    def curBlocks(self):
        curHour = datetime.now().time().hour
        curMinute = datetime.now().time().minute
        curNumBlocks = (curHour)*6 + curMinute//10
        return curNumBlocks

class Activity_Options_Window:
    """Activitity options window for changing linked blocks for 144 Blocks"""
    def __init__(self, master, row, col, colour_settings, app_obj):
        """
        Parameters:
        -----------
        row : int
            Value between 0 and 23
        col : int
            Value between 0 and 5
        """
        self.master = master
        self.acts = app_obj.acts
        [self.col_txt_primary, self.col_txt_secondary, self.col_bg, self.col_fg, self.col_unlinked]  = colour_settings
        self.row = row
        self.col = col
        self.var_options = tk.StringVar(self.master)

        self.var_options.set(app_obj.block_linking[row][col] if app_obj.block_linking[row][col] in list(app_obj.acts.keys()) else '-1')
        self.btn = app_obj.btn

        configure_window(self.master,"Activity Setting",200,100,False,False,self.col_bg)

        # Calculate the time start and end of current selected block acivity
        time_start = str(row).zfill(2)+":"+str(col)+"0"
        if col==5:
            if row==23:
                time_end = str(row+1-24).zfill(2)+":"+str(col-5)+"0"
            else:
                time_end = str(row+1).zfill(2)+":"+str(col-5)+"0"
        else:
            time_end = str(row).zfill(2)+":"+str(col+1)+"0"

        tk.Label(self.master, text="Select Activity for\n\n"+time_start+"-"+time_end, bg=self.col_bg, fg=self.col_txt_secondary).pack(side=tk.TOP)
        
        # Option menu of activities
        option_arr = list(app_obj.acts.keys())
        _args = (self.master, self.var_options) + tuple(option_arr)
        option = tk.OptionMenu(*_args)
        option.pack(side=tk.LEFT, padx=10)

        # OK button for selecting current activity
        btnOK = tk.Button(self.master, text="OK", bg='#66ff66', activebackground='#66ff66', command=lambda: self.buttonOK(app_obj))
        btnOK.pack(side=tk.RIGHT, padx=10)
    
    # Change activity linked to the current block
    def buttonOK(self, app_obj):
        chosen_option = self.var_options.get()
        chosen_colour = acts[chosen_option]['colour']
        chosen_image = acts[chosen_option]['icon']
        app_obj.block_linking[self.row][self.col] = chosen_option
        self.btn[self.row][self.col].config(bg=chosen_colour, activebackground=chosen_colour, image=chosen_image)

        self.master.destroy()


class Save_Load_Window:
    """Save/Load plan for 144 Blocks"""
    def __init__(self, master, colour_settings, app_obj):
        self.master = master
        self.master.lift()
        self.master.attributes('-topmost',True)
        [self.col_txt_primary, self.col_txt_secondary, self.col_bg, self.col_fg, self.col_unlinked]  = colour_settings
        self.btn = app_obj.btn

        configure_window(self.master,"Save/Load",300,150,False,False,self.col_bg)

        # Option menu of saved plans
        load_options = os.listdir("./saved_plans/")
        if len(load_options)>0:
            self.var_options = tk.StringVar(self.master)
            self.var_options.set(load_options[0])
            _args = (self.master, self.var_options) + tuple(load_options)
            option = tk.OptionMenu(*_args)
            option.pack(padx=20)

            # Load saved plan button
            btnLoad = tk.Button(self.master, text="Load", bg='#66ff66', activebackground='#66ff66', command=lambda: self.buttonLoad(app_obj))
            btnLoad.pack(padx=20,pady=2)
        
        # Save current plan button
        btnSave = tk.Button(self.master, text="Save", bg='#66ff66', activebackground='#66ff66', command=lambda: self.buttonSave(app_obj.block_linking))
        btnSave.pack(side=tk.BOTTOM,padx=20,pady=2)

        # Entry box for name of plan to save
        self.var_save_name = tk.StringVar(self.master)
        saveFilenameEntry = tk.Entry(self.master, font=("Courier",12), textvariable=self.var_save_name)
        saveFilenameEntry.pack(side=tk.BOTTOM)

    # Load the selected plan
    def buttonLoad(self, app_obj):
        chosen_option = self.var_options.get()
        filename_to_load = "./saved_plans/" +chosen_option
        
        app_obj.block_linking = read_saved_plan(filename_to_load)

        for row in range(24):
            for col in range(6):
                if app_obj.block_linking[row][col] == '-1':
                    btncolour=app_obj.col_unlinked
                    btnimg=tk.PhotoImage(width=block_size,height=block_size)
                else:
                    btncolour=acts[app_obj.block_linking[row][col]]['colour']
                    btnimg=acts[app_obj.block_linking[row][col]]['icon']

                self.btn[row][col].config(bg=btncolour, activebackground=btncolour, image=btnimg)
        
        self.master.destroy()
    
    # Save the current plan
    def buttonSave(self, block_linking):
        write_saved_plan(self.var_save_name.get(), block_linking)
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    # Load settings file containing appearance and activity settings
    settings_filename = "./settings.ini"
    if os.path.isfile(settings_filename):
        (colour_arr, block_size, acts) = read_settings_file(settings_filename, root)    
        [col_txt_primary, col_txt_secondary, col_bg, col_fg, col_unlinked]  = colour_arr
    else:
        write_settings_file(settings_filename, root)
        (colour_arr, block_size, acts) = read_settings_file(settings_filename, root)    
        [col_txt_primary, col_txt_secondary, col_bg, col_fg, col_unlinked]  = colour_arr

    app = App(root, block_size, acts, colour_arr)

    root.mainloop()
