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


def process_query(query: str, messages: list) -> str:
    response_list = []

    # Start the query in a background thread
    thread = threading.Thread(
        target=lambda: response_list.append(query_gpt4(messages + [{"role": "user", "content": query}])))
    thread.start()

    spinner = Halo(text='Processing', spinner='dots')
    spinner.start()

    # Wait for the thread to finish
    thread.join()

    spinner.stop()

    return response_list[0] if response_list else ''


def interactive_session():
    session_history = []
    try:
        while True:
            query = input("> ")
            if query.lower() in ["exit", "quit"]:
                break

            session_history.append({"role": "user", "content": query})
            response = process_query(query, session_history)
            if response:
                print(colored(response, 'green', attrs=['bold']))
                session_history.append({"role": "assistant", "content": response})

    except (KeyboardInterrupt, EOFError):
        print("\nBye.")


def main():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])  # Join all arguments into a single string
        response = process_query(query, [])
        if response:
            print(response)
    else:
        interactive_session()


if __name__ == "__main__":
    main()
