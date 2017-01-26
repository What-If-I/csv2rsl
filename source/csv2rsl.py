import csv
import sys
from os import path


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


def main(path2csv):

    with open(path2csv, mode='r', encoding='utf-8') as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(2048), delimiters=[',', ';', '\t', ' ', ':'])
        except csv.Error:
            print("Не смог распознать разделитель по первым 2048 битам.\n"
                  "Пробую прочесть весь файл...")
            csvfile.seek(0)
            dialect = csv.Sniffer().sniff(csvfile.read(), )
        csvfile.seek(0)
        has_header = csv.Sniffer().has_header(csvfile.read(2048))
        csvfile.seek(0)

        if not has_header:
            input("[WARNING] Файл не содержит заголовка. Для выхода нажмите Enter")
            exit()

        csv_reader = csv.reader(csvfile, dialect=dialect)
        headers = next(csv_reader)
        rows = [row for row in csv_reader]

        concatenated_values = []
        for row in rows:
            concatenated_values.append(concatenate_values(headers, row) + "\n")

    path2rsl = path2csv.split(".")[0] + ".rsl"
    with open(path2rsl, mode='w', encoding='utf-8') as rslfile:
        rslfile.writelines(concatenated_values)

    print("Файл успешно сохранён:", path2rsl)

if __name__ == '__main__':
    path2file = get_path_from_console_args()
    if path2file and valid_csv(path2file):
        main(path2file)
    else:
        sys.exit(0)
