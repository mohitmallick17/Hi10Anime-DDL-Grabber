import os
import sys
from subprocess import call

from colorama import Fore, Style
from dotenv import load_dotenv
from hi10dl.helpers.fetchAnimeData import FetchAnimeData

from hi10dl.helpers.exceptions import InvalidSessionException

load_dotenv('hi10dl/config.env')
print(Fore.RED + Style.BRIGHT)
if os.getenv('LOGIN_TOKEN') is None or os.getenv('LOGIN_TOKEN') == '':
    print('LOGIN_TOKEN var not found! Please login on the web to generate one')
    call(["python", "hi10dl/helpers/generateLoginToken.py"])
    print(Fore.RED + 'Run the script again to continue. Exiting..')
    sys.exit()

try:
    token = os.getenv('LOGIN_TOKEN').split(': ')
    left = token[0]
    right = token[1]
except:
    print("Invalid Syntax for the LOGIN_TOKEN ENV. Please login to generate a new one")
    call(["python", "generateLoginToken.py"])
    print(Fore.RED + 'Run the script again to continue. Exiting..')
    print(Style.RESET_ALL)
    sys.exit()

print(Style.RESET_ALL)


def fetchAndStoreAnimeData(URL):
    try:
        animeTitle, animeList = FetchAnimeData(URL, left, right)
        if animeList:
            with open(os.path.dirname(__file__) + f'/../out/{animeTitle}.txt', 'w', encoding='utf-8') as f:
                for episode in animeList:
                    f.write("%s\n" % episode)
            print(f'File {animeTitle}.txt saved successfully!')
        else:
            print('Nothing Found on ' + URL)
    except InvalidSessionException:
        print(Fore.RED + Style.BRIGHT)
        print("Token Expired. Please login to generate a new one")
        call(["python", "hi10dl/helpers/generateLoginToken.py"])
        print(Fore.RED + 'Run the script again to continue. Exiting..')
        print(Style.RESET_ALL)
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass at least one URL as argument with the file.\nUsage: python -m hi10dl URL1 URL2 URL3 ...")
    else:
        outdir = os.path.dirname(__file__) + '/../out'
        isExist = os.path.exists(outdir)
        if not isExist:
            os.makedirs(outdir)
        for i, arg in enumerate(sys.argv):
            if i > 0:
                fetchAndStoreAnimeData(arg)
