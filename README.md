# Dictionary Attack Script

This is a Python script for performing a dictionary attack on a target URL by attempting different passwords from a wordlist. It supports custom headers and user agents for the HTTP requests.

## Features
- Performs dictionary attacks on a specified URL
- Supports custom headers for the attack
- Utilizes a wordlist file for attempting different passwords
- Uses randomized user agents for each request
- Provides real-time progress updates with a progress bar
- Displays information about each attempted password, including status code and content length
- Estimates the remaining time for the attack to complete
- Allows cancellation of the attack with confirmation

## Screenshots

![Alt Text](https://raw.githubusercontent.com/hxlxmjxbbxs/defuse/main/img/defuse%20%20(2).jpg?token=GHSAT0AAAAAACCY5JV7AA7LBWVLXB2UJAVSZEBH2NQ)

![Alt Text](https://raw.githubusercontent.com/hxlxmjxbbxs/defuse/main/img/defuse%20%20(1).jpg?token=GHSAT0AAAAAACCY5JV7MHREAZT35H7MCQVCZEBH2NA)

## Prerequisites
- Python 3.x
- Required Python packages:
  - requests
  - base64
  - argparse
  - tqdm
  - termcolor
  - tabulate

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/hxlxmjxbbxs/dictionary-attack-script.git
   ```

2. Navigate to the project directory:
   ```
   cd dictionary-attack-script
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the script:
   ```
   python dictionary_attack.py -u <target_url> -H <header> -w <wordlist_file> -a <user_agents_file>
   ```

   - Replace `<target_url>` with the URL of the target server.
   - Replace `<header>` with the header to be attacked.
   - Replace `<wordlist_file>` with the path to the wordlist file containing potential passwords.
   - Replace `<user_agents_file>` with the path to the file containing user agents.

5. Follow the on-screen instructions and observe the progress of the attack.

## License
[MIT License](LICENSE)

## Author
- Name: hxlxmjxbbxs
- GitHub: [https://github.com/hxlxmjxbbxs](https://github.com/hxlxmjxbbxs)

## Release Date
- 2023/06/07

Feel free to contribute to the project or report any issues on GitHub. Thank you for using the dictionary attack script!
