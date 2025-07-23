import requests
import time
from colorama import Fore, Style, init



def get_coin_price(crypto_ids):
    ids = ','.join(crypto_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()  
 
init()

def highlight_letter(word, position):
        result = ""
        for i, letter in enumerate(word):
            if i == position:
                result += Fore.BLUE + letter + Style.RESET_ALL
            else:
                result += letter
            return result
