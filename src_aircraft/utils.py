import logging
from tenacity import retry, stop_after_attempt, wait_fixed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def get_request_with_retries(url):
    import requests
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed request with status code {response.status_code}")
    return response


def log_message(message):
    logging.info(message)


if __name__ == "__main__":
    # Example usage of utility functions
    url = "https://opensky-network.org/api/states/all"
    response = get_request_with_retries(url)
    log_message(f"Request to {url} completed with status code {response.status_code}")
