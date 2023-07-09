## bs4_parser_pep

### О проекте:
Данный проект представляет собой парсер документации `PEP`.
Его назначение:
* Выводить отчет со ссылками на обзор обновлений в новых версиях языка - `whats-new`;
* Выводить отчет о последних актуальных версиях языка со ссылкой на документацию - `latest-versions`;
* Загружать документацию на самую актуальную версию языка в директорию `downloads` - `download`;
* Выводить отчет о всех статусах `PEP` и их количестве.

У пользователя есть возможность выводить отчет в читаемом виде в терминал, используя флаг
`-o pretty`, а также выгружать отчет в виде `.csv`-файла, используя флаг `-o file`.

### Технологии
```
python 3.7
beautifulsoup4
requests-cache
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Esposus/bs4_parser_pep.git
```

```
cd bs4_parser_pep
```

Cоздать и активировать виртуальное окружение:

```
py -3.9 -m venv env
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Для работы с парсером необходимо пройти в директорию `src`:

```
cd src
```

Все доступные режимы использования парсера:

```
python main.py [-h], [--help]
```

### Автор проекта:

- [Дмитрий Морозов](https://github.com/Esposus "GitHub аккаунт")