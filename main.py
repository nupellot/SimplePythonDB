global_variables = {"C": "29", "B": "30"}


# Функция для вывода текущего состояния бд.
def print_variables(variables, transaction_depth):
    print("\033[42m", "Текущее состояние базы", "\033[0m", end=" ")
    print(f"({transaction_depth} вложенность транзакции)")
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

        variables = global_variables | changes
        command = arguments[0]
        # Обрабатываем команды пользователя.
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
        elif command == "SET":
            changes[arguments[1]] = arguments[2]
        elif command == "UNSET":
            changes[arguments[1]] = None

        # Обрабатываем команды, связанные с транзакциями.
        elif command == "BEGIN":
            changes |= process_commands(global_variables, 
                                        changes.copy(), 
                                        transaction_depth + 1)
        elif command == "COMMIT":
            return changes
        elif command == "ROLLBACK":
            return {}
        # Транзакции реализованы через рекурсивный вызов главной функции.
        
        elif command == "HELP":
            with open('help.txt', 'r') as file:
                read_file = file.read()
                print(read_file)
        else:
            print(f"Неизвестная команда \"{command}\". Используйте HELP")

        print_variables(global_variables | changes, transaction_depth)


process_commands(global_variables, {}, 0)
