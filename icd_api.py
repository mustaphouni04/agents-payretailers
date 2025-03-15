import requests
from smolagents.tools import tool
from smolagents import ToolCallingAgent
from smolagents.models import LiteLLMModel
import litellm

@tool
def get_health_information(query: str) -> str:
    """
    Retrieves health information from the WHO ICD API based on the provided query.
    
    Args:
        query (str): The search term or health condition to look up in the ICD database
        
    Returns:
        str: JSON response from the ICD API containing health information
    """
    # Token endpoint and credentials
    token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
    client_id = '8caa6a12-6a0c-42ad-8d01-1c0df86aff21_8d1f0335-1aa2-442f-98f3-e25bcd008972'
    client_secret = 'i7EfJLFL/bRZfYQZvipLCT/IIuqY5nSJKcJyQ5K/JLw='
    scope = 'icdapi_access'
    grant_type = 'client_credentials'
    # Obtain the OAuth2 token
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': grant_type
    }
    response = requests.post(token_endpoint, data=payload, verify=True)
    response.raise_for_status()  # Ensure the request was successful
    token = response.json().get('access_token')
    if not token:
        raise Exception("Failed to retrieve access token")
    # ICD API endpoint
    uri = 'https://id.who.int/icd/entity/search'
    # HTTP headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Accept-Language': 'es',
        'API-Version': 'v2',
        'useFlexisearch': 'true'
    }
    # Query parameters
    params = {
        'q': query,
        'useFlexisearch': 'true',
        'propertiesToBeSearched': 'Definition',
    }
    # Make the request
    response = requests.get(uri, headers=headers, params=params, verify=True)
    response.raise_for_status()  # Ensure the request was successful
    # Print the result
    #print(response.json())
   
    parsing = response.json()
    answer = ""
    
    answer += f"Resultados de la busqueda por {query}\n"
    for i in range(len(parsing['destinationEntities'])):
        answer += "\nTitle: " + parsing['destinationEntities'][i]['title'] + "\nDefinition: " + parsing['destinationEntities'][i]['matchingPVs'][0]['label'] + "\n"
    

    return answer


def cepal_statistics(statistic: str, country: str):
    break

