import csv
import os
from dotenv import load_dotenv


def create_new_csv_with_groups(file_name, start_date, end_date):
    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, 'data')
    file_path = os.path.join(data_directory, file_name)

    new_file_path = os.path.join(current_directory, 'students_with_groups.csv')

    row_count = 0
    with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        row_count = sum(1 for row in reader)

    with open(file_path, mode='r', newline='', encoding='utf-8') as infile, \
            open(new_file_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        for row_number, row in enumerate(reader, start=1):
            if row:
                number = row[0]
                print(f"Numer {number} jest przetwarzany... [{row_number}/{row_count}]")

                groups = get_number_group_set(number, start_date, end_date)

                for group in groups:
                    row.append(group)
                writer.writerow(row)


def get_number_group_set(number, start_date, end_date):
    import requests

    load_dotenv()

    url = os.getenv('API_URL')

    params = {
        "number": number,
        "start": start_date + "T00%3A00%3A00%2B02%3A00",
        "end": end_date + "T00%3A00%3A00%2B02%3A00"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        unique_groups = set()

        for item in data:
            if isinstance(item, dict) and "group_name" in item:
                unique_groups.add(item["group_name"])

        return sorted(unique_groups)

    else:
        print(f"Błąd w pobieraniu danych. Response status: {response.status_code}")


def print_students_in_group(group):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, 'students_with_groups.csv')

    with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')

	    print(f"Grupa: {group}")

        for row in reader:
            if any(group in (col or '') for col in row[3:]):
                print(f"{row[:3]}")

if __name__ == '__main__':

    # 1. CREATE FILE
    # Create the csv file with groups.

    student_data_csv_filename = 'student_data.csv'
    start_date = "2024-10-07"
    end_date = "2024-10-21"

    create_new_csv_with_groups(student_data_csv_filename, start_date, end_date)

    print("Pomyślnie utworzono nowy plik z grupami.")

    # 2. USE THE CREATED FILE
    # Search for students from a specified group in the file created
    # in a function above.

    # group = 'group_to_search'
    # print_students_in_group(group)