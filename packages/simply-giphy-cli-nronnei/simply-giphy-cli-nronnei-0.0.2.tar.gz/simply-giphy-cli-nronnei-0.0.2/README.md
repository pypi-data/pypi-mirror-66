# Basic Giphy CLI
Feeling sorry that you're a guest in a Slack workspace and can't use Giphy? Want to spam gifs in Discord but don't... want.. to use the built in tool (shh, I know I'm reaching here)? This is the CLI tool for you!

## What does it do?
Pretty simple. Given whatever you type into your command line, search Giphy. Copies your search terma and a random gif from the top 10 results to your system clipboard for you to use wherever.

## Setup
Requires Python 3.x. so [initialize your virtual environment accoringly.](https://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv)

If Try running `python --version`. If you get something back something with a `3.x`, you're good to go with the commands below. If not, try the same thing with `python3 --version`. If that gives you `3.x`, then use `python3` for your virtual env setup command below.

### On Linux/Mac
```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### On Windows
```sh
python -m venv env
.\env/Scripts/activate
pip install -r requirements.txt
```

## Usage
With your virtual environment activated, run the following command to search:

```py
python get_gif.py <your search here>
# example | python get_gif.py big baller
```

This will automatically copy somthing that looks like the following to your system clipboard:
```
Searched: *big baller*
https://media0.giphy.com/media/8lHnYZ7i9uS62KtX5h/giphy.gif?cid=b5159ec11f9cd7cf31065875e47238f5a62eb2a3176477b6&rid=giphy.gif
```
