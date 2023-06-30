import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (FILE, FILE_SAVED_MESSAGE, PRETTY,
                       RESULTS_DIR, DATETIME_FORMAT, BASE_DIR
                    )


def default_output(results, *args):
    """Вывод данных в терминал построчно."""
    for row in results:
        print(*row)


def pretty_output(results, *args):
    """Вывод данных в формате PrettyTable."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Создание директории и запись данных в файл."""
    RESULTS_DIR = BASE_DIR / 'results'
    RESULTS_DIR.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = RESULTS_DIR / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(FILE_SAVED_MESSAGE.format(file_path=file_path))


OUTPUT_FUNCTIONS = {
    FILE: file_output,
    PRETTY: pretty_output,
    None: default_output,
}


def control_output(results, cli_args, outputs=OUTPUT_FUNCTIONS):
    OUTPUT_FUNCTIONS.get(cli_args.output)(results, cli_args)
