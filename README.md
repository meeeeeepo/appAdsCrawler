# appAdsCrawler

Скрипт позволяет проверять app-ads.txt у списка заданных приложении. 
Для запуска проверки нужно подготовить список приложении на проверку (файл apps.csv) и список нужных значении (app-ads.txt)
Список приложении должен быть в формате: platform,store_id (например android,com.openmygame.games.android.jigsawpuzzle или ios,1527569819)
Файл app-ads.txt должен быть без пробелов и комментариев
Примеры файлов можно найти в репозитории
Запуск скрипта осуществляется без аких либо параметров, просто подготавливаем файлы и выполняем: 
```
python3 checkAppAds.py
```
