import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import psycopg2
from psycopg2.extras import RealDictCursor
from prettytable import PrettyTable
from termcolor import colored
import os
import shutil
import textwrap

# Exécute la commande "clear" pour nettoyer l'affichage du terminal
os.system('clear')

conn = psycopg2.connect(host='localhost', user='postgres', password='postgres', dbname='data')
cur = conn.cursor(cursor_factory=RealDictCursor)



def exportPdfData():
    to_csv = showData("SELECT id,name,age as birthday,city FROM student ORDER BY id", '')

    data = [list(to_csv[0].keys())]  # Extract the header row from the data

    for row in to_csv:
        data.append(list(row.values()))  # Convert each row dictionary to a list of values

    name = input("Enter the name of the file: ")
    file_path = name + '.pdf'

    # Create a PDF document and specify the file path
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    # Create a table with the data
    table = Table(data)

    # Define the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font style for the header row
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Font size for the header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for the header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background color for data rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines for all cells
    ])

    # Apply the table style
    table.setStyle(table_style)

    # Build the PDF document
    elements = [table]
    doc.build(elements)

    print_centered(colored(f"Data exported in {file_path}", "green"))



def exportCsvData():
    to_csv = showData("SELECT id,name,age as birthday,city FROM student ORDER BY id",'')

    keys = to_csv[0].keys()
    name = input("Enter the name of the file: ")
    file_path = name+'.csv' 
    with open(file_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for row in to_csv:
            dict_writer.writerow(row)

    print_centered(colored(f"Data exported in {file_path}","green"))


def updateData():
    user_id = int(input("Enter id: "))
    sql = f"SELECT id,name,age as birthday,city FROM student WHERE id = {user_id}"
    cur.execute(sql)
    record = cur.fetchone()

    if record:
        user_name = input(f"Enter name({record['name']}): ")
        # user_age_input = input(f"Enter age ({record['age']}): ")
        # user_age = int(user_age_input) if user_age_input.strip() else record['age']
        user_age = input(f"Enter age ({record['birthday']}): ")
        user_city = input(f"Enter city({record['city']}): ")

        # Mise à jour des valeurs si elles ne sont pas vides
        if user_name.strip():
            record['name'] = user_name
        if user_age.strip():
            record['birthday'] = user_age
        if user_city.strip():
            record['city'] = user_city

        # Exécution de la mise à jour dans la base de données
        sql = f"UPDATE student SET name = '{record['name']}', age = '{record['birthday']}', city = '{record['city']}', updated_at = CURRENT_TIMESTAMP WHERE id = {user_id}"
        cur.execute(sql)
        conn.commit()
        print_centered(colored("Update successful.", "green"))
        record['modified'] = True
        id = user_id
        showData("SELECT id,name,age as birthday,city FROM student ORDER BY id",id)

    else:
        print_centered(colored("User ID does not exist.", "yellow"))

def searchOption():
    option = None
    os.system('clear')
    
    while option != 00 and option != 99:
        print_centered("================\n")
        print_centered(colored("\t   S E A R C H   O P T I O N\n","green"))
        print_centered("1. Search name")
        print_centered("2. Search between 2 dates")
        print_centered("3. Search date")
        print_centered("4. Search by month")
        print_centered("5. Search city\n\n")
        print_centered("00. return to Home")
        print_centered(colored("99. Exit", 'red'))
        
        option = input("Choose Option (1-5): ")

        if option not in ['99', '1', '2', '3','4','5', '00']:
            print_centered(colored("Invalid option. Please choose a number from 0 to 5.", "yellow"))
        else:
            option = int(option)  # Si vous souhaitez convertir l'option en entier, utilisez int(option)

            if option == 1:
                name= input("Enter here name :")
                showData(f"SELECT id,name,age as birthday,city FROM student WHERE LOWER(name) LIKE LOWER('%{name}%') ORDER BY id",'')
                
            if option == 2:
                date1= input("Enter here the first date(month - day) :")
                date2= input("Enter here the second date(month - day) :")
                
                query = f"SELECT id,name,age as birthday,city FROM student WHERE TO_DATE(CONCAT(EXTRACT(MONTH FROM age), '-', EXTRACT(DAY FROM age)), 'MM-DD') >= TO_DATE('{date1}', 'MM-DD') AND TO_DATE(CONCAT(EXTRACT(MONTH FROM age), '-', EXTRACT(DAY FROM age)), 'MM-DD') <= TO_DATE('{date2}', 'MM-DD')"
                # cur.execute(query)

                showData(query,'')
            
            if option == 3:
                date= input("Enter here the date(month - day) :")
                
                query = f"SELECT id,name,age as birthday,city FROM student WHERE TO_DATE(CONCAT(EXTRACT(MONTH FROM age), '-', EXTRACT(DAY FROM age)), 'MM-DD') = TO_DATE('{date}', 'MM-DD') "
                # cur.execute(query)

                showData(query,'')
                
            if option == 4:
                date1= input("Enter here the month( 1-12) :")
                
                query = f"SELECT id,name,age as birthday,city FROM student WHERE TO_DATE(CONCAT(EXTRACT(MONTH FROM age)), 'MM') = TO_DATE('{date1}', 'MM')"
                # cur.execute(query)

                showData(query,'')
                    
            if option == 5:
                city= input("Enter here city name :")
                showData(f"SELECT id,name,age as birthday,city FROM student WHERE LOWER(city) LIKE LOWER('%{city}%') ORDER BY id",'')
                
            if option == 00:
                os.system("clear")
                break    
                    
            if option == 99:
                os.system("clear")
                print_centered(colored("Thank you for using our software\n\n", "green"))
                exit()



def insertData():
    user_name = input("Enter name: ")
    user_age = input("Enter birthday: ")
    user_city = input("Enter city: ")
    sql = f"INSERT INTO student (name, age, city, added_at, updated_at) VALUES ('{user_name}', '{user_age}', '{user_city}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    cur.execute(sql)
    conn.commit()
    showData("SELECT id,name,age as birthday,city FROM student ORDER BY id",id)


def deleteData():
    user_id = int(input("Enter id to delete record: "))
    sql = f"SELECT id,name,age as birthday,city FROM student WHERE id={user_id} ORDER BY id"
    showData(sql,'')
    cur.execute(sql)
    record = cur.fetchone()
    if record:

        # Demande de confirmation à l'utilisateur
        confirmation = input("Are you sure you want to delete this record? (y/n): ")

        if confirmation.lower() == "y":
            sql = f"DELETE FROM student WHERE id = {user_id}"
            cur.execute(sql)
            conn.commit()
            print_centered(colored("Deletion successful.", "green"))

        else:
            print_centered(colored("Deletion canceled.", "yellow"))
        showData("SELECT id,name,age as birthday,city FROM student ORDER BY id",'')

    else:
        print_centered(colored("User ID does not exist.", "yellow"))

def showData(sql, id):
    cur.execute(sql)
    records = cur.fetchall()

    header = ['id', 'name', 'birthday', 'city']
    rows = []

    for user in records:
        row = [str(user['id']), user['name'], str(user['birthday']), user['city']]
        if id == user['id']:
            row = [colored(str(user['id']), 'green'), colored(user['name'], 'green'),
                   colored(str(user['birthday']), 'green'), colored(user['city'], 'green')]
        rows.append(row)

    table_width = shutil.get_terminal_size().columns
    column_width = (table_width - 2) // len(header)

    # Affichage de l'en-tête
    header_row = '|'.join([item.center(column_width) for item in header])
    print('=' * table_width)
    print(header_row)
    print('=' * table_width)

    # Affichage des lignes du tableau
    for i, row in enumerate(rows):
        if id == row[0]:
            row_str = '|'.join([str(item).center(column_width) for item in row])
            print(colored(row_str, 'green').center(table_width))
        else:
            row_str = '|'.join([str(item).center(column_width) for item in row])
            print(row_str)

    print('=' * table_width)

    return records






def print_centered(text):
    # Obtenir la largeur du terminal
    terminal_width = shutil.get_terminal_size().columns

    # Centrer le texte en fonction de la largeur du terminal
    centered_text = text.center(terminal_width)

    # Afficher le texte centré
    print(centered_text)


option = None

while option != 99:
    print_centered("================\n")
    print_centered(colored("\t      S T U D E N T    M A N A G E M E N T\n","green"))
    print_centered("1. Show Student")
    print_centered("2. Search")
    print_centered("3. Insert Student")
    print_centered("4. Update Student")
    print_centered("5. Delete Student")
    print_centered("6. Export Csv Student")
    print_centered("7. Export Pdf Student\n\n")
    print_centered("88. Clear screen")
    print_centered(colored("99. Exit", 'red'))

    # option = int(input("Choose Option (0-5): "))
    option = input("Choose Option (1-7): ")

    if option not in ['99','88', '1', '2', '3', '4', '5','6','7']:
        print_centered(colored("Invalid option. Please choose a number from 0 to 5.", "yellow"))

    else:
        option = int(option)  # Si vous souhaitez convertir l'option en entier, utilisez int(option)

        if option == 1:
            showData("SELECT id,name,age as birthday,city FROM student ORDER BY id","")
        elif option == 2:
            searchOption()
            
        elif option == 3:
            insertData()
        elif option == 4:
            updateData()
        elif option == 5:
            deleteData()
        elif option == 6:
            exportCsvData()
        elif option == 7:
            exportPdfData()
        if option == 88:
            os.system("clear")
        if option == 99:
            os.system('clear')
            print_centered(colored("Thank you for using our software\n\n", "green"))
            


