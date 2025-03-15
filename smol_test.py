from smolagents.tools import tool
from smolagents import ToolCallingAgent
from smolagents.models import LiteLLMModel
import litellm
from api_tools import get_health_information

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
agent = ToolCallingAgent(tools=[get_health_information], model=model)

# Run the agent
print(agent.run("Como es la tendencia de paro últimamente?"))
