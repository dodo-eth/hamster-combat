
from flask import Flask, request, render_template, redirect, url_for
import threading
import time
import csv
import requests 
import datetime 

app = Flask(__name__)


def send_request(url, request_type, token, proxy, data):
    
    headers = {
        'Accept-Language': 'en,en-US;q=0.9,ru-RU;q=0.8,ru;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    proxies = {
        'http': proxy,
        'https': proxy
    }
    
    try:
        if request_type.upper() == 'POST':
            response = requests.post(url, headers=headers, proxies=proxies, json=data)
        elif request_type.upper() == 'GET':
            response = requests.get(url, headers=headers, proxies=proxies, params=data)
        else:
            raise ValueError("Unsupported request type")
        
        response.raise_for_status()
        print(response.status_code)
        return response.status_code, response.json()
       
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}" )
        print(response.json())
        return response.status_code, response.json()
    
def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 3:  # Проверяем, что строка содержит 3 поля
                entry = {
                    'discription': row[0],
                    'proxy': row[1],
                    'token': row[2]
                }
                data.append(entry)
    return data

def check_proxy(proxy):
    test_url = 'http://httpbin.org/ip'
    
    try:
        response = requests.get(test_url, proxies={'http': proxy, 'https': proxy})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Proxy check failed: {e}")
        return None



def daily_reward_function(file_path):
    while True:
        data = read_csv(file_path)
        for entry in data:
            data = {"taskId":"streak_days"}
            send_request("https://api.hamsterkombat.io/clicker/check-task", "POST", entry['token'], entry['proxy'], data)
            print(entry['discription'] + " streak_days function отработал")
        time.sleep(24 * 60 * 60)  # Спим 24 часа 
        
def sync_function(file_path):
    while True:
        data = read_csv(file_path)
        for entry in data:
            send_request("https://api.hamsterkombat.io/clicker/sync", "POST", entry['token'], entry['proxy'], "")
            print(entry['discription'] + " Sync function отработал")
        time.sleep(2 * 60 * 60)  # Спим 2 часа (2 * 60 минут * 60 секунд)


def claim_dayly_cipher(combo):
    data = read_csv('file.csv')
    for entry in data:
        current_timestamp = int(datetime.datetime.now().timestamp() * 1000) 
        for card in combo: 
            if isinstance(card, list):
                card = card[0]
            data = {"cipher": card}
            response_data = send_request("https://api.hamsterkombat.io/clicker/claim-daily-cipher","POST", entry['token'], entry['proxy'],data)
            print(f"Response Data: {response_data}")

def claim_dayly_function(combo):
    data = read_csv('file.csv')
    for entry in data:
        current_timestamp = int(datetime.datetime.now().timestamp() * 1000) 
        for card in combo: 
            if isinstance(card, list):
                card = card[0]
            payload = {"upgradeId": card, "timestamp": current_timestamp} 
            send_request("https://api.hamsterkombat.io/clicker/buy-upgrade","POST", entry['token'], entry['proxy'],payload)
            
        status,response = send_request("https://api.hamsterkombat.io/clicker/claim-daily-combo","POST", entry['token'], entry['proxy'],"")

        print(entry['discription'] + " claim_dayly отработал")
    
    
    
    
     


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        if input_text:
            lines = input_text.splitlines()
            data_list = [line.strip().split(',') for line in lines if line.strip()]
            r= len(data_list)
            if len(data_list) == 3:
                start_dayly_combo_thread(data_list)
                return "Дейли комбо started"
            
            if len(data_list) == 1:
                start_dayly_cipher_thread(data_list)
                return "шифр  started"
            
            else:
                return "Input should have exactly 3 groups of data"
    return render_template('index.html')



def start_dayli_rewards_thread(file_path):
    dayli_rewards_thread = threading.Thread(target=daily_reward_function, args=(file_path,))
    dayli_rewards_thread.daemon = True
    dayli_rewards_thread.start()

def start_dayly_cipher_thread(combo):
    dayly_cipher_thread = threading.Thread(target=claim_dayly_cipher, args=(combo,))
    dayly_cipher_thread.daemon = True
    dayly_cipher_thread.start()

def start_dayly_combo_thread(combo):
    dayly_combo_thread = threading.Thread(target=claim_dayly_function, args=(combo,))
    dayly_combo_thread.daemon = True
    dayly_combo_thread.start()

def start_sync_thread(file_path):
    sync_thread = threading.Thread(target=sync_function, args=(file_path,))
    sync_thread.daemon = True
    sync_thread.start()

if __name__ == '__main__':
    file_path = 'file.csv'
    
    # Запуск функции синхронизации в отдельном потоке
    
    start_dayli_rewards_thread(file_path)
    start_sync_thread(file_path)
    # Flask-приложение будет запущено в основном потоке
    app.run(debug=True, host='0.0.0.0', port=5000)


 