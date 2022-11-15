import time
import tkinter as tk
from tkinter import *
from datetime import datetime, timedelta
import helper_methods

class TimerApp(tk.Tk):

    def __init__(self, event, thread):
        super().__init__()
        self.event = event
        self.scrape_thread = thread
        self.scraping_frequency = helper_methods.get_scraping_frequency()
        self.next_scrape_time = datetime.utcnow() + timedelta(milliseconds=self.scraping_frequency)

        # create widget
        app_width = 400
        app_height = 100
        app_location_x = (self.winfo_screenwidth()/2) - (app_width/2)
        app_location_y = (self.winfo_screenheight()/2) - (app_height/2)
        self.geometry(f'{app_width}x{app_height}+{int(app_location_x)}+{int(app_location_y)}')
        self.resizable(0, 0)
        self.title('Price Monitor')
        self.create_wigets()

    def create_wigets(self):
        # Create clock label and stop button
        self.clock = tk.ttk.Label(self, font =('Helvetica bold',22), foreground='black', anchor=CENTER, justify=CENTER)
        self.clock.pack(fill="both", expand=1)
        self.stop_button = tk.ttk.Button(self, text='Stop', command=self.stop_clicked)
        self.stop_button.pack(fill="both", expand=1)

    def update_label(self, text, color='black'):
        # Update clock label text and color
        self.clock.config(text=text)
        self.clock.config(foreground=color)
        self.update()

    def stop_clicked(self):
        # Let scrape_thread know that user wants to stop
        self.event.set()

        full_text = "Stopping...."
        self.update_label(full_text)
        # Let user know that we are stopping while tick_thread
        # is waiting
        while self.scrape_thread.is_alive() is True:
            text = ""
            if len(self.clock.cget("text")) == len(full_text):
                text = full_text[0:-3]
            else:
                text = self.clock.cget("text") + '.'
            self.update_label(text)
            time.sleep(0.5)

        # Once scrape_thread is dead then destroy this UI
        # signals main thread to leave main loop
        self.destroy()

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return hour, minutes, seconds

    def scraping_has_started(self):
        # Holding place for tick_thread while scrape_thread runs
        while helper_methods.get_wait() is False:
            # Let user know status
            if helper_methods.get_total_rows() > 0:
                text = f'Scraping {helper_methods.get_cur_row_pos()} of {helper_methods.get_total_rows()}'
            else:
                text = 'Prepping to scrape...'
            self.update_label(text)

    def tick(self):
        nextCall = 200

        # Find out how much time is left in wait pattern
        diff = self.next_scrape_time - datetime.utcnow()
        # convert to milliseconds
        diff_ms = diff.total_seconds() * 1000

        # Time has been met
        if diff_ms <= 0:
            # "Release" scrape_thread to start scraping
            helper_methods.set_wait(False)
            # tick_thread goes into its holding pattern
            self.scraping_has_started()
            # Once scrape_thread has finished tick_thread set next time
            self.next_scrape_time = datetime.utcnow() + timedelta(milliseconds=self.scraping_frequency)
        else:
            # Thread is still waiting, update clock face
            hour, min, sec = self.convert(diff.total_seconds())
            text= "%02d:%02d:%02d" % (hour, min, sec)
            self.update_label(text)
            # If time to next_scrape_time is less than 200milliseconds
            # set nextCall to value so that tick occurs on time
            if diff_ms < 200 and diff_ms > 0:
                nextCall = int(diff_ms)

        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.clock.after(nextCall, self.tick)
