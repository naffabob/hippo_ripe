# hippo_ripe

## Что это
hippo_ripe - инструмент учета префиксов BGP-пиров провайдера и генерации access-list-ов. Использует [bgpq3](https://github.com/snar/bgpq3) для обновления данных из агрегаторов. Позволяет наглядно отображать изменения в списках. В hippo_ripe используются Flask и SQLite.

## Установка
Скачайте проект с github
```
git clone https://github.com/naffabob/hippo_ripe.git
```

Создайте виртуальное окружение и установите зависимости
```commandline
pip install -r requirements.txt
```

## Запуск
Создайте DB, cделайте миграцию и примените её
```commandline
export FLASK_APP=webapp && flask db init
export FLASK_APP=webapp && flask db migrate
flask db upgrade
```

Запустите проект
```commandline
export FLASK_APP=webapp && flask run
```

Исполняемый файл для получения префиксов: [get_prefixes.py](get_prefixes.py)
Запустите его по необходимости.

Либо добавьте в crontab автоматический запуск, например каждые сутки
```commandline
* * 1 * * <path_to_venv>/python get_prefixes.py
```