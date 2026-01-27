import requests
from tabulate import tabulate
import datetime

def fetch_models():
    """Fetches model data from the OpenRouter API."""
    url = "https://openrouter.ai/api/v1/models"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching models: {e}")
        return None

def format_models_table(data):
    """Formats the model data into a human-readable table."""
    if not data or 'data' not in data:
        return "No model data available."

    models = data['data']
    table_data = []
    headers = [
        "ID",
        "Name",
        "Created",
        "Context Length",
        "Modality",
        "Input Modalities",
        "Output Modalities",
        "Tokenizer",
        "Instruct Type",
        "Prompt Price (per 1M tokens)",
        "Completion Price (per 1M tokens)",
        "Request Price",
        "Image Price",
        "Web Search Price",
        "Internal Reasoning Price",
        "Description"
    ]

    for model in models:
        prompt_price = model['pricing']['prompt'] if 'pricing' in model and 'prompt' in model['pricing'] else "N/A"
        completion_price = model['pricing']['completion'] if 'pricing' in model and 'completion' in model['pricing'] else "N/A"

        # Multiply by 1 million if the price is a number
        try:
            prompt_price = float(prompt_price) * 1000000 if prompt_price != "N/A" else "N/A"
            prompt_price = f"{prompt_price:.2f}" if prompt_price != "N/A" else "N/A" # Format to 2 decimal places
        except (ValueError, TypeError):
            pass  # Keep "N/A" if conversion fails

        try:
            completion_price = float(completion_price) * 1000000 if completion_price != "N/A" else "N/A"
            completion_price = f"{completion_price:.2f}" if completion_price != "N/A" else "N/A" # Format to 2 decimal places
        except (ValueError, TypeError):
            pass  # Keep "N/A" if conversion fails

        table_data.append([
            model['id'],
            model['name'],
            model['created'],
            model['context_length'],
            model['architecture']['modality'] if 'architecture' in model and 'modality' in model['architecture'] else "N/A",
            ", ".join(model['architecture']['input_modalities']) if 'architecture' in model and 'input_modalities' in model['architecture'] else "N/A",
            ", ".join(model['architecture']['output_modalities']) if 'architecture' in model and 'output_modalities' in model['architecture'] else "N/A",
            model['architecture']['tokenizer'] if 'architecture' in model and 'tokenizer' in model['architecture'] else "N/A",
            model['architecture']['instruct_type'] if 'architecture' in model and 'instruct_type' in model['architecture'] else "N/A",
            prompt_price,
            completion_price,
            model['pricing']['request'] if 'pricing' in model and 'request' in model['pricing'] else "N/A",
            model['pricing']['image'] if 'pricing' in model and 'image' in model['pricing'] else "N/A",
            model['pricing']['web_search'] if 'pricing' in model and 'web_search' in model['pricing'] else "N/A",
            model['pricing']['internal_reasoning'] if 'pricing' in model and 'internal_reasoning' in model['pricing'] else "N/A",
            model['description']
        ])

    return tabulate(table_data, headers=headers, tablefmt="pipe")  # Use pipe format for readability

def save_table_to_file(table_string):
    """Saves the formatted table string to a file with a timestamp in the filename."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"openrouter-models_{timestamp}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(table_string)
        print(f"Table saved to: {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")

if __name__ == "__main__":
    model_data = fetch_models()
    if model_data:
        table = format_models_table(model_data)
        save_table_to_file(table)
