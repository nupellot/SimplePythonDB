global_variables = {"C": "29", "B": "30"}


# Функция для вывода текущего состояния бд.
def print_variables(variables, transaction_depth):
    print("\033[44m", "Текущее состояние базы", "\033[0m", end=" ")
    if transaction_depth != 0:
        print(f"({transaction_depth} вложенность транзакции)")
    else:
        print("")
    for name in variables:
        print("\033[45m", name, "\033[0m", sep=" ", end=" ")
        print("\033[0m", variables[name], "\033[0m", sep="")


# Главная цикличная функция для обработки команд пользователя.
def process_commands(global_variables, changes, transaction_depth):
    
    # Вечный цикл ждёт ввода и завершается при получении команды "END"
    while True:
        line = input(">" * (transaction_depth + 1) + " ")
        # Обарабыватем исключения.
        if line == "END":  # Штатно завершаем работу программы.
            print("Завершение работы программы")
            raise SystemExit
        arguments = line.split()  # Разбиваем ввод на аргументы.
        if len(arguments) < 1:
            print("Недостаточно аргументов")
            continue
        if len(arguments) > 3:
            print("Слишком много аргументов")
            continue

        
        # Обрабатываем команды пользователя.
        
        variables = global_variables | changes
        # Текущее локальное состояние переменных, с которым мы работаем.
        
        command = arguments[0]
        # Обработка команд, не изменяющих состояние БД.
        if command == "GET":
            print(variables.get(arguments[1]))
        elif command == "FIND":
            for key in variables:
                if variables[key] == arguments[1]:
                    print(key)
        elif command == "COUNTS":
            counter = 0
            for key in variables:
                if variables[key] == arguments[1]:
                    counter += 1
            print(counter)
        # Обработка команд, изменяющих состояние БД.
        elif command == "SET":
            if len(arguments) == 3:
                changes[arguments[1]] = arguments[2]
            else:
                print("Неподходящие аргументы. Верный формат: /SET <ИМЯ> <ЗНАЧЕНИЕ>")
        elif command == "UNSET":
            changes[arguments[1]] = "NULL"

        # Обрабатываем команды, связанные с транзакциями.
        elif command == "BEGIN":
            changes |= process_commands(global_variables, 
                                        changes.copy(), 
                                        transaction_depth + 1)
            for change in dict(changes):
                if changes[change] == "NULL":
                    changes.pop(change)
        elif command == "COMMIT":
            if transaction_depth != 0:
                return changes
            else:
                print("Нет транзакции, которую можно было бы завершить")
                continue
                
        elif command == "ROLLBACK":
            if transaction_depth != 0:
                return {}
            else:
                print("Нет транзакции, которую можно было бы завершить")
                continue
        # Транзакции реализованы через рекурсивный вызов главной функции.
        # Каждый вызов в стеке хранит ссылку на исходное состояние БД
        # а также свою копию всех совершенных в транзакции изменений.

        
        elif command == "HELP":  # В случае, если пользователь не угадал с командой.
            with open('help.txt', 'r') as file:
                print(file.read())
        else:
            print(f"Неизвестная команда \"{command}\". Используйте HELP")

        # Для удобства выводим текущее состояние БД после каждой команды.
        print_variables(global_variables | changes, transaction_depth)


# Запуск программы.
process_commands(global_variables, {}, 0)
