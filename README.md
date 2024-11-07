
# Verba Group Task: Quotes Parser

Этот проект предназначен для сбора цитат с ресурса https://quotes.toscrape.com

### Описание
Проект написан на Python 3.8
Использует библиотеки BeautifulSoup4 и requests, для парсинга и HTTP запросов.

### Основные возможности
- Многопоточный парсинг циатат
- Сбор информации об авторах (дата рождения, место рождения, описание)
- Сохранение данных в JSON-файл
- Логирование процесса выполнения

### Установка и настройка
#### Клонирование 
`git clone https://github.com/SHADR1N/verba-group-task.git`
`cd verba-group-task`
#### Установка зависимостей
`pip freeze -r req.txt`

### Использование
Выполните скрипт с определением глубины (количества страниц, которые нужно собрать).

#### Пример запуска
```python
from scrap import Scrap

# Задаем глубину парсинга - например, 10 страниц
scraper = Scrap(depth=10)
scraper.run()
scraper.save("results.json")
```
После выполнения в папке с проектом появится файл results.json, содержащий собранные данные о цитатах и авторах.

#### Структура данных
JSON-файл `results.json` сохраняет данные в следующем формате:

```json
[
    {
        "text": "Текст цитаты",
        "tags": [
            {"href": "ссылка_на_тег", "name": "имя_тега"}
        ],
        "author": {
            "author_name": "Имя автора",
            "author_href": "Ссылка на профиль автора",
            "author_date": "Дата рождения",
            "author_location": "Место рождения",
            "author_description": "Описание автора"
        }
    },
    ...
]
```
#### Логирование

Проект использует логгер для записи важной информации и ошибок. Настройки логирования можно изменить в файле `logger.py`

### Примечания
- Сайт `quotes.toscrape.com` является тестовым ресурсом для парсинга, предоставленный `Verba Group`. Этот проект предназначен только для демонстрационных целей.