import requests

def main():
    url = 'https://itcollege.lviv.ua/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Вміст сторінки:")
            print(response.text)
        else:
            print(f"Не вдалося отримати вміст сторінки. Статус код: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Помилка під час запиту:", e)

if __name__ == "__main__":
    main()
