from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import math
import time
import concurrent.futures


# Функция, выполняющая основную работу.
def up_ad(url, login, password):
    # options
    chrome_options = webdriver.ChromeOptions()
    # Юзер-Агент
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    # Запуск в фоновом режиме. Пока не включаем.
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Передаем параметры в driver
    driver = webdriver.Chrome(options=chrome_options)
    # Открываем на весь экран
    driver.maximize_window()
    # Переходим по ссылке
    driver.get(url)
    # Процесс авторизации.
    try:
        auth = driver.find_element(By.ID, 'js-modal2').click()
        # Ждем, пока форма станет видимой
        login_form = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'js-login-form'))
        )

        # Вводим логин и пароль
        email_input = login_form.find_element(By.NAME, 'email')
        email_input.send_keys(f'{login}')

        password_input = login_form.find_element(By.NAME, 'password')
        password_input.send_keys(f'{password}')
    except Exception as ex:
        print(ex)
        print('Не найдено кнопка для авторизации, или поля с логином и паролем.')
    print("Для продолжения нажмите Shift+H")
    # Жмем сочетание клавиш Shift+h только после того, как авторизируемся на всех аккаунтах.
    while True:
        if keyboard.is_pressed('shift+h'):
            print("Вы нажали Shift+H! Продолжаем выполнение кода.")
            break
        time.sleep(0.1)

    while True:
        try:
            print('Начал новый цикл.')
            # Переходим в профиль аккаунта.
            driver.get(f'{url}/profile/{login}')
            time.sleep(5)

            # Ищем строку с количеством элементов.
            total = driver.find_element(By.CSS_SELECTOR, 'h2.profile__posts-title')
            # Отделяем число
            listing_text = total.text
            listing_value = int(listing_text.split('(')[1].split(')')[0].strip())

            # Определяем промежуток нажатия на кнопку по формуле: 5 дней (в секундах) делим на количество карточек (с округлением в > + 1 сек).
            wait_click = 432000 / int(listing_value)
            rounded_value = math.ceil(wait_click)

            # Ждем некоторое время, чтобы страница загрузилась
            time.sleep(5)

            # Найдем все li элементы с классом profile__post
            li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.profile__post')

            # Итерируемся по каждому li элементу
            for li_element in li_elements:
                while True:  # Бесконечный цикл для повторной попытки нажатия на кнопку
                    try:
                        # Найдем кнопку "UP" внутри текущего li элемента
                        up_button = li_element.find_element(By.CSS_SELECTOR, 'a.up-group-profile')

                        # Нажмем на кнопку "UP"
                        up_button.click()

                        # Ожидание до следующего клика.
                        time.sleep(rounded_value)

                        # Если удалось нажать кнопку, выходим из бесконечного цикла
                        break

                    except Exception as internet:
                        print("Возможна проблема с интернетом. Ждем 10 секунд и повторяем попытку!")
                        try:
                            name = driver.find_element(By.TAG_NAME, 'b').text
                        except Exception as ex:
                            name = ex
                        with open('log.txt', 'a', encoding='utf-8') as file:
                            file.writelines(f"Кнопка не была найдена: {url} : {name}. Ошибка: {internet}")

                        # Ждем 10 секунд перед повторной попыткой найти и нажать кнопку
                        time.sleep(10)

            print('Закончил')
        except Exceptionas as ex:
            print('Ошибка в цикле.')
            with open('log.txt', 'a', encoding='utf-8') as file:
                file.writelines(f"Ошибка в цикле: {ex}")


# Функция для парсинга данных из файла
def parse_config_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().split('|') for line in lines]



def main():
    # Парсим данные из файла
    config_data = parse_config_file('config.txt')

    # Создаем и запускаем потоки для каждой строки из файла
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(up_ad, data[0], data[1], data[2]) for data in config_data]

        # Ждем завершения всех потоков
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Поток завершился с ошибкой: {e}")

# Точка входа.
if __name__ == '__main__':
    main()

