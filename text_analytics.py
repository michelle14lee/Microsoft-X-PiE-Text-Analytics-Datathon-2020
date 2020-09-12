import os
import requests
from pprint import pprint
import pandas as pd

# Fill in your credentials
subscription_key = ...
endpoint = ...

"""
The code in this section isn't required, unless you want to hide your subscription credentials from the public. 
Look into python-dotenv for more information.
authenticate_client() uses the Text Analytics SDK to create a client

# from dotenv import load_dotenv
# load_dotenv()
# subscription_key = os.getenv('SUBSCRIPTION_KEY')
# endpoint = os.getenv('ENDPOINT')

# def authenticate_client():
#     ta_credential = AzureKeyCredential(subscription_key)
#     text_analytics_client = TextAnalyticsClient(
#             endpoint= endpoint, credential=ta_credential)
#     return text_analytics_client
"""

def sentiment_analysis_example(documents):
    sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(sentiment_url, headers=headers, json=documents)
    sentiments = response.json()

    print("Printing sentiments ... \n")
    pprint(sentiments)
    return sentiments


def extract_key_phrases(documents):
    keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(keyphrase_url, headers=headers, json=documents)
    key_phrases = response.json()

    print("Printing key phrases ... \n")
    pprint(key_phrases)
    return key_phrases


def identify_entities(documents):
    entities_url = endpoint + "/text/analytics/v3.0/entities/recognition/general"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(entities_url, headers=headers, json=documents)
    entities = response.json()
    pprint(entities)


def convert_text_to_JSON(data):
    """
    Convert text data to the format required by the
    Text Analytics API. Example format included below in the main function.
    """
    pass


def parse_output(output_JSON):
    """
    Convert the response body from the API request to
    select the values you want.
    """
    pass


if __name__ == "__main__":
    """
    Read in your data here and call the functions above.
    You'll likely do a bulk of your coding here.

    - `documents`: an example of the required input format by the Text Analytics API
    """

    documents = {"documents": [
        {"id": "1", "language": "en",
            "text": "I do not like this hammer made by Black & Decker. It does not work correctly. I want to request a return."},
        {"id": "2", "language": "es",
            "text": "I've been trying to talk to someone about my sink problem. It won't hold all of my fish."}
    ]}

    # Uncomment the line below if you choose to use the SDK in the future
    # client = authenticate_client()
    sentiments = sentiment_analysis_example(documents)
    key_phrases = extract_key_phrases(documents)
    entities = identify_entities(documents)

