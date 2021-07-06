from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import insta_username, insta_password
import time
import random


# # create login function with two parameters
# def login(insta_username, insta_password):
#
#     # создаем экземпляр класса хром и в качестве параметров передаем путь до драйвера
#     wdriver = webdriver.Chrome("C:\\Users\\user\\PycharmProjects\\instaBot\\chromedriver\\chromedriver.exe")
#     try:
#         # открываем главную страницу инстаграм
#         wdriver.get('https://instagram.com')
#         # даем время для прогрузки браузера от 3 до 5 сек
#         time.sleep(random.randrange(3, 5))
#
#     # Для поля username
#         # указываем поля из кода страницы для имени пользователя
#         username_input_field = wdriver.find_element_by_name('username')
#         # очищаем поле от возможно введенных ранее данных
#         username_input_field.clear()
#         # передаем в него наше имя пользователя
#         username_input_field.send_keys(insta_username)
#
#         time.sleep(3)
#
#     # Для поля password
#         # указываем поля из кода страницы для пароля
#         password_input_field = wdriver.find_element_by_name('password')
#         # очищаем поле от возможно введенных ранее данных
#         password_input_field.clear()
#         # передаем в него наш пароль
#         password_input_field.send_keys(insta_password)
#
#         # эмулируем нажатие клавиши Enter в поле с паролем
#         password_input_field.send_keys(Keys.ENTER)
#         time.sleep(7)
#
#         # закрываем вкладку в браузере
#         wdriver.close()
#         # выходим из браузера
#         wdriver.quit()
#     except Exception as ex:
#         print(ex)
#         wdriver.close()
#         wdriver.quit()
#
#
# login(insta_username, insta_password)


# создаем функцию поиска по хэштегам
def hash_search(insta_username, insta_password, hashtag):

    # создаем экземпляр класса хром и в качестве параметров передаем путь до драйвера
    wdriver = webdriver.Chrome("C:\\Users\\user\\PycharmProjects\\instaBot\\chromedriver\\chromedriver.exe")
    try:
        # открываем главную страницу инстаграм
        wdriver.get('https://instagram.com')
        # даем время для прогрузки браузера от 3 до 5 сек
        time.sleep(random.randrange(3, 5))

        # Для поля username
        # указываем поля из кода страницы для имени пользователя
        username_input_field = wdriver.find_element_by_name('username')
        # очищаем поле от возможно введенных ранее данных
        username_input_field.clear()
        # передаем в него наше имя пользователя
        username_input_field.send_keys(insta_username)

        time.sleep(3)

        # Для поля password
        # указываем поля из кода страницы для пароля
        password_input_field = wdriver.find_element_by_name('password')
        # очищаем поле от возможно введенных ранее данных
        password_input_field.clear()
        # передаем в него наш пароль
        password_input_field.send_keys(insta_password)

        # эмулируем нажатие клавиши Enter в поле с паролем
        password_input_field.send_keys(Keys.ENTER)
        time.sleep(7)

        # выполняем поиска по хэштегу и ставим пользвателю лайк
        try:
            wdriver.get(f'https://instagram.com/explore/tags/{hashtag}/')
            time.sleep(3)

            # имитируем скрол страницы ботом
            # в range передается количество скроллов
            for i in range(1, 4):
                # вызываем у браузера метод execute_script и направляем в него скрипт из javascript, который скролит
                # скроллит страницу по всей высоте
                wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            # собираем все посты со страницы, что бы потом мы могли по ним переходить
            # вызываем метод поиска по тегу и передаем в него метод 'a'
            hrefs = wdriver.find_element_by_tag_name('a')

            posts_url = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
            print(posts_url)

            # создаем список для будущих ссылок, код аналогичен верхнему
            # post_urls = []
            # # обращаемся к атрибуту href и достаем ссылку из каждого элемента
            # for item in hrefs:
            #     href = item.get_attribute('href')
            #
            #     # если строка "/p/" находится в ссылке, то мы записываем ее в список использую метод update,
            #     # а если ее нет, то пропускаем и переходим к следующей
            #     if "/p/" in href:
            #         posts_urls.append(href)
            #         print(href)

            # открываем сохраненые ссылки и ставим лайка
            for url in posts_url:
                try:
                    wdriver.get(url)
                    time.sleep(3)
                    like_button_press = wdriver.find_element_by_xpath('/html/body/div(1)/selection/main/div/div(1)/article/div(3)/selection(1)/span(1)/button').click()
                    # ставим лайк каждые 90 сек, заставляе бот засыпать в диапазоне от 80 до 100 сек
                    time.sleep(random.randrange(80, 100))
                except Exception as ex:
                    print(ex)

            wdriver.close()
            wdriver.quit()

        except Exception as ex:
            print(ex)
            # закрываем вкладку в браузере
            wdriver.close()
            # выходим из браузера
            wdriver.quit()

            # закрываем вкладку в браузере
            wdriver.close()
            # выходим из браузера
            wdriver.quit()
    except Exception as ex:
        print(ex)
        wdriver.close()
        wdriver.quit()


hash_search(insta_username, insta_password, 'beauty')














