import argparse
import os
import sys
import threading

from halo import Halo
from tqdm import tqdm
import time

from openai import OpenAI

def query_gpt4(query: str) -> str:
    """
    Send a query to GPT-4 Turbo using the chat completions endpoint and return the response.

    :param query: The query string to send to GPT-4 Turbo.
    :return: The response from GPT-4 Turbo.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",  # Updated to use GPT-4 Turbo
        messages=[
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content

def query_in_background(query: str, response_list: list):
    # Assume query_gpt4 is defined elsewhere in your script
    response_list.append(query_gpt4(query))

def main():
    query = ' '.join(sys.argv[1:])  # Join all arguments into a single string
    response_list = []

    # Start the query in a background thread
    thread = threading.Thread(target=query_in_background, args=(query, response_list))
    thread.start()

    spinner = Halo(text='Processing', spinner='dots')
    spinner.start()

    # Wait for the background thread to finish
    thread.join()

    spinner.stop()

    if response_list:
        print(response_list[0])  # Print the response

if __name__ == "__main__":
    main()