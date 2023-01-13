import requests
import json
# import related models here
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, SemanticRolesOptions,EntitiesOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from requests.auth import HTTPBasicAuth
from .models import CarDealer,DealerReview

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    api_key=kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = request.get(requests.get(url, params=params, headers={'Content-Type': 'application/json'},auth=HTTPBasicAuth('apikey', api_key)))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    # Retrieve the dealer data from the response
    print("line 55 RA", json_result)
    dealers = json_result
    # For each dealer in the response
    for dealer in dealers:
        # Get its data in `doc` object
        dealer_doc = dealer["doc"]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"])
        results.append(dealer_obj)

    return results
def get_dealer_reviews_from_cf(url, id):
    results = []
    # Perform a GET request with the specified dealer id
    json_result = get_request(url, id=id)
    if json_result:
        #print(json_result)
        # Get all review data from the response
        reviews = json_result["data"]["docs"]
        # For every review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            # These values must be present
            review_content = review["review"]
            id = review["id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealership"]
            car_make = review["car_make"]
            car_model = review["car_model"]
            car_year = review["car_year"]
            purchase_date = review["purchase_date"]
            review_obj = DealerReview(id=id, name=name, dealership=dealership, review=review_content, sentiment=None, purchase=purchase, purchase_date=purchase_date, car_make=car_make, car_model=car_model, car_year=car_year)
            results.append(review_obj)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
    return results

def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            dealerid=dealer_obj.id
            if(dealerid==dealerid):
                results.append(dealer_obj)

    return results 
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54', json_result)
    if json_result:
        dealers = json_result[0]
    print("line 70 restapis",json_result)
    dealer_doc = dealers
    print("0th address element line 73", dealers["address"])
    dealer_obj = CarDealer(address=dealers["address"], city=dealers["city"],id=dealers["id"], lat=dealers["lat"], long=dealers["long"], full_name=dealers["full_name"],short_name=dealers["short_name"], st=dealers["st"], zip=dealers["zip"])
    return dealer_obj
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def analyze_review_sentiments(dealerreview):
    print(dealerreview)
    print(dealerreview)
    print(dealerreview)
    api_key = IAMAuthenticator('7hONHM3lp4AbHSvUJ0Ii41uz0oDy01nciohO6U8Xmtk7')
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=api_key)
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/fc516d31-284d-4459-86d1-9804557e72bd')
    response = natural_language_understanding.analyze(text=dealerreview,features=Features(entities=EntitiesOptions(sentiment=True,limit=1))).get_result()
    print(response["entities"]) 
    return response["entities"]
# Create a get_dealers_from_cf method to get dealers from a cloud function
# ef get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative