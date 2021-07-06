from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import insta_username, insta_password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os


# создаем класс
class InstaBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.wdriver = webdriver.Chrome("C:\\Users\\user\\PycharmProjects\\instaBot\\chromedriver\\chromedriver.exe")

    # создаем метод для закрытия браузера
    def browser_close(self):
        self.wdriver.close()
        self.wdriver.quit()

    # создаем метод для логина
    def login(self):
        wdriver = self.wdriver
        wdriver.get('https://instagram.com')
        time.sleep(random.randrange(3,5))
        
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

    # создаем метод для лайка
    def like_by_hashtag(self, hashtag):
        wdriver = self.wdriver
        wdriver.get(f'https://instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 6))

        hrefs = wdriver.find_element_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                wdriver.get(url)
                time.sleep(4)
                like_btn_press = wdriver.find_element_by_xpath('/html/body/div(1)/selection/main/div/div(1)/article/div(3)/selection(1)/span(1)/button').click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.browser_close()

    # проверяем, есть ли элемент на странице(по xpath)
    def element_existence_by_xpath(self, url):

        wdriver = self.wdriver
        # метод пытается найти на странице переданный элемент
        try:
            wdriver.find_element_by_xpath(url)
            # в случае успеха задаем флаг True
            exist = True
        # а если его нет, то будет вызвано исключение и будет присвоен флаг False
        except NoSuchElementException:
            exist = False
        return exist

    # ставим лайк по прямой ссылке на пост
    # он принимает в себя прямую ссылку на пост, получив которую он будет заходить на страницу и ставить лайки
    def put_actual_like(self, ready_post):

        # отправляем браузер по ссылке
        wdriver = self.wdriver
        # условие для проверки, неверная ссылка и если поста нет
        wdriver.get(ready_post)
        time.sleep(3)

        # скопируем из браузера xpath сообщения с несуществующим постом
        # создадим переменную с этим значением и в if вызовем созданный метод для проверки элементов на странице
        # передадим в него переменную
        non_existent_post = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(non_existent_post):
            print("Данный пост не существует!")
            self.browser_close()
        # иначе, переходим на страницу с постом и ставим лайк
        else:
            print("Пост найден, ставим Like!")
            time.sleep(2)

            # ставим лайк вызвав метод клик
            like_btn = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            wdriver.find_element_by_xpath(like_btn).click()
            time.sleep(3)

            print(f"We have another Like ))) on {ready_post}")
            self.browser_close()

    # собираем ссылки на все пользовательские посты
    def get_all_posts_url(self, userpage):

        wdriver = self.wdriver
        wdriver.get(userpage)
        time.sleep(5)

        # услови для проверки на валидацию, такое же как и выше
        non_existent_post = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(non_existent_post):
            print("Данный пользователь не существует!")
            self.browser_close()
        # иначе, переходим на страницу с постом и ставим лайк
        else:
            print("Пользователь найден, ставим Like!")
            time.sleep(2)

            # прокручиваем страницу вниз чтобы собрать все посты
            # копируем xpath до блока с постами и вызываем свойство text чтобы получить содержимое
            # и обернем полученный результат в функцию int, чтобы получить целое число
            posts_counter = int(wdriver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            # создадим переменную для вычисления количества постов
            loop_counter = int(posts_counter / 12)
            print(loop_counter)

            # складываем все получаемые ниже ссылки
            posts_storage = []

            # вызываем цикл который будет совершать нужное количество прокруток страницы и собирать ссылки в список
            for i in range(0, loop_counter):
                links = wdriver.find_element_by_tag_name('a')
                links = [item.get_attribute('href') for item in links if "/p" in item.get_attribute('href')]

                # пробегаемся по получаемым ссылкам и добавляем их в наш список
                for href in links:
                    posts_storage.append(href)

                # скролим страницу
                wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
                print(f"Iteration #{i}")

            # сохраним полученные ссылки в файл, по имени аккаунта с которым мы работаем
            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_storage:
                    file.write(post_url + "\n")

            # проверяем ссылки на уникальность, применяя к функции функцию set, которая транслирует его во множество
            # множество - это контейнер, который содержит в себе только уникальные и неупорядоченные элементы
            set_posts_urls = set(posts_storage)
            # трансформируем множество обратно в список
            set_posts_urls = list(set_posts_urls)

            # сохраним неповторяющийся список в новый файл
            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # ставим лайки по ссылке на аккаунт пользователя
    # бот заходит на страницу пользователя, собирает все его посты и ставит на них лайки
    def put_may_likes(self, userpage):

        # метод принимает ссылку на страницу
        wdriver = self.wdriver
        self.get_all_posts_url(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(3)
        wdriver.get(userpage)
        time.sleep(5)

        # ставим лайк под каждым постом
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            # создаем цикл for, который отправляет бота по ссылке, находит кнопку лайка и кликает
            # для прохода бота по первым 9 постам, пишем:
            # for post_url in urls_list[0:9]:
            for post_url in urls_list:
                try:
                    wdriver.get(post_url)
                    time.sleep(3)

                    like_btn = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    wdriver.find_element_by_xpath(like_btn).click()
                    # обманываем ограничение инсты на количество лайков
                    time.sleep(random.randrange(80, 100))
                    time.sleep(3)

                    self.browser_close()
                    print(f"We have another Like ))) on {post_url} and that's great")
                except Exception as ex:
                    print(ex)
                    self.browser_close()

        self.browser_close()

            # # ставим лайк вызвав метод клик
            # like_btn = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            # wdriver.find_element_by_xpath(like_btn).click()
            # time.sleep(3)
            #
            # print(f"We have another Like ))) on {ready_post}")
            # self.browser_close()

    # метод для скачивания контента со страницы пользователя
    def download_user_page_content(self, userpage):
        # метод принимает ссылку на страницу
        wdriver = self.wdriver
        self.get_all_posts_url(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(3)
        wdriver.get(userpage)
        time.sleep(5)

        # создаем папку с именем пользователя для хранения в ней скаченного контента
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует")
        else:
            os.mkdir(file_name)

        # сохраняем полученные ссылки в список
        vid_and_img_source_list = []

        # ставим лайк под каждым постом
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            # создаем цикл for, который отправляет бота по ссылке, находит кнопку лайка и кликает
            # для прохода бота по первым 9 постам, пишем:
            # for post_url in urls_list[0:9]:
            for post_url in urls_list:
                try:
                    wdriver.get(post_url)
                    time.sleep(3)

                    insta_user_img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    insta_user_video_src = "/html/body/div[1]/section/main/div/div[1]/article/" \
                                           "div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    # если картинка находится на странице, то бот забирает ссылку лежащую в атрибуте src
                    if self.xpath_exists(insta_user_img_src):
                        img_url = wdriver.find_element_by_xpath(insta_user_img_src).get_attribute("src")
                        vid_and_img_source_list.append(img_url)

                        # сохраняем изображение
                        get_img = requests.get(insta_user_img_src)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(insta_user_video_src):
                        video_url = wdriver.find_element_by_xpath(insta_user_video_src).get_attribute("src")
                        vid_and_img_source_list.append(video_url)

                        # сохраняем видео
                        get_video = requests.get(insta_user_video_src, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        print("Error!!! Check the code!!!")
                        vid_and_img_source_list.append(f"{post_url}, нет ссылки!")
                    print(f"Загрузка из {post_url} завершена!")
                except Exception as ex:
                    print(ex)
                    self.browser_close()

            self.browser_close()
        with open(f'{file_name}/{file_name}_vid_and_img_source_list.txt', 'a') as file:
            for i in vid_and_img_source_list:
                file.write(i + "\n")

    # подписка на всех подписчиков переданного аккаунта
    def get_all_subscribers(self, userpage):
        wdriver = self.wdriver
        wdriver.get(userpage)
        time.sleep(5)
        file_name = userpage.split("/")[-2]

        # создаем папку с именем пользователя для хранения в ней скаченного контента
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует")
        else:
            print(f"Создаем папку пользователя {file_name}")
            os.mkdir(file_name)

        # услови для проверки на валидацию, такое же как и выше
        non_existent_post = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(non_existent_post):
            print(f"Данный пользователь {file_name} не существует!")
            self.browser_close()
        # иначе, переходим на страницу с постом и ставим лайк
        else:
            print(f"Пользователь {file_name} найден, скачиваем ссылки на подписчиков!")
            time.sleep(2)

            # находим кнопку с подписчиками и парсим их количество
            subscribers_parse = wdriver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            subscribers_count = subscribers_parse.text
            subscribers_count = int(subscribers_count.split(' ')[0])
            print(f"Количество подписчиков: {subscribers_count}")
            time.sleep(3)

            # скроллим список подписчиков
            # количество итераций скрола равно результату деления числа подписчиков на 12
            loops_count = int(subscribers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(5)

            # нажимаем на кнопку с подписчиками
            subscribers_parse.click()
            time.sleep(4)

            subscribers_ul = wdriver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

            try:
                # создаем список для ссылок
                subscribers_urls = []
                # запускаем цикл скролла
                for i in range(1, loops_count + 1):
                    wdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", subscribers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_subscr_urls_div = subscribers_ul.find_element_by_tag_name("li")

                # проходимся по списку циклом извлекая из каждого тега a аттрибут href и сохраняя его в список(append)
                for url in all_subscr_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    subscribers_urls.append(url)

                # сохраним полученых подписчиков в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in subscribers_urls:
                        text_file.write(link + "\n")

                # открываем файл с подписчиками
                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_list = text_file.readlines()

                    for user in users_list[0:10]:
                        try:
                            # проверяем файл с подписчиками на наличие ссылки и если есть совпадение, то переходим
                            # к следующей итерации
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками не существует!')
                                #print(ex)

                            wdriver = self.wdriver
                            wdriver.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):
                                print("Мы уже подписаны на этот профиль!")
                            elif self.xpath_exists(
                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(f'Мы уже подписаны на {page_owner}')
                            else:
                                time.sleep(random.randrange(4, 10))

                                if self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_btn = wdriver.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'Запросить подписку у пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                else:
                                    try:
                                        if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_btn = wdriver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_btn = wdriver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, то он создается
                                with open(f'{file_name}/{file_name}_subscriber_list.txt', 'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                # пауза между подпиской
                                time.sleep(random.randrange(120, 180))

                        except Exception as ex:
                            print(ex)
                            self.browser_close()

            except Exception as ex:
                print(ex)
                self.browser_close()

        self.browser_close()


mr_bot = InstaBot(insta_username, insta_password)
mr_bot.login()
mr_bot.put_actual_like("https://instagram.com/")
mr_bot.download_user_page_content("https://www.instagram.com/username/")









