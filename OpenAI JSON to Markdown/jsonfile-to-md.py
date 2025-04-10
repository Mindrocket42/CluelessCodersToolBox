import json
# from datetime import datetime # Removed
from pathlib import Path
# import os # Removed import

def process_json_file(filepath):
    # Ensure filepath is a Path object
    filepath = Path(filepath)
    # Read JSON file with UTF-8 encoding
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check for nested 'payload' structure first
    payload = data.get('payload')
    if isinstance(payload, dict):
        # Use payload for messages and settings
        source_data = payload
        # Model might still be at the top level or within payload
        model = data.get('model', source_data.get('model', 'Unknown Model'))
        # Settings are likely within payload
        settings = {
            'temperature': source_data.get('temperature', 'N/A'),
            'max_completion_tokens': source_data.get('max_completion_tokens', 'N/A'),
            'top_p': source_data.get('top_p', 'N/A'),
            'frequency_penalty': source_data.get('frequency_penalty', 'N/A'),
            'presence_penalty': source_data.get('presence_penalty', 'N/A')
        }
        messages = source_data.get('messages', [])
    else:
        # Fallback to top-level structure (original assumption)
        source_data = data
        model = source_data.get('model', 'Unknown Model')
        settings = {
            'temperature': source_data.get('temperature', 'N/A'),
            'max_completion_tokens': source_data.get('max_completion_tokens', 'N/A'),
            'top_p': source_data.get('top_p', 'N/A'),
            'frequency_penalty': source_data.get('frequency_penalty', 'N/A'),
            'presence_penalty': source_data.get('presence_penalty', 'N/A')
        }
        messages = source_data.get('messages', [])

    # Format the content
    content = [
        f"# Conversation with {model}\n",
        "## Model Settings",
        f"- Temperature: {settings['temperature']}",
        f"- Max Completion Tokens: {settings['max_completion_tokens']}",
        f"- Top P: {settings['top_p']}",
        f"- Frequency Penalty: {settings['frequency_penalty']}",
        f"- Presence Penalty: {settings['presence_penalty']}\n",
        "## Conversation\n"
    ]

    # Process messages with clear role labels
    for msg in messages:
        role = msg.get('role', 'unknown').upper()
        # Handle different roles slightly differently for clarity
        if role == "USER":
            content.append(f"### 👤 USER")
        elif role == "ASSISTANT":
            content.append(f"### 🤖 ASSISTANT")
        elif role == "SYSTEM":
             content.append(f"### ⚙️ SYSTEM") # Handle SYSTEM role
        else:
            content.append(f"### {role}") # Fallback for other roles

        # Get message content - could be string or list
        msg_content = msg.get('content')

        if isinstance(msg_content, str):
            # If content is a simple string
            if msg_content:
                content.append(msg_content.strip()) # Append the string content
        elif isinstance(msg_content, list):
            # If content is a list of items (original assumption)
            for item in msg_content:
                item_type = item.get('type', '')
                if item_type == 'text':
                    text = item.get('text', '')
                    if text:
                        content.append(text.strip())
                elif item_type.startswith('image'):
                    content.append("*[Image attached]*")
        # Else: Handle other potential content types or ignore

        content.append("\n---\n")  # Add separator between messages

    # Generate output filename using source filename (same directory)
    output_file = filepath.with_suffix(".md")

    # Save content with UTF-8 encoding
    output_file.write_text('\n'.join(content), encoding='utf-8')
    print(f"Processed '{filepath.name}' and saved to: {output_file.name}")

if __name__ == "__main__":
    # Get the directory where the script is located or CWD as fallback
    try:
        script_dir = Path(__file__).parent.resolve() # Use resolve() for absolute path
    except NameError:
        script_dir = Path('.').resolve()
        print(f"Warning: Could not determine script's absolute directory, using current working directory: {script_dir}")

    print(f"Scanning for JSON files in: {script_dir}")
    # Find all JSON files in the script's directory
    json_files = list(script_dir.glob('*.json'))

    if not json_files:
        print("No JSON files found in the directory.")
    else:
        print(f"Found {len(json_files)} JSON file(s). Checking for corresponding Markdown files...")

    converted_count = 0
    skipped_count = 0

    for json_filepath in json_files:
        # Construct the expected markdown filepath
        md_filepath = json_filepath.with_suffix('.md')

        # Check if the markdown file already exists
        if not md_filepath.exists():
            print(f"Found '{json_filepath.name}'. Corresponding '.md' file missing. Converting...")
            try:
                process_json_file(json_filepath)
                converted_count += 1
            except Exception as e:
                print(f"Error processing {json_filepath.name}: {e}")
        else:
            # Optional: print skipping message
            # print(f"Skipping '{json_filepath.name}', corresponding markdown file '{md_filepath.name}' already exists.")
            skipped_count += 1

    print(f"\nConversion process complete.")
    print(f"Successfully converted {converted_count} new JSON file(s).")
    if skipped_count > 0:
      print(f"Skipped {skipped_count} JSON file(s) as corresponding Markdown files already exist.")