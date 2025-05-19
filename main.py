from sqlalchemy import text
from session import engine


def about():
    print("""
    ███████╗ ██████╗ ██╗          █████╗ ██████╗ ███████╗
    ██╔════╝██╔═══██╗██║         ██╔══██╗██╔══██╗██╔════╝
    ███████╗██║   ██║██║         ███████║██████╔╝███████╗
    ╚════██║██║   ██║██║         ██╔══██║██╔══██╗╚════██║
    ███████║╚██████╔╝███████╗    ██║  ██║██║  ██║███████║
    ╚══════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    
    SQL Query Runner v1.0
    Интерактивная утилита для работы с базой данных.
    Возможности:
    - Создание таблиц
    - Выполнение SELECT/INSERT/UPDATE/DELETE запросов
    - Автоматическое управление соединениями
    
    Нажмите Enter чтобы продолжить...
    """)
    input()
    return




def create_table():
    while True:
        print('-' * 10)
        question = input('Хотите создать базу данных? y/n ')
        if question == 'n' or question == 'N':
            print('-' * 10)
            print('Скорее всего башей базы данных нету. Рекомендую создать!')
        elif question == 'y' or question == 'Y':
            with engine.begin() as conn:
                print('-' * 10)
                sql = input("Введите запрос на создание таблицы\nПример(CREATE TABLE some_table (x int,y int)\n")

                if len(sql) == 0:
                    print('-' * 10)
                    sql = input("Введите запрос на создание таблицы\nПример(CREATE TABLE some_table (x int,y int)\n")

                try:
                    conn.execute(text(f'{sql}'))
                    print('База данных создана')
                    break
                except Exception as e:
                    print(f'Ошибка: {e}')
        else:
            print('Ждем ответа')




def main():
    while True:
        print('-' * 10)
        question = input('Хочешь выполнить sql запрос? y/n ')
        if question == 'y' or question == 'Y':
            print('-' * 10)
            sql_operation = input('Какой это будет оператор(SELECT,INSERT,UPDATE,DELETE): \n')
            if len(sql_operation) == 0:
                print('-' * 10)
                sql_operation = input('Какой это будет оператор(SELECT,INSERT,UPDATE,DELETE): \n')

            if sql_operation == 'INSERT' or sql_operation == 'UPDATE' or sql_operation == 'DELETE':
                with engine.begin() as conn:
                    print('-' * 10)
                    sql = input('Введи sql запрос\nПример:(SELECT * FROM table)\n$')

                    if len(sql) == 0:
                        print('-' * 10)
                        sql = input('Введи sql запрос\nПример:(INSERT INTO table (x,y) VALUES (1,2))\n$')

                    print(f'Оператор: {sql_operation}')

                    try:
                        conn.execute(text(f"{sql}"))
                        conn.commit()
                    except Exception as e:
                        print(f'Ошибка: {e}')

            elif sql_operation == 'SELECT':
                with engine.connect() as conn:
                    print(f'Оператор: {sql_operation}')

                    try:
                        print('-' * 10)
                        sql = input('Введи sql запрос\nПример:(SELECT * FROM table)\n$')
                        result = conn.execute(text(f"{sql}"))
                        for i in result.all():
                            print(i)
                    except Exception as e:
                        print(f'Ошибка: {e}')

            else:
                print('Такой операции нету')

        elif question == 'n' or question == 'N':
            print('-' * 10)
            print('Программа завершена')
            print('Все данные удалены')
            print('-' * 10)
            break

        else:
            print('Ждем ответа')


if __name__ == '__main__':
    about()
    create_table()
    main()