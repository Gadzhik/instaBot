name = "https://instagram.com/some_insta_account/"

# разбиваем ссылку по слешу и забираем нужную часть из списка
file_name = name.split("/")[-2]
print(file_name)