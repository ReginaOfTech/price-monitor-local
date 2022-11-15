import tkinter as tk
from tkinter import ttk, messagebox
from webscraper import start_scrape_page
import csv
import os.path
import helper_methods


class App(tk.Tk):
    def output_data(self, url, title, price):
        # Output data to the csv
        try:
            # Default to create and write to file
            action = 'w'
            # If csv is present then append
            if os.path.exists(self.csv_title):
                action = 'a'
            data = [title, price, url]
            with open(self.csv_title, action) as file:
                write = csv.writer(file)
                # If csv is new then need to insert header line
                if action == 'w':
                    header = ["title", "price", "url"]
                    write.writerow(header)
                write.writerow(data)
        except Exception as e:
            return False
        return True

    def on_closing(self):
        self.event.set()
        self.destroy()

    def __init__(self, event):
        super().__init__()
        self.event = event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        app_width=450
        app_height = 100
        app_location_x = (self.winfo_screenwidth() / 2) - (app_width / 2)
        app_location_y = (self.winfo_screenheight() / 2) - (app_height / 2)
        # Place gui in center of screen so that user can see it easily
        self.geometry(f'{app_width}x{app_height}+{int(app_location_x)}+{int(app_location_y)}')
        # Fixed window size
        self.resizable(0, 0)
        self.title('Price Monitor')

        # initialize website data
        self.websites = ('amazon') #, 'walmart', 'bath and body works', etc)

        # set up variable
        self.option_var = tk.StringVar(self)

        # create widget
        self.create_wigets()

    def create_wigets(self):
        # padding for widgets using the grid layout
        paddings = {'padx': 5, 'pady': 5}

        # label
        label = ttk.Label(self, text='Select the website you are following:')
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            self.websites[0],
            *self.websites,
            command=self.option_changed)

        option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

        # Create UI
        self.output_label = ttk.Label(self, text='https://www.amazon.com/', foreground='red')
        self.output_label.grid(column=0, row=1, sticky=tk.W, **paddings)
        self.input_textbox = ttk.Entry(self)
        self.input_textbox.grid(column=1, row=1, sticky=tk.W, **paddings)
        self.status_label = ttk.Label(self, text='', foreground='black')
        self.status_label.grid(column=2,row=1,sticky=tk.W, **paddings)
        self.monitor_button = ttk.Button(self, text='Follow', command=self.monitor_clicked)
        self.monitor_button.grid(column=1, row=3, sticky=tk.W, **paddings)
        self.run_button = ttk.Button(self, text='Run', command=self.run_clicked)
        self.run_button.grid(column=0, row=3, sticky=tk.W, **paddings)

    def option_changed(self, *args):
        # Change if user switches between website drop down
        self.output_label['text'] = f'https://www.{self.option_var.get()}.com/'
        self.output_label.update()

    def status_changed(self, text, color):
        # Let user know state of scrape run
        self.status_label.config(text=text)
        self.status_label.config(foreground=color)
        self.status_label.update()

    def monitor_clicked(self, *args):
        # New website page has been requested. Create full url.
        full_url = self.output_label.cget("text")+self.input_textbox.get()
        title, price = "", 0.0
        # Make sure that user entered end of url
        if len(self.input_textbox.get()) > 1:
            # check to update label to let user know the program is running
            if self.option_var.get() == self.websites[0]:
                # Amazon is only option currently.
                self.status_changed(f'Scraping {self.option_var.get()}...', 'black')
            elif self.option_var.get() == self.websites[1]:
                # Amazon is only option currently.
                self.status_changed(f'Scraping {self.option_var.get()}...', 'black')
            title, price = start_scrape_page(full_url)
        else:
            self.status_changed(f'Fail: Check url!', 'red')
            return

        # Make sure that values were properly retrieved before adding to csv
        if len(title) > 0 and price > 0:
            # Let user know status
            if self.output_data(full_url, title, price):
                self.status_changed('Success', 'green')
            else:
                self.status_changed('Fail', 'red')
        else:
            self.status_changed('Fail: Check url!', 'red')

    def run_clicked(self):
        # User is ready to run program.
        # Leave to create timer_gui
        if os.path.exists(helper_methods.get_csv_name()):
            if helper_methods.calc_total_rows() > 1: # First row is header line
                self.destroy()

        messagebox.showwarning(title="Missing Data", message="You are not following any products! Please add urls.")
