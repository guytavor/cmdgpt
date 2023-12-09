import os
import sys
import threading

from halo import Halo

from openai import OpenAI


def query_gpt4(query: str) -> str:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content


def query_in_background(query: str, response_list: list):
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
