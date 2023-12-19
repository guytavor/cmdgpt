import os
import queue
import sys
import threading
import time
import webbrowser
from os import _exit

from halo import Halo
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

no_detail = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:"


def call_dall_e(prompt: str) -> str:
    client = OpenAI()
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd", #hd, normal
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"\nOpenAI error: {e}")
        _exit(1)


def internal_generate_image(prompt: str, result_queue: queue.Queue):
    url = call_dall_e(prompt)
    result_queue.put(url)


def generate_image(prompt: str):
    start_time = time.time()

    result_queue = queue.Queue()
    thread = threading.Thread(target=internal_generate_image, args=(prompt, result_queue))
    thread.start()

    spinner = Halo(text='Creating image', spinner='dots')
    spinner.start()
    thread.join()
    spinner.stop()

    end_time = time.time()

    image_url = result_queue.get()  # Retrieve the image URL from the queue

    print(f"Image generated in {end_time - start_time:.2f} seconds")
    print(f"Image URL: {image_url}")

    # Open the image URL in the default web browser
    webbrowser.open(image_url)


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
    console = Console()

    try:
        while True:
            query = input("> ")
            if len(query.strip()) == 0:
                continue
            if query.lower() in ["exit", "quit"]:
                break

            session_history.append({"role": "user", "content": query})
            response = process_query(query, session_history)
            if response:
                markdown = Markdown(response)
                console.print(markdown)
                session_history.append({"role": "assistant", "content": response})

    except (KeyboardInterrupt, EOFError):
        print("\nBye.")


def main():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])  # Join all arguments into a single string

        first_word = query.split()[0].lower()
        if first_word in ["pic", "pix"]:
            prompt = ' '.join(query.split()[1:])
            if first_word == "pix":
                prompt = no_detail + ' ' + prompt
            generate_image(prompt)
            exit()

        response = process_query(query, [])
        if response:
            console = Console()
            markdown = Markdown(response)
            console.print(markdown)
    else:
        interactive_session()


if __name__ == "__main__":
    main()
