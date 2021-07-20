import os
import sys
from subprocess import call

from colorama import Fore, Style
from dotenv import load_dotenv
from fetchAnimeData import FetchAnimeData

load_dotenv('config.env')
print(Fore.RED + Style.BRIGHT)
if os.getenv('LOGIN_TOKEN') is None or os.getenv('LOGIN_TOKEN') == '':
    print('LOGIN_TOKEN var not found! Please login on the web to generate one')
    call(["python", "generateLoginToken.py"])
    print(Fore.RED + 'Run the script again to continue. Exiting..')
    sys.exit()
    # raise NullEnvironmentError("Exiting")
try:
    token = os.getenv('LOGIN_TOKEN').split(': ')
    left = token[0]
    right = token[1]
except:
    print("Invalid Syntax for the LOGIN_TOKEN ENV. Please login to generate a new one")
    call(["python", "generateLoginToken.py"])
    print(Fore.RED + 'Run the script again to continue. Exiting..')
    sys.exit()
    # raise SyntaxError("Invalid Syntax for the LOGIN_TOKEN ENV. Please read the docs and try again")

print(Style.RESET_ALL)


def fetchAndStoreAnimeData(URL):
    animeTitle, animeList = FetchAnimeData(URL, left, right)
    if animeList:
        with open(f'{animeTitle}.txt', 'w') as f:
            for episode in animeList:
                f.write("%s\n" % episode)
        print(f'File {animeTitle}.txt saved successfully!')
    else:
        print('Nothing Found on ' + URL)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass at least one URL as argument with the file.\nUsage: python main.py URL1 URL2 URL3")
    else:
        for i, arg in enumerate(sys.argv):
            if i > 0:
                fetchAndStoreAnimeData(arg)
