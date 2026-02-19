import requests
import logging
from retry.api import retry_call

# Some basic logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Global variable to track the number of attempts
# to help simulate a flaky endpoint that fails a few times before succeeding
attempts = 0

def flaky_get():
    global attempts
    attempts += 1
    uri = ""
    
    if attempts < 3:
        uri = "https://httpbin.org/status/500"  # Simulate failure
    else:
        uri = "https://httpbin.org/get"  # Simulate success
    logging.info(f"Attempt {attempts}: Making request to {uri}")
    response = requests.get(uri)
    if response.status_code != 200:
        logging.error(f"Attempt {attempts} failed with status code {response.status_code}")
        raise Exception(f"Request failed with status code {response.status_code}")
    logging.info(f"Attempt {attempts} succeeded with status code {response.status_code}")
    return response.text

if __name__ == "__main__":
    try:
        result = retry_call(flaky_get, tries=5, delay=2)
        logging.info("Request succeeded")
        logging.info(f"Total attempts: {attempts}")
    except Exception as e:
        logging.error("All attempts failed")
        logging.error(f"All attempts failed: {e}")