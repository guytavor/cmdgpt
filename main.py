import os
import sys
import threading

from halo import Halo

from openai import OpenAI
from termcolor import colored


def query_gpt4(messages: list) -> str:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message.content


def query_in_background(query: str, response_list: list, messages: list):
    response_list.append(query_gpt4(messages + [{"role": "user", "content": query}]))


def interactive_session():
    session_history = []
    try:
        while True:
            query = input("> ")
            if query.lower() == "exit":
                break

            session_history.append({"role": "user", "content": query})
            response = query_gpt4(session_history)
            print(colored(response, 'green', attrs=['bold']))
            session_history.append({"role": "assistant", "content": response})
    except KeyboardInterrupt:
        print("\nSession ended.")


def main():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])  # Join all arguments into a single string
        response_list = []

        # Start the query in a background thread
        thread = threading.Thread(target=query_in_background, args=(query, response_list, []))
        thread.start()

        spinner = Halo(text='Processing', spinner='dots')
        spinner.start()

        # Wait for the background thread to finish
        thread.join()

        spinner.stop()

        if response_list:
            print(response_list[0])  # Print the response
    else:
        interactive_session()


if __name__ == "__main__":
    main()
