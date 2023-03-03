
<h1 align="center">
  <br>
<img src="https://user-images.githubusercontent.com/59805766/222643217-ea37efe1-fd1a-42fe-9081-ce9609cffe70.png" alt="CenQuest"></a>
</h1>
<h4 align="center">A Python script using the Censys API to search for internet-facing hosts based on custom queries</h4>

<p align="center">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
<a href="https://github.com/ReverseTEN/CenQuest/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</p>

<p align="center">



# CenQuest

CenQuest is a Python script that uses the Censys API to search for internet-facing hosts based on custom search queries. It retrieves the IP addresses and port numbers of all matching hosts and stores the results in a file called `Hosts.txt`. 

In addition,CenQuest includes a **resume search feature that enables you to pick up where you left off without having to restart the search**. This feature utilizes a CSV file called Info.csv, which keeps track of previously executed search queries and the number of pages retrieved for each query.

## Requirements

To run the script, you need to have the following:

- Python 3.x
- A Censys account with API credentials

Set up your Censys API credentials by creating a file named `config.ini` in the same directory as the script, with the following format:

```

[Censys Api Config]

api=YOUR_CENSYS_UID
secret=YOUR_CENSYS_SECRET

```


## Usage
To use the script, you need to provide a search query and the number of pages you want to retrieve. Here's an example command:

```bash
git clone https://github.com/ReverseTEN/CenQuest.git
cd CenQuest
python cenquest.py [-h] -q QUERY -p PAGES

```

The following arguments are available:

- -h, --help: show the help message and exit.
- -q QUERY, --query QUERY: search query to be executed.
- -p PAGES, --pages PAGES: number of pages to retrieve.

### Example:

```bash

python3 cenquest.py -q "apache" -p 5

```

This will search for hosts with the word "apache" in their banners and retrieve the first 5 pages of results. The results will be written to the `Hosts.txt` file in the same directory as the script.


## Resume Search

CenQuest uses a CSV file called `Info.csv` to keep track of which search queries have already been executed and how many pages of results were obtained for each query. This allows the script to resume a search from where it left off, in case the script is interrupted or terminated prematurely.


## Disclaimer
This script is for educational purposes only. Use it at your own risk.
