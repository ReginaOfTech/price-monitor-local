import csv
import threading
import time
from plyer import notification
from webscraper import start_scrape_page

# Change name here only
csv_title = 'scraped_data.csv'
# Change frequency here only
scraping_frequency = 10000 #milliseconds

# Shared resources
lock = threading.Lock()
wait = True
total_rows = 0
cur_row_pos = 1

def calc_total_rows():
    with open(get_csv_name()) as f:
        return int(sum(1 for line in f) / 2) - 1

def get_csv_name():
    return csv_title

def get_scraping_frequency():
    return scraping_frequency

def calculate_percent_of(num_a, num_b):
    return abs(((num_a - num_b) / num_b) * 100)

def set_wait(isWaiting):
    with lock:
        global wait
        wait = isWaiting

def get_wait():
    return wait

def set_total_rows(rows):
    with lock:
        global total_rows
        total_rows = rows

def get_total_rows():
    return total_rows

def set_cur_row_pos(pos):
    with lock:
        global cur_row_pos
        cur_row_pos = pos

def get_cur_row_pos():
    return cur_row_pos

def reset_cur_row_pos():
    set_cur_row_pos(1)

def scrape_csv(event):
    # tick_thread needs set wait to False for scrape_thread to move forward
    while get_wait() is True:
        if event.is_set():
            break
        time.sleep(0.5)

    # Make sure event hasn't been set
    if event.is_set() is False:
        with open(get_csv_name()) as file:
            reader = csv.DictReader(file)
            set_total_rows(calc_total_rows())
            for i, row in enumerate(reader, start=1):
                # Let scrape_thread know where scrape_thread is at in file
                set_cur_row_pos(i)
                # Check that event is not set before starting scrape
                if event.is_set():
                    break
                title, price = start_scrape_page(row['url'], event)
                if event.is_set():
                    break
                check_to_notify(row, price)
        # Let tick_thread that scraping is done
        set_wait(True)
        reset_cur_row_pos()
        if event.is_set():
            return
        # Recursive call so that thread stays in this method
        scrape_csv(event)

def check_to_notify(dict_row, scraped_product_price):
    # Check old and new scraped prices to see if user needs to know about sales
    if float(scraped_product_price) < float(dict_row['price']):
        # Create notification
        title_end = " is on SALE!!"
        title_full = f"{dict_row['title']}{title_end}"
        # title can only be 64 characters long.
        if len(title_full) > 64:
            # Figure out how many characters need to be removed to fit
            diff = 64 - len(title_full)
            # Remove excess characters from product title
            new_prod_title = dict_row['title'][0:diff]
            title_full = f"{new_prod_title}{title_end}"
        # Calculate the percentage off
        percent_off = calculate_percent_of(float(scraped_product_price), float(dict_row['price']))
        message = f"It's now {percent_off}% off.\n" \
                  f"Can be found at:\n" \
                  f"{dict_row['url']}"
        notification.notify(title=title_full, message=message, app_icon=None, timeout=10, toast=False)