import ssl
import time

import requests
import selectorlib
import os
import smtplib

if os.path.exists('env.py'):
    import env

URL = 'http://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def send_email(message):
    host = 'smtp.gmail.com'
    port = 465

    username = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')

    receiver = username
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email sent!")


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value


def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + "\n")


def read(extracted_data):
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        content = read(extracted)
        if extracted != 'No upcoming tours':
            if extracted not in content:
                store(extracted)
                send_email(message='New event was found!')
        time.sleep(2)
