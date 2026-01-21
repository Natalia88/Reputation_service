import requests
import uuid
import time

get_rep_url = "http://127.0.0.1:8000/getReputation/"
get_status_url = "http://127.0.0.1:8000/isReputationReady/"

try:
    hash_str = uuid.uuid4().hex
    response = requests.get(get_rep_url, params={'hash_str': hash_str})
    print(response.json())
    request_id = response.json()['request_id']
    time.sleep(10)
    status = requests.get(get_status_url, params={'request_id': request_id})
    print(status.json())
    #
    # # Print the full URL that was requested
    # print(f"Requested URL: {response.url}")
    #
    #
    # # Check if the request was successful (status code 200-299)
    # response.raise_for_status()
    #
    # # Parse the JSON response body into a Python dictionary/list
    # data = response.json()
    #
    # # Print the data (e.g., the name of the first repository)
    # if data:
    #     print(f"Response: {data}")
    # else:
    #     print("No data found.")

except requests.exceptions.RequestException as e:
    # Handle any errors during the request (e.g., connection issues, 4xx/5xx status codes)
    print(f"An error occurred: {e}")





