import csv
import sys
from os import path


def get_keys(row):
    return [key for (key, value) in (kv_pair.split("=") for kv_pair in row.split("|"))]


def get_values(row):
    return [value for (key, value) in (kv_pair.split("=") for kv_pair in row.split("|"))]


def valid_rsl(path2rsl):
    if not path.exists(path2rsl):
        print("Файл {f_name} не найден.".format(f_name=path2rsl))
        return False

    try:
        path2rsl.split(".")[1]
    except IndexError:
        print("{f_name} не является файлом.".format(f_name=path2rsl))
        return False

    if path2rsl.split(".")[1] != "rsl":
        print("Файл {f_name} не является rsl.".format(f_name=path2rsl))
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


def main(path2rsl):

    with open(path2rsl, mode='r', encoding='utf-8') as rslFile:
        rows = [row.replace("\n", "") for row in rslFile.readlines()]

        keys = get_keys(rows[0])
        values_list = [get_values(row) for row in rows]

    path2csv = path2rsl.split(".")[0] + ".csv"
    with open(path2csv, mode='w', newline="") as csvFile:
        csv_writer = csv.writer(csvFile, dialect="excel")
        csv_writer.writerow(keys)
        csv_writer.writerows(values_list)

    print("Файл успешно сохранён:", path2csv)


if __name__ == '__main__':
    path2file = get_path_from_console_args()
    if path2file and valid_rsl(path2file):
        main(path2file)
    else:
        sys.exit(0)
