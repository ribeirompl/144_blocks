# 144 Blocks
Focused time planner for planning your day into 10-minute blocks, and keeping you aware of how many productive blocks you have left in the day.
Inspired by Tim Urban's [100-Blocks article](https://waitbutwhy.com/2016/10/100-blocks-day.html) and [144 Blocks website](144blocks.com)
## Project Description
There are 144 blocks, representing the 144 10-minute time slots in a day. By clicking on a block, the activity option window is shown (see bottom right) where you can change the activity.

![Gui display](help_images/readme_img.png?raw=true "Gui display")

If you toggle the edit checkbox off, then it displays the blocks from the past in black. It also displays a counter at the bottom showing the completed productive-blocks out of the total number of productive-blocks. Each activity can be set as either productive or non-productive in the settings file. In this example the gold "work" blocks and the red "planning" blocks are productive.

The settings button currently opens the save/load window, however, it will have extra functionality in the future.

Currently the settings file has to be manually edited, where you have control of the GUI colours, block sizes and the attributes for each activity. This application was designed to have complete customisability.

![Settings file](help_images/settings_file.png?raw=true "Settings file")

You can add multiple .mp3 or .wav files into the `tunes/` folder, which will play a random tune, every 10 minutes, when a block is completed.

## Future Plans
* GUI interface for editing settings file
* Windows support
* Better GUI scaling (scrollbar)

## Dependencies
Currently, only linux operating systems are supported.
```
Python >= 3.7
Tkinter >= 8.6
Pillow >= 6.0.0

ffmpeg >= 3.4.6
```

## Installation
Copy the files into a directory.


To start the application:
```sh
python3 144blocks.py
```

