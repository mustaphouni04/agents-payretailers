from smolagents.tools import tool
from smolagents import ToolCallingAgent
from smolagents.models import LiteLLMModel
import litellm
from api_tools import find_relevant_stat, maps_instruction, legal_assistance, browser
import json

litellm.drop_params = True

# Azure OpenAI credentials (replace these with your actual values)
AZURE_OPENAI_API_KEY = "6evUUU8hO6Z13XrWLqupolcAtbxiOdCiw0LBeu2prfMuqEd33BwUJQQJ99BCACYeBjFXJ3w3AAAAACOGQmQt"
AZURE_OPENAI_ENDPOINT = "https://ai-hackathonuabpayretailers082809715538.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-12-01-preview"
AZURE_DEPLOYMENT_NAME = "gpt-4o-mini"  # Set this to your deployed model's name

# Use LiteLLMModel with Azure openai
model = LiteLLMModel(
    model_id=f"azure/{AZURE_DEPLOYMENT_NAME}",
    api_key=AZURE_OPENAI_API_KEY,
    base_url=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview",
    # Add the API version
)

# Create the agent with the updated model
agent = ToolCallingAgent(tools=[find_relevant_stat, browser, legal_assistance], model=model)

def answer_question(question):
	with open("memory.json", "r") as f:
		memory = json.load(f)
	user_info = {key: val for key,val in memory.items() if key != "last_queries"}
	last_query = memory["last_queries"][0] if len(memory["last_queries"]) > 0 else "None"
	prompt = f"User info: {user_info}\n"
	prompt += f"History of questions: {last_query}\n"
	prompt += f"Question: {question}"
	return agent.run(prompt)

if __name__ == "__main__":
	# Run the agent
	print(answer_question("Tengo que renovar mi carne de conducir, ¿que debo hacer?"))

	# Cuales són los valores de la deuda pública de mi pais en la ultima década?
	# Como esta la deuda pública de mi pais comparado con la de Perú?
	# Como ha subido el precio de la gasolina en los ultimos años?
