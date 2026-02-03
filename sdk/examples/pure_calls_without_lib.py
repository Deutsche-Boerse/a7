import pandas as pd
import requests
import numpy as np
from pprint import pprint
import time
from datetime import datetime, timedelta
import json
import urllib3
import yaml
from urllib.parse import quote_plus  # Import quote_plus

# --- User Configuration ---
OWNER = "your_userid"  # Replace with your A7 login
API_TOKEN = "your_token"
ALGO_NAME = "testing_algo"  # Name of the algo to upload/download/delete/run
ALGO_FILE = "testing_algo.yml"
SECURITY_ID = 2504978  # Unique security identifier on T7 (example: for XEUR 4611674 is FGBL SI 20200908 PS, for XETR 2504978 is DEUTSCHE BOERSE NA O.N.)
MARKET_SEGMENT_ID = 52885  # # Unique product identifier or product pool identifier of market on T7 (example: for XEUR 688 is FGBL, for XETR 52885 is DB1)
MARKET_ID = "XETR"  # Market identifier code as specified in ISO 10383 (XEEE, XETR, XEUR)
DATA_DATE = "20230804"  # Data Date
OUTPUT_FILE = "OUTPUT"  # Output to CSV file
LIMIT_OUTPUT_TO = 15 # Global setting for limiting JSON output. Set to 0 for unlimited

# --- End User Configuration ---

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
VERIFY_SSL = False

PROXIES = {
    "http":  "", #Enter http Proxy if needed",
    "https": ""  #Enter https Proxy if needed",
}

A7_API_BASE_URL_DEV = "https://a7.deutsche-boerse.de/api/v1"
A7_API_BASE_URL_PROD = "https://a7.deutsche-boerse.com/api/v1"
A7_API_BASE_URL_PROD_INT = "https://a7.deutsche-boerse.de/api/v1"
# --- Choose environment ---
A7_API_BASE_URL = A7_API_BASE_URL_DEV

# --- Functions ---

def load_yaml(file_path):
    """Loads a YAML file and returns its content as a dictionary."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: ")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: ")
        return None


def get_algo_owners():
    """Retrieves a list of algo owners."""
    url = f"{A7_API_BASE_URL}/algo"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        print(f"GET {url}")
        response = requests.get(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching algo owners: {e}")
        return None


def get_algos(owner, mode="compact"):
    """Retrieves a list of available algos for a given owner."""
    url = f"{A7_API_BASE_URL}/algo/{owner}?mode={mode}"  # Added mode parameter and owner
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        print(f"GET {url}")
        response = requests.get(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching algos for owner {owner}: {e}")
        return None

def delete_algo(owner, algo_name):
    """Deletes an algo."""
    encoded_algo_name = quote_plus(algo_name)
    url = f"{A7_API_BASE_URL}/algo/{owner}/{encoded_algo_name}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        print(f"DELETE {url}")
        response = requests.delete(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL)
        response.raise_for_status()
        return {"success": True, "message": "Algo deleted successfully"}
    except requests.exceptions.RequestException as e:
        print(f"Error deleting algo {algo_name}: {e}")
        if response is not None:
            print(f"Response code: {response.status_code}")
            try:
                print(f"Response content: {response.content.decode()}")
            except:
                print(f"Decoding failed.") # decoding failed.
        return {"success": False, "message": f"Failed to delete algo: {e}"}


def upload_algo(owner, algo_name, algo_file):
    """Uploads an algo from a YAML file."""
    encoded_algo_name = quote_plus(algo_name)  # URL encode the algo name
    url = f"{A7_API_BASE_URL}/algo/{owner}/{encoded_algo_name}"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/yaml"}  # Correct Content-Type for YAML!

    algo_source = load_yaml(algo_file)  # Correctly load the algo from the YAML file.
    if algo_source is None:
        print("Error: Could not load algo source from file.")
        return None

    #Verify name matches url
    if "title" in algo_source:
        yamlTitle = algo_source["title"]
        if algo_name != yamlTitle: #The error may be here!
          print(f"YAML's Title field must be {algo_name}, which is not matching {yamlTitle}. Please fix.")

    try:
        print(f"PUT {url}")
        # Explicitly format the YAML with a block scalar style
        yaml_data = yaml.dump(algo_source, indent=2, sort_keys=False, width=79, allow_unicode=True)

        response = requests.put(url, headers=headers, data=yaml_data, proxies=PROXIES, verify=VERIFY_SSL)  # Consistent verify parameter
        response.raise_for_status()

        response_json = response.json()  # Capture the JSON response

        if "success" in response_json and response_json["success"] == False:
            print(f"Upload failed according to API: {response_json.get('message', 'No message provided')}")

        return response_json
    except requests.exceptions.RequestException as e:
        print(f"Error uploading algo: {e}")
        if response is not None:
            print(f"Response code: {response.status_code}")
            try:
                print(f"Response content: {response.content.decode()}")
            except:
                print(f"Decoding failed") # decoding failed.
        return None


def download_algo(owner, algo_name):
    """Downloads an algo's source code."""
    encoded_algo_name = quote_plus(algo_name)  # URL encode the algo name
    url = f"{A7_API_BASE_URL}/algo/{owner}/{encoded_algo_name}/download"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        print(f"GET {url}")
        response = requests.get(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL)
        response.raise_for_status()
        # print(response.headers['Content-Type'])
        return response.content.decode(
            "utf-8")  # Changed to .content to get bytes, necessary since it is downloading the ALGO's yaml string code.
    except requests.exceptions.RequestException as e:
        print(f"Error downloading algo {algo_name}: {e}")
        return None

def run_algo(owner, algo_name, market_id, date, market_segment_id, security_id, additional_params=None):
    """Runs an algo with specified parameters."""
    encoded_algo_name = quote_plus(algo_name)  # URL encode the algo name
    url = f"{A7_API_BASE_URL}/algo/{owner}/{encoded_algo_name}/run?marketId={market_id}&date={date}&marketSegmentId={market_segment_id}&securityId={security_id}"
    if additional_params:
        # Format additional parameters into the URL
        url += '&' + '&'.join([f'{k}={v}' for k, v in additional_params.items()])

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        print(f"GET {url}")
        response = requests.get(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL)
        response.raise_for_status()
        algo_run_response = response.json() # Capture the response JSON

        if LIMIT_OUTPUT_TO == 0:
            print(f"Algo run response:\n{json.dumps(algo_run_response, indent=2)}")  # Print all
        else:
            # Limit the output to the first LIMIT_OUTPUT_TO items if it's a list
            if isinstance(algo_run_response, list):
                limited_response = algo_run_response[:LIMIT_OUTPUT_TO]
                print(f"Algo run response (first {min(LIMIT_OUTPUT_TO, len(algo_run_response))} items):\n{json.dumps(limited_response, indent=2)}")
            else:
                print(f"Algo run response:\n{json.dumps(algo_run_response, indent=2)}")  # Print the whole thing if it's not a list

        return algo_run_response  # Return the original response
    except requests.exceptions.RequestException as e:
        print(f"Error running algo {algo_name}: {e}")
        if response is not None:
            print(f"Response code: {response.status_code}")
            try:
                print(f"Response content: {response.content.decode()}")
            except Exception as e:
                print(f"Response content could not be printed. Decoding Failed.")

        return None


# EOBI data functions from the previous example
def get_transact_times(market_id, date, market_segment_id, security_id, limit=15):
    """Fetches a list of TransactTimes."""
    url = f"{A7_API_BASE_URL}/eobi/{market_id}/{date}/{market_segment_id}/{security_id}?limit={limit}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        print(f"GET {url}")
        response = requests.get(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transact times: {e}")
        if response is not None:
            print(f"Response code: {response.status_code}")
            try:
                print(f"Response content: {response.content.decode()}")
            except:
                print(f"Content Decode failed, error {e}") # content Decode failed.
        return None

def get_orderbook(market_id, date, market_segment_id, security_id, from_time, to_time=None, levels=10, orderbook_type="aggregated", trades=True):
    """Retrieves order book data for T7 from the /ob API."""
    ### Changed Type from Int to String
    url = f"{A7_API_BASE_URL}/ob/{market_id}/{date}/{market_segment_id}/{security_id}"

    params = {
        "from": from_time,
        "levels": levels,
        "orderbook": orderbook_type,
        "trades": trades,
    }
    if to_time:  # Added condition for to_time
        params["to"] = to_time

    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        print(f"URL: {url}") #Line added to print the url.
        print(f"Params: {params}") #Line added to print parameters.
        response = requests.get(url, headers=headers, proxies=PROXIES, verify=VERIFY_SSL, params=params) #Added params=params
        response.raise_for_status()
        order_book_data = response.json()

        if order_book_data:  # Check if order_book_data is not None
            if isinstance(order_book_data, list):  # Check if it's a list of order books
                if LIMIT_OUTPUT_TO == 0:
                    print(f"Order Book Data:\n{json.dumps(order_book_data, indent=2)}")
                else:
                    num_rows = min(LIMIT_OUTPUT_TO, len(order_book_data))  # Limit to the specified number or less
                    print(f"Order Book Data (first {num_rows} rows):\n{json.dumps(order_book_data[:num_rows], indent=2)}")
            elif "MarketId" in order_book_data:  # Check if it's a single order book
                print(f"Order Book Data:\n{json.dumps(order_book_data, indent=2)}")
            else:
                print("Unexpected order book data format.")
                print(f"Data: {order_book_data}")  # Print order book data. I added this.

        else:
          print(f"Failed to retrieve order book data in get_orderbook(), function returned None, investigate why.")
          if response is not None:
            try:
              print(f"API response content within get_orderbook(): {response.content.decode()}") #Very Important!
            except Exception as e:
              print(f"Response content within get_orderbook() could not be printed, decoding failed, message {e}. try to call get with curl.")#Very Important!
          else:
            print(f"Response was None, possible connection  or setup issue. #Check network & verify settings.") # check response.
          #Try to call get the same URL in CURL to check if result is back.

        return order_book_data #Return order book data.

    except requests.exceptions.RequestException as e:
        print(f"Error fetching order book data: {e}")
        if response is not None:
            try:
              print(f"API response content in Exception:{response.content.decode()}") #Very Important!
            except:
              print(f"Response content could not be printed because decoding failed in exception, verify the connection. , message {e}") #Very Important! Try calling with curl for same date.
        else:
           print(f"Get OrderBook had an Exception, verify the settings or connection..Original exception {e}") # check response. Verify the parameters.
        return None


# --- Main Execution ---
def main():
    """Demonstrates the usage of the A7 Analytics Platform API."""

    print("--- A7 Analytics Platform API Demonstration ---")

    # 1. Get Algo Owners
    print("\n1. Getting Algo Owners:")
    owners_data = get_algo_owners()
    if owners_data and "Owners" in owners_data:
        print(f"Algo Owners: {owners_data['Owners']}")
    else:
        print("Failed to retrieve algo owners.")

    # 2. Get Algos for a Specific Owner
    print("\n2. Getting Algos for Owner:")
    algos_data = get_algos(OWNER, mode="compact")
    if algos_data and "Algos" in algos_data:  # Check for "Algos" key
        print(f"Algos for {OWNER}: {algos_data['Algos']}")
    else:
        print(f"Failed to retrieve algos for owner {OWNER}.")

    # 3. Delete Algo (if it exists)
    print("\n3. Deleting Algo (if it exists):")
    delete_response = delete_algo(OWNER, ALGO_NAME)
    print(delete_response['message'])

    # 4. Upload an Algo
    print("\n4. Uploading Algo:")
    upload_response = upload_algo(OWNER, ALGO_NAME, ALGO_FILE)
    if upload_response and upload_response.get("success"):  # Always check that the return is not None, before accessing it. You have an error check with if-else, use it.
        print(f"Algo uploaded successfully: {upload_response}")
    else:
        print(f"Failed to upload algo {ALGO_NAME}.")
        if upload_response and upload_response.get("message"):
            print(f"Upload Error Message: {upload_response['message']}")  # Show specific error message.

    # 5. Download an Algo
    print("\n5. Downloading Algo:")
    downloaded_algo = download_algo(OWNER, ALGO_NAME)
    if downloaded_algo:
        print(f"Algo source code:\n{downloaded_algo}")
    else:
        print(f"Failed to download algo {ALGO_NAME}.")

    # 6. Run an Algo
    print("\n6. Running Algo:")
    # Example of passing additional parameters
    additional_params = {"aggr": 4, "level": 1}

    run_response = run_algo(OWNER, ALGO_NAME, MARKET_ID, DATA_DATE, MARKET_SEGMENT_ID, SECURITY_ID,
                                         additional_params)

    # 7. Get Transact Times (EOBI Data)
    print("\n7. Getting Transact Times (EOBI):")
    transact_times_data = get_transact_times(MARKET_ID, DATA_DATE, MARKET_SEGMENT_ID, SECURITY_ID)
    if transact_times_data and "TransactTimes" in transact_times_data:
        transact_times = transact_times_data["TransactTimes"]
        print(f"Transact Times: ")
        transact_times = transact_times_data["TransactTimes"]
        print(f"Transact Times: {transact_times[:5]}...")  # Show only the first 5

        if transact_times:
            # Process multiple transact times (e.g., first 15)
            for i, transact_time in enumerate(transact_times[:15]):
                print(f"\nAttempting to get order book for transact_time {i+1}: {transact_time}")
                order_book_data = get_orderbook(MARKET_ID, DATA_DATE, MARKET_SEGMENT_ID, SECURITY_ID, transact_time)

                if order_book_data:  # Check if order_book_data is not None
                  print(f"Order book data was returned getting next set.")
                  break #Success getting data
                else:
                  print(f"Will try next listing, cannot get at {transact_times}.") # if not can get it, proceed on..
        else:
            print("No transact times available, skipping message details retrieval")


    else:
        print("Failed to retrieve transact times.")

if __name__ == "__main__":
    main()
