import requests
from smolagents.tools import tool
from smolagents import ToolCallingAgent
from smolagents.models import LiteLLMModel
from sklearn.metrics.pairwise import cosine_similarity
import litellm
import numpy as np
import json
import os
from datetime import datetime
# levenshtein distance
import Levenshtein
import asyncio
from browser_use import Agent
from langchain_openai import AzureChatOpenAI


AZURE_OPENAI_ENDPOINT = ""
AZURE_OPENAI_API_KEY = ""
AZURE_DEPLOYMENT_NAME = "" 

AZURE_OPENAI_ENDPOINT_EMBS = ""
AZURE_OPENAI_API_KEY_EMBS = ""


def extract_json_from_file(file_path):
    """Extracts JSON objects from a file."""
    extracted_json = []
    collecting_json = False
    json_lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if line == "RESPONSE":
                collecting_json = True
                json_lines = []  # Reset JSON lines

            elif collecting_json:
                json_lines.append(line)
                # Attempt to parse once we have a full JSON object
                try:
                    json_data = json.loads("\n".join(json_lines))
                    extracted_json.append(json_data)
                    collecting_json = False  # Stop collecting once successful
                except json.JSONDecodeError:
                    pass  # Keep collecting until we have valid JSON

    return extracted_json

def find_conversation_with_highest_number(logs_directory):
    """Finds the conversation with the highest index 'i' in conversation_i.txt files."""
    highest_index = -1
    highest_file_path = None
    
    # First, find the file with the highest index
    for filename in os.listdir(logs_directory):
        if filename.startswith("conversation_") and filename.endswith(".txt"):
            try:
                # Extract the index number from the filename
                index = int(filename.replace("conversation_", "").replace(".txt", ""))
                if index > highest_index:
                    highest_index = index
                    highest_file_path = os.path.join(logs_directory, filename)
            except ValueError:
                # Skip files that don't have a proper number format
                continue
    
    # If we found a file with valid index, extract the JSON from it
    if highest_file_path:
        print(f"Found highest indexed file: {highest_file_path} with index {highest_index}")
        extracted_data = extract_json_from_file(highest_file_path)
        return extracted_data
    
    return None


def get_embedding(text): # str or list
	headers = {
		"Content-Type": "application/json",
		"api-key": AZURE_OPENAI_API_KEY_EMBS,
	}
	data = {
		"input": text,
		"model": "text-embedding-ada-002",
	}
	response = requests.post(AZURE_OPENAI_ENDPOINT_EMBS, headers=headers, json=data)
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
		"api-key": AZURE_OPENAI_API_KEY,
	}
	data = {
		"model": "gpt-4o-mini",
		"messages": [{"role": "user", "content": prompt}],
		"temperature": temperature,
	}
	response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=data)
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
	Finds the relevant statistic for a given user query, retrieves some data points related to the query and user personal information, and generates an answer using the GPT model. If the user didn't specify a country, do not infer it, this function will do so. If the user did specify a country or more, mention it.
	
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
	print("-"*50)
	print("Searching information for:", indicator_name)

	# retrieve the dimensions of the statistic
	response = make_request(f"https://api-cepalstat.cepal.org/cepalstat/api/v1/indicator/{indicator_id}/dimensions", headers={"accept": "application/json"}, params={"in": 1})
	dimensions = response["body"]["dimensions"]
	dimensions_names = [dimension["name"] for dimension in dimensions]
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
	# print("none_values:", none_values)
	current_date = datetime.now()
	formated_date = current_date.strftime("%d-%m-%Y")
	if len(none_values) > 0:
		# make gpt-4o-mini suggest values
		possible_values_prompt = {key: list(value.keys()) for key, value in possible_values.items()}
		prompt = f"A statistic must be retrieved related to {indicator_name}, but we need first to fill in the values for the dimensions: {list(none_values.keys())}. Given that the original user query was: {query}, today is {formated_date}, and the user information is: {memory}, suggest values for the dimensions in the form of string or list of strings. For the dimension \"Years__ESTANDAR\", it is accepted in the form of list of years if the query asks for a period of time explicitly or implicitly (e.g. if the user says \"recently\" we could pick the last five years). Also, multiple countries can be specified. The values must be one of the following possible values: {possible_values_prompt}. In case the value is not present in the possible values set the value to \"null\". In case no value can be inferred from the given information, set the value to \"null\". Provide only the values in a dictionary format (without prefix json) with the keys as the dimension names and the values as the suggested values. Do not add any other text."
		# print("prompt:", prompt)
		response2 = prompt_gpt(prompt)
		# print("response2:", response2)
		# parse the response
		response2 = json.loads(response2)
		# fill the dimensions values
		for key in none_values.keys():
			if key in response2.keys() and response2[key] is not None:
				response_values = response2[key]
				if key == "Years__ESTANDAR" and int(response_values[-1]) > int(list(possible_values[key].keys())[-1]):
					diff = int(response_values[-1]) - int(list(possible_values[key].keys())[-1])
					response_values = [str(int(value) - diff) for value in response_values]
					print("Corrected response_values:", response_values)
				if isinstance(response2[key], str):
					response_values = [response_values]
				for value in response_values:
					print("possible_values[key]", list(possible_values[key].keys()))
					print("value", value)
					print("get_closer_string(value, possible_values[key])", get_closer_string(value, list(possible_values[key].keys())))
				response_values = [get_closer_string(value, list(possible_values[key].keys())) for value in response_values]
				dimensions_values[key] = response_values
			else:
				dimensions_values[key] = None
		# print("dimensions_values:", dimensions_values)
		# print("dimensions_names:", dimensions_names)
		# print("possible_values:", possible_values)
	
	dimensions_values_ids = []
	for key in dimensions_names:
		if dimensions_values[key] is not None and dimensions_values[key] != ["null"]:
			ks = dimensions_values[key]
			for k in ks:
				print(possible_values[key], key, k)
				dimensions_values_ids.append(str(possible_values[key][k]))
	members = ",".join(map(str,dimensions_values_ids))
	# print("members:", members)
	# print("indicator_id", indicator_id)

	response3 = make_request(f"https://api-cepalstat.cepal.org/cepalstat/api/v1/indicator/{indicator_id}/data", params={"members": members})
	# print("response3:", response3["body"]["data"])

	prompt2 = "System prompt: Avoid answering without context information or without being provided some minimum information to answer.\n"
	prompt2 += f"Query: {query}\nContext:\n{indicator_name}:\n"
	for point in response3["body"]["data"]:
		value = point["value"]
		ids = [val for key,val in point.items() if key not in ("value", "source_id", "notes_ids", "iso3")]
		dims = [get_key(possible_values, id) for id in ids]
		dims_str = ", ".join(dims)
		prompt2 += f"{dims_str}: {value}\n"

	prompt2 += f"User information:\n{memory}"
	# print("prompt2:", prompt2)
	response4 = prompt_gpt(prompt2)

	# save memory
	memory["last_queries"] = update_last_queries(memory["last_queries"], {"query": query, "answer": response4})
	with open("memory.json", "w") as file:
		json.dump(memory, file)

	return response4

@tool
def maps_instruction(query: str) -> str:
    """
    Uses Bing Maps to find information based on the user query.
    
    Args:
        query: The user's query about locations, directions, or travel information, translated to English.
        
    Returns:
        String containing the response with maps information
    """
    async def main(query: str):
        """Runs the AI agent to answer a user query."""
        agent = Agent(
            task=f"Go to Bing Maps and help the user with this instruction: {query}",
            llm=AzureChatOpenAI(
                model="gpt-4o-mini", 
                api_version="2024-02-15-preview",
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY
            ),
            save_conversation_path='logs/conversation',
        )
        
        await agent.run()

    # Run the AI agent
    asyncio.run(main(query))

    # Process logs and find highest-number conversation
    logs_directory = 'logs'
    highest_conversation = find_conversation_with_highest_number(logs_directory)

    if highest_conversation:
        return str(highest_conversation)
    else:
        print("No conversation found.")

@tool
def browser(query: str) -> str:
    """
    Uses Google search to answer the user query.
    
    Args:
        query: The user's query about anything.
        
    Returns:
        String containing the response
    """
    async def main(query: str):
        """Runs the AI agent to answer a user query."""
        agent = Agent(
            task=f"Find a quick answer to the user query: {query}. Don't stop until you find enough information to answer.",
            llm=AzureChatOpenAI(
                model="gpt-4o", 
                api_version="2024-02-15-preview",
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY
            ),
            save_conversation_path='logs/conversation',
        )
        
        await agent.run()

    # Run the AI agent
    asyncio.run(main(query))

    # Process logs and find highest-number conversation
    logs_directory = 'logs'
    highest_conversation = find_conversation_with_highest_number(logs_directory)

    if highest_conversation:
        return str(highest_conversation)
    else:
        print("No conversation found.")

@tool
def legal_assistance(query: str) -> str:
    """
    Uses a browser tool to return instructions on how to fill forms and paper work related to the legal cases.
    
    Args:
        query: The user's query about passport renovation, documentation filling...
        
    Returns:
        Visits the webs the user wants to fill the forms and gives a detailed report on how to fill them up.
    """ 

    async def main(query: str):
        """Runs the AI agent to answer a user query."""
        agent = Agent(
            task=f"Ayuda al usuario con esta instrucción: {query}. No hace falta que rellenes formulario, simplemente accede a la pagina y explica los pasos que veas necesarios.",
            llm=AzureChatOpenAI(
                model="gpt-4o-mini", 
                api_version="2024-02-15-preview",
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY
            ),
            save_conversation_path='logs/conversation',
        )
        
        await agent.run()


    # Run the AI agent
    asyncio.run(main(query))

    # Process logs and find highest-number conversation
    logs_directory = 'logs'
    highest_conversation = find_conversation_with_highest_number(logs_directory)

    if highest_conversation:
        return str(highest_conversation)
    else:
        print("No conversation found.")
