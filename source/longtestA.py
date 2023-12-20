import os
import openai
import tiktoken

# Set up your OpenAI API key
# Load your API key from an environment variable or secret management service

openai.api_key = "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"

def send(prompt=None, text_data=None, chat_model="gpt-3.5-turbo", model_token_limit=8192, max_tokens=2500,):
    """
    Send the prompt at the start of the conversation and then send chunks of text_data to ChatGPT via the OpenAI API.
    If the text_data is too long, it splits it into chunks and sends each chunk separately.

    Args:
    - prompt (str, optional): The prompt to guide the model's response.
    - text_data (str, optional): Additional text data to be included.
    - max_tokens (int, optional): Maximum tokens for each API call. Default is 2500.

    Returns:
    - list or str: A list of model's responses for each chunk or an error message.
    """

    # Check if the necessary arguments are provided
    if not prompt:
        return "Error: Prompt is missing. Please provide a prompt."
    if not text_data:
        return "Error: Text data is missing. Please provide some text data."

    # Initialize the tokenizer
    tokenizer = tiktoken.encoding_for_model(chat_model)

    # Encode the text_data into token integers
    token_integers = tokenizer.encode(text_data)

    # Split the token integers into chunks based on max_tokens
    chunk_size = max_tokens - len(tokenizer.encode(prompt))
    chunks = [
        token_integers[i : i + chunk_size]
        for i in range(0, len(token_integers), chunk_size)
    ]

    # Decode token chunks back to strings
    chunks = [tokenizer.decode(chunk) for chunk in chunks]

    responses = []
    messages = [
        {"role": "user", "content": prompt},
        {
            "role": "user",
            "content": "To provide the context for the above prompt, I will send you text in parts. When I am finished, I will tell you 'ALL PARTS SENT'. Do not answer until you have received all the parts.",
        },
    ]

    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})

        # Check if total tokens exceed the model's limit and remove oldest chunks if necessary
        while (
            sum(len(tokenizer.encode(msg["content"])) for msg in messages)
            > model_token_limit
        ):
            messages.pop(1)  # Remove the oldest chunk

        response = openai.ChatCompletion.create(model=chat_model, messages=messages)
        chatgpt_response = response.choices[0].message["content"].strip()
        responses.append(chatgpt_response)

    # Add the final "ALL PARTS SENT" message
    messages.append({"role": "user", "content": "ALL PARTS SENT"})
    response = openai.ChatCompletion.create(model=chat_model, messages=messages)
    final_response = response.choices[0].message["content"].strip()
    responses.append(final_response)

    return responses

#############################################################################################################

# First, import the necessary modules and the function
import os

# from chatgptmax import send

# Define a function to read the content of a file
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Use the function
if __name__ == "__main__":
    # Specify the path to your file
    file_path = "D:/PSI/Source/demoA/queue_example.py"
    
    # Read the content of the file
    file_content = read_file_content(file_path)
    
    # Define your prompt
    prompt_text = "Please create unit test using UnitTest for the python code below:"
    
    # Send the file content to ChatGPT
    responses = send(prompt=prompt_text, text_data=file_content)
    
    # Print the responses
    for response in responses:
        print(response)