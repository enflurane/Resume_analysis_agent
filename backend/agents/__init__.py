from smolagents import OpenAIServerModel, LiteLLMModel
from ..config import settings

def get_model(model_name: str = None):
    if model_name is None:
        model_name = settings.MODEL_NAME
    api_key = settings.API_KEY
    base_url = settings.BASE_URL
    
    return LiteLLMModel(
        model_id=f'openai/{model_name}',
        api_key=api_key,
        api_base=base_url,
        enable_thinking=True
    )
