import schedule
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from tinydb import TinyDB, Query


websites_to_monitor = [
    'https://www.telesphera.net'
]
response_time_threshold = 2.0  # in seconds


def check_website_performance(url):
    current_time = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
        # Send a GET request to the website
        response = requests.get(url, timeout=10, headers=headers)

        # Measure response time
        response_time = response.elapsed.total_seconds()
        # Check the status code
        if response.status_code == 200:
            print(f"[{datetime.now()}] {url} is up. Response time: {response_time} seconds.")
        else:
            print(f"[{datetime.now()}] {url} is down. Status code: {response.status_code}.")
            return False, response_time

        return True, response_time, current_time

    except requests.exceptions.RequestException as e:
        # Handle exceptions like connection errors, timeouts, etc.
        print(f"[{datetime.now()}] Error checking {url}: {e}")
        return False, None, current_time



# def send_email_alert(subject, body, to_email):
#     from_email = 'your-email@example.com'
#     password = 'your-email-password'
#
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = from_email
#     msg['To'] = to_email
#
#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP('smtp.example.com', 587) as server:
#             server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
#             server.login(from_email, password)
#             server.sendmail(from_email, to_email, msg.as_string())
#         print("Alert email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")


# def monitor_websites(websites, threshold):
#     for url in websites:
#         is_up, response_time = check_website_performance(url)
#
#         if not is_up or (response_time is not None and response_time > threshold):
#             # Prepare email alert
#             subject = f"Website Performance Alert: {url}"
#             body = f"Website {url} is down or slow. Response time: {response_time} seconds."
#             send_email_alert(subject, body, 'recipient-email@example.com')
#
#
# schedule.every(5).minutes.do(monitor_websites, websites=websites_to_monitor, threshold=response_time_threshold)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
