import requests
import threading, time

def get_request1(url1, url2):

    print("Thread 1: began")

    for i in range(1000):    
        response = requests.get(url1)
        print(f"Response from {url1}: {response.status_code}, {response.text}")
        response = requests.get(url2)
        print(f"Response from {url2}: {response.status_code}, {response.text}")
    return

def get_request2(url1, url2):

    print("Thread 2: began")
    for i in range(500):    
        response = requests.get(url1)
        print(f"Response from {url1}: {response.status_code}, {response.text}")
        response = requests.get(url2)
        print(f"Response from {url2}: {response.status_code}, {response.text}")

    time.sleep(60)

    for i in range(1000):    
        response = requests.get(url1)
        print(f"Response from {url1}: {response.status_code}, {response.text}")
        response = requests.get(url2)
        print(f"Response from {url2}: {response.status_code}, {response.text}")
    return

# Create and start threads for each URL
def requests_main(DNS):
    threads = []
    urls = [f'https://{DNS}/1', f'https://{DNS}/2']
    thread1 = threading.Thread(target=get_request1, args=(urls[0],urls[1]))
    thread1.start()
    threads.append(thread1)

    thread2 = threading.Thread(target=get_request2, args=(urls[0],urls[1]))
    thread2.start()
    threads.append(thread2)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    return