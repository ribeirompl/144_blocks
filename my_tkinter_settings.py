"""
Functions for easily setting up Tkinter window settings

Author: Marco P. L. Ribeiro
Date: June 2019

MIT License
Copyright (c) 2019 Marco P. L. Ribeiro
"""

def configure_window(master, title="Python Application", width=600, height=600, resizable=True, centred=True, bg=None):
    '''Configure Tkinter GUI window

    Parameters
    ----------
        master : Tk object
        title : str
            Application title
        width : int
            Application width
        height : int
            Application height
        resizable : bool
            Allow resizing of application
        centred : bool
            Centre application on screen
        bg : tkinter color string
            Application background colour
    '''
    
    master.title(title)

    if centred:
        s_width = master.winfo_screenwidth()
        s_height = master.winfo_screenheight()
        x = (s_width - width)//2
        y = (s_height - height)//2
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))
    else:
        master.geometry('{}x{}'.format(width, height))

    if not resizable:
        master.resizable(width=False, height=False)
    
    if bg is not None:
        master.configure(bg=bg)
