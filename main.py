import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig(BaseSettings):
    """Конфигурация подключения к базе данных"""
    db_host: str = "localhost"
    db_port: str = "5432"
    db_user: str = "postgres"
    db_password: str = ""
    db_name: str = "postgres"
    db_type: str = "sqlite"

    @property
    def sync_db_url(self) -> str:
        """Формирует URL подключения к БД"""
        if self.db_type == "postgresql":
            return (
                f'postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
            )
        return 'sqlite+pysqlite:///:memory:'


class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)

    def get_tables(self) -> list[str]:
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    
    def table_exists(self, table_name: str) -> bool:
        """Проверяет существование таблицы"""
        return table_name in self.get_tables()
    
    def execute_query(self, sql: str, params: dict | None = None):
        """Выполняет SQL-запрос и возвращает результат"""
        try:
            with self.engine.begin() as conn:
                result = conn.execute(text(sql), params or {})
                if sql.strip().upper().startswith("SELECT"):
                    return result.fetchall()
                return result.rowcount
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка выполнения запроса: {e}") from e


class DatabaseError(Exception):
    """Кастомное исключение для ошибок БД"""
    pass


def setup_config() -> DatabaseConfig:
    """Настройка конфигурации подключения"""
    print('-' * 40)
    use_postgres = input("Хотите подключиться к PostgreSQL? (y/n): ").lower()
    
    config = {
        "db_type": "postgresql" if use_postgres == "y" else "sqlite"
    }
    
    if use_postgres == "y":
        config.update({
            "db_host": input("Введите host [localhost]: ") or "localhost",
            "db_port": input("Введите port [5432]: ") or "5432",
            "db_user": input("Введите пользователя [postgres]: ") or "postgres",
            "db_password": input("Введите пароль: "),
            "db_name": input("Введите имя БД [postgres]: ") or "postgres",
        })
    

    with open(".env", "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print(f"Конфигурация сохранена. Будет использоваться {config['db_type']}.")
    return DatabaseConfig(**config)


def show_tables(db: DatabaseManager):
    """Показывает список таблиц в БД"""
    tables = db.get_tables()
    if tables:
        print("\nСуществующие таблицы:")
        for table in tables:
            print(f"- {table}")
    else:
        print("\nВ базе данных нет таблиц.")


def create_table_interactive(db: DatabaseManager):
    """Интерактивное создание таблицы"""
    print('-' * 40)
    show_tables(db)
    
    table_name = input("\nВведите имя новой таблицы: ").strip()
    if not table_name:
        print("Имя таблицы не может быть пустым!")
        return
    
    if db.table_exists(table_name):
        print(f"Таблица {table_name} уже существует!")
        return
    
    print("\nВведите SQL для создания таблицы (например: CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT)):")
    sql = input("SQL> ")
    
    try:
        db.execute_query(sql)
        print(f"Таблица {table_name} успешно создана!")
    except DatabaseError as e:
        print(f"Ошибка: {e}")


def run_query_interactive(db: DatabaseManager):
    """Интерактивное выполнение запроса"""
    print('-' * 40)
    show_tables(db)
    
    print("\nДоступные операции: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP")
    sql = input("\nВведите SQL-запрос:\nSQL> ")
    
    try:
        result = db.execute_query(sql)
        
        if isinstance(result, list): 
            if not result:
                print("Запрос не вернул результатов.")
            else:
                print("\nРезультаты:")
                for row in result:
                    print(row)
        else:
            print(f"Запрос выполнен успешно. Затронуто строк: {result}")
    except DatabaseError as e:
        print(f"Ошибка выполнения: {e}")


def show_about():
    """Показывает информацию о программе"""
    print("""
    ███████╗ ██████╗ ██╗          █████╗ ██████╗ ███████╗
    ██╔════╝██╔═══██╗██║         ██╔══██╗██╔══██╗██╔════╝
    ███████╗██║   ██║██║         ███████║██████╔╝███████╗
    ╚════██║██║   ██║██║         ██╔══██║██╔══██╗╚════██║
    ███████║╚██████╔╝███████╗    ██║  ██║██║  ██║███████║
    ╚══════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

    SQL Query Runner v2.0
    Расширенная интерактивная утилита для работы с базами данных

    Возможности:
    - Поддержка PostgreSQL и SQLite
    - Просмотр существующих таблиц
    - Создание и изменение таблиц
    - Выполнение любых SQL-запросов
    - Безопасное управление соединениями

    Нажмите Enter чтобы продолжить...
    """)
    input()


def main_menu(db: DatabaseManager):
    """Главное меню программы"""
    while True:
        print('\n' + '-' * 40)
        print("ГЛАВНОЕ МЕНЮ")
        print('1. Показать таблицы')
        print('2. Создать таблицу')
        print('3. Выполнить SQL-запрос')
        print('4. О программе')
        print('0. Выход')
        
        choice = input('> ').strip()
        
        if choice == '1':
            show_tables(db)
        elif choice == '2':
            create_table_interactive(db)
        elif choice == '3':
            run_query_interactive(db)
        elif choice == '4':
            show_about()
        elif choice == '0':
            print('Завершение работы...')
            break
        else:
            print('Неверный выбор, попробуйте снова')


if __name__ == '__main__':
    if not os.path.exists('.env') or input("Переконфигурировать настройки? (y/n): ").lower() == 'y':
        config = setup_config()
    else:
        config = DatabaseConfig()
    
    db_manager = DatabaseManager(config.sync_db_url)
    
    try:
        main_menu(db_manager)
    except KeyboardInterrupt:
        print("\nПрограмма завершена по запросу пользователя")
    except Exception as e:
        print(f"Критическая ошибка: {e}")