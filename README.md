## NovelUpdates search parser

This is a parser for the search results of [NovelUpdates.com](https://www.novelupdates.com/).
It downloads all the search result pages and parse them to get the list of novels.
Also, it can download the novel pages and parse them to get all novel information and links to chapters.

### Usage

Edit Config.py to set the URL of the novel you want to parse. Then run the script. The

Use the following command to install the required packages:

    pip install -r requirements.txt

Edit Config.py to set the URL of the novel you want to parse.
Also, you can set a delay between requests to avoid being blocked by the server and a output paths for the results.

Then run the script. The results will be saved in the output path.

    python main.py

### Additional information

You can edit main.py to change the behavior of the script.
For example, you can set json pretty print to True to make the output more readable or set force update to True to force
the script to download all the pages again.