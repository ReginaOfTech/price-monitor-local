import helper_methods
from url_gui import App
from timer_gui import TimerApp
import threading
from threading import Event

def create_url_gui(event):
    app = App(event)
    app.mainloop()

def start_csv_checking(event):
    if event.is_set():
        return

    # Thread that waits until event is set for it to scrape the csv file
    scrape_thread = threading.Thread(target=helper_methods.scrape_csv, args=(event,))
    app = TimerApp(event, scrape_thread)

    # Thread that will handle "talking" to scrape thread
    # also handles displaying countdown
    tick_thread = threading.Thread(target=app.tick())

    # When main thread terminates, all threads should terminate as well
    tick_thread.daemon
    scrape_thread.daemon

    # Start threads
    scrape_thread.start()
    tick_thread.start()

    # Main thread enters main loop
    # Tkinter requires master thread to be in main loop
    app.mainloop()

if __name__ == '__main__':
    # event that will be triggered when user wants to stop program
    event = Event()
    create_url_gui(event)
    start_csv_checking(event)
