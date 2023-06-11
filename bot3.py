import requests
import random
import time

def load_proxy_list(file_path):
    with open(file_path, 'r') as file:
        proxy_list = file.read().splitlines()
    return proxy_list

def load_user_agents(file_path):
    with open(file_path, 'r') as file:
        user_agents = file.read().splitlines()
    return user_agents

def load_referers(file_path):
    with open(file_path, 'r') as file:
        referers = file.read().splitlines()
    return referers

def change_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    proxies = {
        'http': proxy,
        'https': proxy
    }
    print(f"Changing proxy to {proxy}")
    return proxies

def select_user_agent(user_agents):
    user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': user_agent
    }
    print(f"Selected user agent: {user_agent}")
    return headers

def select_referer(referers):
    referer = random.choice(referers)
    headers = {
        'Referer': referer
    }
    print(f"Selected referer: {referer}")
    return headers

def make_request(url, proxies, headers):
    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        if response.status_code == 200:
            print("Request successful")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    proxy_file_path = 'proxy.txt'
    user_agents_file_path = 'agent.txt'
    referers_file_path = 'referers.txt'
    url = 'https://yourdomain.com'  # Ganti dengan URL tujuan Anda
    request_limit = 1000

    proxy_list = load_proxy_list(proxy_file_path)
    random.shuffle(proxy_list)
    user_agents = load_user_agents(user_agents_file_path)
    referers = load_referers(referers_file_path)

    request_count = 0
    error_count = 0

    while request_count < request_limit:
        proxies = change_proxy(proxy_list)
        user_agent_headers = select_user_agent(user_agents)
        referer_headers = select_referer(referers)
        headers = {**user_agent_headers, **referer_headers}

        try:
            make_request(url, proxies, headers)
            request_count += 1
        except:
            error_count += 1
            print(f"An error occurred, skipping request ({error_count}/{request_limit})")

        time.sleep(2)

if __name__ == '__main__':
    main()
