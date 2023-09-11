class Database:
    def __init__(self):
        self.data = {}  # Словарь для хранения данных.
        self.transactions = []  # Стек для хранения изменений в транзакциях.

    def set(self, key, value):
        # Записываем изменение в текущую транзакцию либо в основное хранилище.
        if self.transactions:
            self.transactions[-1][key] = value
        else:
            self.data[key] = value

    def get(self, key):
        return self.data.get(key, "NULL")

    def unset(self, key):
        # Записываем изменение в текущую транзакцию
        if self.transactions:
            self.transactions[-1][key] = None
        elif key in self.data:
            del self.data[key]

    def count(self, value):
        count = list(self.data.values()).count(value)
        return count

    def find(self, value):
        found_keys = [key for key, val in self.data.items() if val == value]
        return found_keys

    def begin(self):
        self.transactions.append({})

    def rollback(self):
        if self.transactions:
            self.transactions.pop()
    
    def commit(self):
        if self.transactions:
            current_transaction = self.transactions.pop()
            for key, value in current_transaction.items():
                if value is None:
                    if key in self.data:
                        del self.data[key]
                else:
                    self.data[key] = value
    
    def get_transaction_depth(self):
        return len(self.transactions)

    # Метод для вывода текущего состояния бд.
    def print_variables(self):
        print("\033[44m", "Список переменных (До применения транзакций)", "\033[0m")
        for name in self.data:
            print("\033[45m", name, "\033[0m", sep=" ", end=" ")
            print("\033[0m", self.data[name], "\033[0m", sep="")

    def help():
        with open('help.txt', 'r') as file:
            print(file.read())


# Главная функция приложения
def main():
    db = Database()

    while True:
        try:
            command = input("> " * (db.get_transaction_depth() + 1)).split()
            if not command:
                continue
            cmd = command[0]

            if cmd == "SET":
                key, value = command[1], command[2]
                db.set(key, value)
            elif cmd == "GET":
                key = command[1]
                print(db.get(key))
                continue
            elif cmd == "UNSET":
                key = command[1]
                db.unset(key)
            elif cmd == "COUNTS":
                value = command[1]
                print(db.count(value))
                continue
            elif cmd == "FIND":
                value = command[1]
                keys = db.find(value)
                print(" ".join(keys))
                continue
            elif cmd == "BEGIN":
                db.begin()
            elif cmd == "ROLLBACK":
                db.rollback()
            elif cmd == "COMMIT":
                db.commit()
            elif cmd == "HELP":
                db.help()
                continue
            elif cmd == "END":
                break
            else:
                print(f"Неизвестная команда \"{command}\". Используйте HELP")
                continue

        except EOFError:
            print("Приложение завершено.")
            break

        if db.get_transaction_depth() == 0:
            db.print_variables()

if __name__ == "__main__":
    main()
