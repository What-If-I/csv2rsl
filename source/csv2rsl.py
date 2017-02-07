import csv
import sys
import argparse

from os import path


def prompt_enter_and_exit():
    input("Работа завершилась неудачно. Нажмите Enter для выхода.")
    exit(1)


def concatenate_values(header, values, separator='=', delimiter="|"):
    concat = ["{key}{sep}{value}".format(key=key, value=value, sep=separator) for key, value in zip(header, values)]
    return delimiter.join(concat)


def valid_csv(path2csv):
    if not path.exists(path2csv):
        print("Файл {f_name} не найден.".format(f_name=path2csv))
        return False

    try:
        path2csv.split(".")[1]
    except IndexError:
        print("{f_name} не является файлом.".format(f_name=path2csv))
        return False

    if path2csv.split(".")[1] != "csv":
        print("Файл {f_name} не является csv.".format(f_name=path2csv))
        return False

    return True


def get_path_from_console_args():
    argv = sys.argv
    if len(argv) > 2:
        print("Указано слишком много аргументов. Требуется ввести только путь к файлу.")

    elif len(argv) <= 1:
        print("Путь к файлу не указан")

    else:
        return argv[1]


def parse_args():
    parser = argparse.ArgumentParser(description="Утилита конвертирует csv файл в rsl.")
    parser.add_argument(dest="input_file", help="Путь к файлу csv.")
    parser.add_argument('-d', dest="delimiter", help="Разделитель.")
    parser.add_argument('-o', dest="output_file", help="Файл на выходе.")
    p = parser.parse_args()
    return p.input_file, p.delimiter, p.output_file


def main(path2csv, csv_delimiter=None, path2rsl=None):
    with open(path2csv, mode='r', encoding='utf-8') as csv_file:
        csv_delimiters = [csv_delimiter] if csv_delimiter else [',', ';', '\t', ' ', ':']

        try:
            dialect = csv.Sniffer().sniff(csv_file.read(2048), delimiters=csv_delimiters)

        except UnicodeDecodeError as err:
            print("[WARNING] Убедись что файл в кодировке UTF-8(без BOM)")
            print("Error:", err)
            prompt_enter_and_exit()

        except csv.Error as err:
            if csv_delimiter:
                print("[WARNING] Не удалось прочесть файл с указанным разделителем.")
            else:
                print("[WARNING] Не удалось подобрать разделитель.")
            print("Пожалуйста укажите верный разделитель с параметром -d")
            print("Error:", err)
            prompt_enter_and_exit()

        else:
            csv_file.seek(0)
            has_header = csv.Sniffer().has_header(csv_file.read(2048))
            csv_file.seek(0)

            if not has_header:
                input("[WARNING] Заголовок в файле не найден.")
                prompt_enter_and_exit()

            csv_reader = csv.reader(csv_file, dialect=dialect)
            headers = next(csv_reader)
            rows = (row for row in csv_reader)

            concatenated_values = [(concatenate_values(headers, row) + "\n")
                                   for row in rows]

            path2rsl = path2rsl if path2rsl else path2csv.split(".")[0] + ".rsl"
            with open(path2rsl, mode='w', encoding='utf-8') as rslfile:
                rslfile.writelines(concatenated_values)

            print("Файл успешно сохранён:", path2rsl)


if __name__ == '__main__':
    input_path, delimiter, output_path = parse_args()
    if valid_csv(input_path):
        main(input_path, delimiter, output_path)
    else:
        prompt_enter_and_exit()
