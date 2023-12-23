from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.shortcuts import render 
from .ML_helper import predict_with_saved_model

def home_view(request): 
      
    # render function takes argument  - request 
    # and return HTML as response 
    return render(request, "home.html") 

@csrf_exempt
@require_POST
def dialogflow_webhook(request):
    req_data = json.loads(request.body)
    # print("Request data:", req_data)

    intent_name = req_data.get('queryResult', {}).get('intent', {}).get('displayName', '')
    parameters = req_data.get('queryResult', {}).get('parameters', {})
    contexts = req_data.get('queryResult', {}).get('outputContexts', [])

    # Extract parameters from contexts
    context_params = {}
    for context in contexts:
        if 'parameters' in context:
            context_params.update(context['parameters'])

    county = context_params.get('County', '')
    amount = context_params.get('Amount', '')
    time = context_params.get('Time', '')

    # Handling missing data
    def is_data_missing():
        return not county or not amount or not time

    # Initialize default response
    response_text = "Unknown intent."

    # Intent handling logic
    if intent_name == 'GetCounty':
        response_text = f"Received county information: {county}. What is the amount?"

    elif intent_name == 'GetAmount':
        response_text = f"Received amount: {amount}. How many years are you looking to invest for?"

    elif intent_name == 'GetYears':
        if is_data_missing():
            # Prompt for missing data
            missing_data_message = "I still need the following information: "
            missing_data_message += "County, " if not county else ""
            missing_data_message += "Amount, " if not amount else ""
            missing_data_message += "Years" if not time else ""
            response_text = missing_data_message.strip(", ")
        else:
            # All data present, proceed with final processing
            top_zip_codes = predict_with_saved_model(model_path='saved_models_smol.pkl', county=county, budget=amount, forecast_years=time, dataset_path='data/zillow_data.csv')
            # print(top_zip_codes)
            response_text = "Here are the top 5 zip codes with their forecasted increase (/100) \n"
            response_text += str(top_zip_codes)

    return JsonResponse({"fulfillmentText": response_text})


