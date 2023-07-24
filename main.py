from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import math
import pickle
import time

# options
chrome_options = webdriver.ChromeOptions()
# Юзер-Агент
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# Запуск в фоновом режиме. Пока не включаем.
# chrome_options.add_argument('--headless')

# Передаем параметры в driver
driver = webdriver.Chrome(options=chrome_options)

# Функция, выполняющая основную работу.
def up_ad(url):
    # Открываем на весь экран
    driver.maximize_window()
    # Переходим по ссылке
    driver.get(url)
    auth = driver.find_element(By.ID, 'js-modal2').click()
    # Ждем, пока форма станет видимой
    login_form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'js-login-form'))
    )

    # Вводим логин и пароль
    email_input = login_form.find_element(By.NAME, 'email')
    email_input.send_keys('aborodin11')

    password_input = login_form.find_element(By.NAME, 'password')
    password_input.send_keys('sYqba3-wijsuw-cuqcem')
    print("Для продолжения нажмите Shift+H")
    keyboard.wait('shift+h')
    print("Вы нажали Shift+H! Продолжаем выполнение кода.")

    # # Время на прохождение капчи и двухфакторки.
    # time.sleep(5)
    # # Сохраняем куки для дальнейшей работы.
    # pickle.dump(driver.get_cookies(), open("aborodin11_cookies", "wb"))
    # time.sleep(30)
    #
    # # Загружаем куки от аккаунта для дальнейшей работы/
    # for cookie in pickle.load(open("aborodin11_cookies", "rb")):
    #     driver.add_cookie(cookie)
    time.sleep(5)
    while True:
        print('Начал новый цикл.')
        # Переходим в профиль аккаунта.
        driver.get(f'{url}/profile/aborodin11')

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
            try:
                # Найдем кнопку "UP" внутри текущего li элемента
                up_button = li_element.find_element(By.CSS_SELECTOR, 'a.up-group-profile')

                # Нажмем на кнопку "UP"
                up_button.click()

                # Подождем 10 секунд перед следующим нажатием
                time.sleep(1)
            except NoSuchElementException:
                print("Кнопка 'UP' не найдена в текущем элементе")
                try:
                    name = driver.find_element(By.TAG_NAME, 'b').text
                except Exception as ex:
                    name = ex
                with open('log.txt', 'a', encoding='utf-8') as file:
                    file.writelines(f"Кнопка не была найдена : {url} : {name}")
        print('Закончил')




def main():
    up_ad('https://accs-market.com')

# Точка входа.
if __name__ == '__main__':
    main()

