# Price Monitor
This is a simple price monitor that utilizes BeautifulSoup, threading, and selenium-wire. This webscarper can easily be changed to work with any other website once the proper tags are found to scrape the needed information.

## To Run
1) Pull code down from repo
```git
$ git clone {repo}
```
2) Make sure the following dependencies are installed:
```python
$ pip install beautifulsoup4
$ pip install selenium
$ pip install selenium-wire
$ pip install fake-useragent
$ pip install webdriver_manager
$ pip install tkinter
$ pip install plyver
```
3) Open your preferred python IDE and open 'main.py' in the folder

4) Run main.py

## To Use
Once you have pulled the code and have it locally you can run the code from the main.py file. 

A popup window will be displayed where you can paste an Amazon url. To successfully scrape the page you only need to include from the '/' after '.com' to right before any 'ref' in the url.  
Examples:  
`https://www.amazon.com/dp/B01HPI5AM2/ref=...` -> dp/B01HPI5AM2/  
`https://www.amazon.com/Python-DevOps-Ruthlessly-Effective-Automation/dp/149205769X/ref=...` -> /Python-DevOps-Ruthlessly-Effective-Automation/dp/149205769X/  
Paste the ending into the text box and hit the 'Follow' button.

A data collection will occur to check the url validity, but also to retrieve the current price that the product is to watch for sales. 
If the url is valid it is inserted into a csv with its title, price, and url. 

Now that the program has a url to look at, all you need to do is hit the 'Run' button and it will do data collection at specified intervals. 

If a price reduction is found then you will be notified with a notification in the bottom right corner of your screen. The notification pop up will contain the name of the product, what its current sale is, and the url so you can go get it.

To stop the program either press the 'Stop' or 'x' button on the timer window. 

## Personalize
There are 3 elements that you can change to make the price monitor work as you would like

1) Csv file name  
To do this go the helper_methods.py file and change 'csv_title' to what you would prefer

2) Scraping frequency  
The default value is 10 seconds, but can be changed to any time interval that you would like. Just keep in mind that the expected input is in milliseconds.  
1,000 milliseoncds = 1 sec

3) Run browser in background  
By default selenium will run the browser in front so that the user can see what is happening. You can change this to run in the background by going to 'webscraper.py' and changing 'run_browser_in_background' to 'True'.

# Enhancements
Not everything is perfect right off the bat. Taking into consideration budget, time, purpose, ease of use, and priority this program could be enhanced.

## Ideas
### Run the data collection event on an AWS Lambda
When the user clicks either of the 'Follow' or 'Run' buttons this will reach out to an API that will trigger a Lambda event.

#### Steps
1) Create IAM role for AWS Lambda  
2) Go to 'webscraper.py' and add a new function for the Lambda service to use
```python
def lambda_handler(event, context):
    start_scrape_page()
```
3) Create function in Lambda  
Create a function from the Lambda dashboard by clicking "Create Function". Then write the function name and choose a runtime of the code. The code is written with Python3.  
4) Upload any dependencies that AWS doesn't natively have
### Store the scraped information in a database
The scraped data could be easily stored in a database locally or on AWS. This could be stored in a datalake or relational database with each feature having its own column. The choice is yours.
### Send SMS text instead of desktop notification
This can be achieved by using a paid API service in its current state. However, if the scraper is moved to AWS Lambda then the function could handle sending a text through an Amazon SNS topic
