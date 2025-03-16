import requests
from smolagents.tools import tool
from smolagents import ToolCallingAgent
from smolagents.models import LiteLLMModel
from sklearn.metrics.pairwise import cosine_similarity
import litellm
import numpy as np
import json
from datetime import datetime
# levenshtein distance
import Levenshtein

endpoint_gpt = "https://ai-hackathonuabpayretailers082809715538.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-21"
api_key_gpt = "6evUUU8hO6Z13XrWLqupolcAtbxiOdCiw0LBeu2prfMuqEd33BwUJQQJ99BCACYeBjFXJ3w3AAAAACOGQmQt"

endpoint_embs = "https://ai-hackathonuabpayretailers082809715538.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"
api_key_embs = "6evUUU8hO6Z13XrWLqupolcAtbxiOdCiw0LBeu2prfMuqEd33BwUJQQJ99BCACYeBjFXJ3w3AAAAACOGQmQt"


def get_embedding(text): # str or list
	headers = {
		"Content-Type": "application/json",
		"api-key": api_key_embs,
	}
	data = {
		"input": text,
		"model": "text-embedding-ada-002",
	}
	response = requests.post(endpoint_embs, headers=headers, json=data)
	response.raise_for_status()  # Raise an error for bad responses
	
	# Handle both single string and list of strings
	if isinstance(text, list):
		return [item["embedding"] for item in response.json()["data"]]
	else:
		return response.json()["data"][0]["embedding"]

def make_request(url, headers=None, params=None):
	response = requests.get(url, headers=headers, params=params)
	response.raise_for_status()  # Raise an error for bad responses
	return response.json()

def prompt_gpt(prompt, temperature=0.7) -> str:
	headers = {
		"Content-Type": "application/json",
		"api-key": api_key_gpt,
	}
	data = {
		"model": "gpt-4o-mini",
		"messages": [{"role": "user", "content": prompt}],
		"temperature": temperature,
	}
	response = requests.post(endpoint_gpt, headers=headers, json=data)
	response.raise_for_status()  # Raise an error for bad responses
	return response.json()["choices"][0]["message"]["content"]

def update_last_queries(last_queries: list, new_query: dict, max_size: int = 30):
	last_queries = [new_query] + last_queries
	if len(last_queries) > max_size:
		last_queries = last_queries[:max_size]
	return last_queries

def get_closer_string(query: str, possible_values: list) -> str:
	min_distance = float("inf")
	closest_string = ""
	for value in possible_values:
		distance = Levenshtein.distance(query, value)
		if distance < min_distance:
			min_distance = distance
			closest_string = value
	return closest_string

def get_key(possible_values, id):
	for area in possible_values:
		for key, value in possible_values[area].items():
			if id == value:
				return key

# @tool
# def get_health_information(query: str) -> str:
#     """
#     Retrieves health information from the WHO ICD API based on the provided query.
    
#     Args:
#         query (str): The search term or health condition to look up in the ICD database
        
#     Returns:
#         str: JSON response from the ICD API containing health information
#     """
#     # Token endpoint and credentials
#     token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
#     client_id = '8caa6a12-6a0c-42ad-8d01-1c0df86aff21_8d1f0335-1aa2-442f-98f3-e25bcd008972'
#     client_secret = 'i7EfJLFL/bRZfYQZvipLCT/IIuqY5nSJKcJyQ5K/JLw='
#     scope = 'icdapi_access'
#     grant_type = 'client_credentials'
#     # Obtain the OAuth2 token
#     payload = {
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'scope': scope,
#         'grant_type': grant_type
#     }
#     response = requests.post(token_endpoint, data=payload, verify=True)
#     response.raise_for_status()  # Ensure the request was successful
#     token = response.json().get('access_token')
#     if not token:
#         raise Exception("Failed to retrieve access token")
#     # ICD API endpoint
#     uri = 'https://id.who.int/icd/entity/search'
#     # HTTP headers
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Accept': 'application/json',
#         'Accept-Language': 'es',
#         'API-Version': 'v2',
#         'useFlexisearch': 'true'
#     }
#     # Query parameters
#     params = {
#         'q': query,
#         'useFlexisearch': 'true',
#         'propertiesToBeSearched': 'Definition',
#     }
#     # Make the request
#     response = requests.get(uri, headers=headers, params=params, verify=True)
#     response.raise_for_status()  # Ensure the request was successful
#     # Print the result
#     #print(response.json())
   
#     parsing = response.json()
#     answer = ""
    
#     answer += f"Resultados de la busqueda por {query}\n"
#     for i in range(len(parsing['destinationEntities'])):
#         answer += "\nTitle: " + parsing['destinationEntities'][i]['title'] + "\nDefinition: " + parsing['destinationEntities'][i]['matchingPVs'][0]['label'] + "\n"
    

#     return answer

@tool
def find_relevant_stat(query: str) -> str:
	"""
	Finds the relevant statistic for a given user query, retrieves some data points related to the query and user personal information, and generates an answer using the GPT model.
	
	Args:
		query (str): The user query
	
	Returns:
		str: The generated answer from the GPT model
	"""
	query_emb = get_embedding(query)
	database_embs = np.load("cepalstat_stats.npy")
	# calculate cosine similarity
	query_emb = np.array(query_emb).reshape(1, -1)
	similarity = cosine_similarity(query_emb, database_embs)
	# get the index of the most similar statistic
	index = np.argmax(similarity)
	# get the id of the most similar statistic
	with open("cepalstat_names.json", "r") as file:
		data = json.load(file)
	ids = data["ids"]
	names = data["names"]
	indicator_id = ids[index]
	indicator_name = names[index]

	# retrieve the dimensions of the statistic
	response = make_request(f"https://api-cepalstat.cepal.org/cepalstat/api/v1/indicator/{indicator_id}/dimensions", headers={"accept": "application/json"}, params={"in": 1})
	dimensions = response["body"]["dimensions"]
	dimensions_names = [dimension["name"] for dimension in dimensions]
	dimensions_ids = [dimension["id"] for dimension in dimensions]
	possible_values = {}
	for dimension in dimensions:
		dimension_name = dimension["name"]
		members = dimension["members"]
		members_names = [member["name"] for member in members]
		members_ids = [member["id"] for member in members]
		possible_values[dimension_name] = dict(zip(members_names, members_ids))

	# read memory
	with open("memory.json", "r") as file:
		memory = json.load(file)

	# fill dimension values
	dimensions_values = {key: None for key in dimensions_names}
	# for dimension_name in dimensions_names:
	# 	if "country" in dimension_name.lower() and memory["country"] is not None:
	# 		dimensions_values[dimension_name] = [memory["country"]]
	# 	elif "sex" in dimension_name.lower() and memory["sex"] is not None:
	# 		dimensions_values[dimension_name] = [memory["sex"]]
	
	none_values = {key: value for key, value in dimensions_values.items() if value is None}
	print("none_values:", none_values)
	current_date = datetime.now()
	formated_date = current_date.strftime("%d-%m-%Y")
	if len(none_values) > 0:
		# make gpt-4o-mini suggest values
		possible_values_prompt = {key: list(value.keys()) for key, value in possible_values.items()}
		prompt = f"A statistic must be retrieved related to {indicator_name}, but we need first to fill in the values for the dimensions: {list(none_values.keys())}. Given that the original user query was: {query}, today is {formated_date}, and the user information is: {memory}, suggest values for the dimensions in the form of string or list of strings. For the dimension \"Years__ESTANDAR\", it is accepted in the form of list of years if the query asks for a period of time explicitly or implicitly (e.g. if the user says \"recently\" we could pick the last five years). Also, multiple countries can be specified. The values must be one of the following possible values: {possible_values_prompt}. In case the value is not present in the possible values set the value to \"null\". In case no value can be inferred from the given information, set the value to \"null\". Provide only the values in a dictionary format (without prefix json) with the keys as the dimension names and the values as the suggested values. Do not add any other text."
		print("prompt:", prompt)
		response2 = prompt_gpt(prompt)
		print("response2:", response2)
		# parse the response
		response2 = json.loads(response2)
		# fill the dimensions values
		for key in none_values.keys():
			if key in response2.keys() and response2[key] is not None:
				response_values = response2[key]
				if isinstance(response2[key], str):
					response_values = [response_values]
				response_values = [get_closer_string(value, possible_values[key]) for value in response_values]
				dimensions_values[key] = response_values
			else:
				dimensions_values[key] = None
		print("dimensions_values:", dimensions_values)
		print("dimensions_names:", dimensions_names)
		print("possible_values:", possible_values)
	
	dimensions_values_ids = []
	for key in dimensions_names:
		if dimensions_values[key] is not None and dimensions_values[key] != ["null"]:
			ks = dimensions_values[key]
			for k in ks:
				print(possible_values[key], key, k)
				dimensions_values_ids.append(str(possible_values[key][k]))
	members = ",".join(map(str,dimensions_values_ids))
	print("members:", members)
	print("indicator_id", indicator_id)

	response3 = make_request(f"https://api-cepalstat.cepal.org/cepalstat/api/v1/indicator/{indicator_id}/data", params={"members": members})
	print("response3:", response3["body"]["data"])

	prompt2 = "System prompt: Avoid answering without context information or without being provided some minimum information to answer.\n"
	prompt2 += f"Query: {query}\nContext:\n{indicator_name}:\n"
	for point in response3["body"]["data"]:
		value = point["value"]
		ids = [val for key,val in point.items() if key not in ("value", "source_id", "notes_ids", "iso3")]
		dims = [get_key(possible_values, id) for id in ids]
		dims_str = ", ".join(dims)
		prompt2 += f"{dims_str}: {value}\n"

	prompt2 += f"User information:\n{memory}"
	print("prompt2:", prompt2)
	response4 = prompt_gpt(prompt2)

	# save memory
	memory["last_queries"] = update_last_queries(memory["last_queries"], {"query": query, "answer": response4})
	with open("memory.json", "w") as file:
		json.dump(memory, file)

	return response4
