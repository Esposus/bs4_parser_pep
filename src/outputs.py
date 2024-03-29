import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, FILE, PRETTY, RESULTS_DIR


FILE_SAVED_MESSAGE = 'Файл с результатами был сохранён: {file_path}'


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
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(f, dialect=csv.unix_dialect).writerows(results)
    logging.info(FILE_SAVED_MESSAGE.format(file_path=file_path))


OUTPUT_FUNCTIONS = {
    FILE: file_output,
    PRETTY: pretty_output,
    None: default_output,
}


def control_output(results, cli_args, outputs=OUTPUT_FUNCTIONS):
    OUTPUT_FUNCTIONS.get(cli_args.output)(results, cli_args)
