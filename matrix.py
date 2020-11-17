import curses
import sys
import time
import threading
import os
import subprocess
import requests
import json

import psutil

#
# Global variables
#
stdscr = None
debug = True
height = 0
width = 0
to_init = True
status_bar_str = "Status: "
cp = None
stop_threads = False

lines = [None]
scrollers = [None]

#
# Global constants
#
SCROLL_TIME = 0.1
REFRESH_TIME = 0.1

#
# Lines related constants
#
NUM_LINES = 4

EMAIL_LINE = 1
CMD_LINE = 2
SYSTEM_DETAILS_LINE = 3

LINE_NAME_DICT = {
    EMAIL_LINE : {"name" : "Email Line", "header" : "Email"},
    CMD_LINE : {"name" : "Command Line", "header" : "Command"},
    SYSTEM_DETAILS_LINE : {"name" : "System Details Line", "header" : "System Details"}
}

scroller_names = ["Line_Thread_%d" % (x) for x in range(1, NUM_LINES)]

class Line():
    def __init__(self, name, line_no, header, data):
        self.name = name
        self.line_no = line_no
        self.header = header
        self.data = data
        self.scroll_reset = False
        self.y = 0
        self.x = 0
        self.line = ""
        self.d_start = 0
        self.d_finish = 0
        self.num_scrolled = 1
        self.to_display = ""

    def show_data(self, x):
        global stdscr

        curses.setsyx(self.line_no, 0)
        stdscr.clrtoeol()
        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)

        if len(self.data) > width:
            self.start_x = (len(self.header) + 2)
            self.finish_x = width - 1
            self.d_length = self.finish_x - self.start_x
            self.d_finish = self.d_start + self.d_length
            self.to_display = self.data[self.d_start: self.d_finish]
            self.line = "%s: %s" % (self.header, self.to_display)
            self.d_start += 1
        else:
            self.to_display = self.data
            self.line = "%s: %s%s" % (self.header, " " * x, self.to_display)
            if len(self.line) > width:
                self.line = "%s: %s%s%s" % (self.header,
                                                self.to_display[-self.num_scrolled:],
                                                " " * (x - self.num_scrolled),
                                                self.to_display)
                self.num_scrolled += 1

        if len(self.line) == width + len(self.data):
            self.scroll_reset = True
            self.num_scrolled = 1

        stdscr.addnstr(self.y, self.x, self.line, width)

class Command_Processor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        status("Started Command Processor")

    def run(self):
        global stdscr
        global lines
        global stop_threads
        global scrollers
        while True:
            cmd = stdscr.getch()

            if cmd == ord('q'):
                stop_threads = True

            if cmd == ord('c'):
                status("Enter command")
                run_cmd = ""
                while True:
                    c = stdscr.getch()
                    if c == curses.KEY_ENTER or c == 10 or c == 13:
                        break

                    run_cmd += chr(c)
                try:
                    result = subprocess.check_output(run_cmd.strip().split())
                    result = result.decode("ascii")
                    result = result.replace("\n", "    ")
                    lines[CMD_LINE].data = result
                    scrollers[CMD_LINE].x = 0
                    lines[CMD_LINE].num_scrolled = 1
                except Exception as e:
                    status("Exception: %s" % (str(e)))

            if cmd == ord('s'):
                try:
                    mem_used = psutil.virtual_memory().percent
                    cpu_used = psutil.cpu_percent()
                    disk_used = subprocess.check_output("df -h /".split())
                    disk_used = disk_used.decode("ascii")
                    du_list = disk_used.split("\n")[1].split()
                    disk_used = "Total Disk -> %s, Used Disk -> %s, Available Disk -> %s" % (du_list[1], du_list[2], du_list[3])

                    lines[SYSTEM_DETAILS_LINE].data = "Memory usage -> %s, CPU usage -> %s, Disk Usage -> %s" % (mem_used, cpu_used, disk_used)
                    scrollers[SYSTEM_DETAILS_LINE].x = 0
                    lines[SYSTEM_DETAILS_LINE].num_scrolled = 1
                except:
                    status("Exception while showing system utils data")

            time.sleep(SCROLL_TIME)
            if stop_threads:
                break

class Scroller(threading.Thread):
    def __init__(self, line, q):
        threading.Thread.__init__(self)
        self.line = line
        self.q = q
        self.y = self.line.line_no
        self.x = 0

        self.name = "Scroller for line %d" % (self.line.line_no)

        status("Started %s" % (self.name))

    def run(self):
        global stop_threads
        while True:
            if self.line.scroll_reset:
                self.x = 0
                self.line.scroll_reset = False

            self.line.show_data(self.x)
            time.sleep(0.1)
            if stop_threads:
                break
            self.x += 1

def set_line_data(line_no, data):
    global lines
    lines[line_no].data = data

def get_line_data(line_no):
    global lines
    return lines[line_no].data

def start():
    global stdscr
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.scrollok(True)

def terminate():
    global scrollers
    global stop_threads
    global cp

    stop_threads = True
    for scroller in scrollers:
        if scroller != None:
            scroller.join()

    cp.join()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def set_init_line(line_no, data, y_pos, x_pos):
    global lines

    line_name = LINE_NAME_DICT[line_no]['name']
    line_header = LINE_NAME_DICT[line_no]['header']
    line_data = data
    line = Line(line_name, line_no, line_header, line_data)
    line.x = x_pos
    line.y = y_pos

    curses.setsyx(line.line_no, len(line.header) + 1)
    stdscr.clrtoeol()
    stdscr.attron(curses.color_pair(1))
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(line.y, line.x, data)

    lines.append(line)

def start_line_scroller(line_no):
    global lines

    line = lines[line_no]
    scroller = Scroller(line, None)

    scrollers.append(scroller)

    scroller.start()

def start_command_processor():
    global cp
    cp = Command_Processor()
    cp.start()

def set_init_lines():
    set_init_line(EMAIL_LINE, "", EMAIL_LINE, 0)
    set_init_line(CMD_LINE, "", CMD_LINE, 0)
    set_init_line(SYSTEM_DETAILS_LINE, "", SYSTEM_DETAILS_LINE, 0)

def status(msg):
    stdscr.addstr(height - 1, 50, str(msg))
    time.sleep(1)

def draw_menu(stdscr):
    global debug
    global to_init
    global scrollers
    global height
    global width

    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    while True:
        #
        # Initialization
        #
        if to_init:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            #
            # Rendering width and height
            #
            whstr = "Width: {}, Height: {} [h -> Help, q -> Exit]".format(width, height)
            stdscr.addstr(0, 0, whstr, curses.color_pair(1))

            #
            # Render status bar
            #
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(height-1, 0, status_bar_str)
            stdscr.addstr(height-1, len(status_bar_str),
                            " " * (width - len(status_bar_str) - 1))
            stdscr.attroff(curses.color_pair(1))

            set_init_lines()
            start_command_processor()
            #
            # Start threads to scroll
            #
            for i in range(1, NUM_LINES):
                start_line_scroller(i)

            to_init = False

        if stop_threads:
            break
        #
        # Refresh the screen
        #
        stdscr.refresh()

        time.sleep(REFRESH_TIME)

if __name__ == "__main__":
    try:
        start()
        curses.wrapper(draw_menu)
        terminate()
    except:
        if debug == True:
            print(sys.exc_info())
        terminate()
