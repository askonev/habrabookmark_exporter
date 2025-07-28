import os
from halo import Halo
from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv

spinner = Halo(text='Waiting for the capcha solution: ', spinner='dots')

load_dotenv()

secret_login = os.getenv("SECRET_LOGIN")
secret_pass = os.getenv("SECRET_PASS")

login = "#app > div > div.tm-layout > div\
.tm-base-layout__header_is-sticky.tm-base-layout__header > div > \
    div > div.tm-header-user-menu.tm-base-layout__user-menu > \
        a:nth-child(4) > button"
form_email = "#ident-form > div:nth-child(1) > input"
form_password = "#ident-form > div:nth-child(2) > input"
# Селекторы для Yandex SmartCaptcha
captcha_container = "#ident-form > div:nth-child(3) > div > iframe"
captcha_button = "#js-button"
captcha_checkbox = ".CheckboxCaptcha-Checkbox"
captcha_modal = ".Modal_visible"
image_challenge = ".AdvancedCaptcha-View > img"
code_entered = ".AdvancedCaptcha-FormField > span > input"
log_in = "button[type='submit']"


def open(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(url)
        
        # Ждем и нажимаем на кнопку логина
        page.wait_for_selector(login)
        page.click(login)

        # Заполняем форму логина
        page.wait_for_selector(form_email)
        page.fill(form_email, secret_login)

        page.wait_for_selector(form_password)
        page.fill(form_password, secret_pass)

        # Обработка капчи с таймаутом и повторными попытками
        try:
            spinner.start()            

            # Проверяем наличие контейнера капчи
            if page.is_visible(captcha_container, timeout=5000):
                print("Обнаружена капча, пытаемся решить...")
                # Пытаемся найти и нажать на кнопку капчи
                if page.is_visible(captcha_button, timeout=5000):
                    
                    # на этом этапе автомат не может кликнуть по radiobutton
                    # 
                    # page.click(captcha_button)
                    # print("Нажали на кнопку капчи")

                    # Ждем появления модального окна с изображением капчи
                    if page.is_visible(captcha_modal, timeout=5000):
                        print("Открылось модальное окно с капчей")
                        # Здесь можно добавить код для решения капчи
                        # Например, сохранить изображение и использовать сервис распознавания
                        
                        # Даем пользователю время решить капчу вручную
                        print("Ожидание 20 секунд для ручного решения капчи...")
                        page.wait_for_timeout(20000)
                    
            spinner.succeed('Capcha solved')

        except TimeoutError as e:
            
            spinner.stop()

            print(f"Таймаут при обработке капчи: {e}")
            print("Продолжаем выполнение...")

        # Пытаемся найти и нажать кнопку входа
        try:
            page.wait_for_selector(log_in, timeout=5000)
            page.click(log_in)
            print("Нажали кнопку входа")
        except TimeoutError:
            print("Кнопка входа не найдена, возможно уже авторизованы")

        # Ждем загрузки страницы после авторизации
        page.wait_for_timeout(5000)
        
        # Проверяем успешность авторизации
        if "habr.com" in page.url:
            print(f"Успешно открыта страница: {page.url}")
        else:
            print(f"Возможно, авторизация не удалась. Текущий URL: {page.url}")

        # Даем возможность увидеть результат перед закрытием
        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    open("https://habr.com/")
    