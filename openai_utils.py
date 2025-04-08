from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Retrieve the OpenAI API key from the environment variables
CLIENT = OpenAI(api_key=OPENAI_API_KEY)  # Initialize the OpenAI client with the API key

def check_args_validity(selected_model, temperature):
    """
    Checks if the provided model is a valid OpenAI model.
    Args:
        selected_model (str): The model ID to validate.
        temperature (float): The temperature for randomness.
    Returns:
        bool: True if the model is valid, False otherwise.
    """
    try:
        if temperature < 0 or temperature > 2:  # Check if the temperature is within the valid range
            print('Temperature must be between 0 and 2')
            return False 
        models_list = CLIENT.models.list()  # Retrieve the list of available models from the OpenAI API
        for model in models_list.data:  # Iterate through the list of models
            if model.id == selected_model:  # Check if the provided model ID matches any of the available models
                return True  # Return True if the model is found
    except Exception as e:  # Catch any exceptions that occur during the API call
        print(e)  # Print the error message
        return False  # Return False if an error occurred
    print('Invalid model/Model not found') # Print message to user if model is invalid.
    return False  # Return False if the model was not found

    
def __get_response(prompt, model, temperature=0.5):
    """
    Gets a response from the OpenAI API.
    Args:
        prompt (str): The prompt to send to the API.
        model (str): The model to use for the API call.
    Returns:
        openai.types.responses.response.Response: The API response.
    """
    response = CLIENT.responses.create(  # Make an API call to get a response
        model= model,  # Specify the model to use
        input= prompt,  # Specify the prompt
        temperature=temperature,  # Set the temperature for randomness
    )
    return response  # Return the API response

def summarize_and_highlight(text, model, temperature):
    """
    Summarizes a contract and highlights important terms.
    Args:
        text (str): The contract text.
        model (str): The model to use.
    Returns:
        openai.types.responses.response.Response: The API response containing the summary and highlights.
    """
    prompt = f"Summarize the following contract and highlight key terms and conditions. Add an appendex that explains any included legal terms:\n{text}"  # Construct the prompt
    return __get_response(prompt, model, temperature)  # Get the API response

def extract_data(text, model, temperature):
    """
    Extracts numerical data from a contract.
    Args:
        text (str): The contract text.
        model (str): The model to use.
    Returns:
        openai.types.responses.response.Response: The API response containing the extracted data.
    """
    prompt = f"Extract important numerical data, if any, from the following contract and summarize. If there is no data, only return 'no_data':\n{text}"  # Construct the prompt
    return __get_response(prompt, model, temperature)  # Get the API response

def assess_risk(text, model, temperature):
    """
    Assesses the risk of a contract.
    Args:
        text (str): The contract text.
        model (str): The model to use.
    Returns:
        openai.types.responses.response.Response: The API response containing the risk assessment.
    """
    prompt = f"Assess the risk of the following contract on a scale of 1-10 and explain your reasoning:\n{text}"  # Construct the prompt
    return __get_response(prompt, model, temperature)  # Get the API response

def assess_deal(text, model, temperature):
    """
    Assesses if a contract is a good deal.
    Args:
        text (str): The contract text.
        model (str): The model to use.
    Returns:
        openai.types.responses.response.Response: The API response containing the deal assessment.
    """
    prompt = f"Assess if the following contract is a good deal on a scale of 1-10 and explain your reasoning:\n{text}"  # Construct the prompt
    return __get_response(prompt, model, temperature)  # Get the API response