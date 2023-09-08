variables = {"C": "29", "B": "30"}


def print_variables(variables, transaction_depth):
	print("\033[42m", "Текущее состояние базы", "\033[0m", end=" ")
	print(f"({transaction_depth} вложенность транзакции)")
	for name in variables:
		print("\033[45m", name, "\033[0m", sep=" ", end=" ")
		print("\033[0m", variables[name], "\033[0m", sep="")


def process_commands(variables, transaction_depth):
	while True:
		line = input(">" * (transaction_depth + 1) + " ")
		if line == "END":  # Завершаем работу программы.
			print("Завершение работы программы")
			raise SystemExit
		arguments = line.split()  # Разбиваем ввод на аргументы.
		if len(arguments) < 1:
			print("Недостаточно аргументов")
			continue
		if len(arguments) > 3:
			print("Слишком много аргументов")
			continue
	
		command = arguments[0]
		# Начинаем обработку команд.
		if command == "GET":
			print(variables.get(arguments[1]))
		if command == "SET":
			variables[arguments[1]] = arguments[2]
		if command == "UNSET":
			variables.pop(arguments[1])
		if command == "COUNTS":
			counter = 0
			for key in variables:
				if variables[key] == arguments[1]:
					counter += 1
			print(counter)
		if command == "FIND":
			for key in variables:
				if variables[key] == arguments[1]:
					print(key)
			
		if command == "BEGIN":
			new_variables = process_commands(variables.copy(), transaction_depth + 1)
			if new_variables is not None:
				variables = new_variables.copy()
		if command == "COMMIT":
			return variables
		if command == "ROLLBACK":
			return None
			
		print_variables(variables, transaction_depth)


process_commands(variables, 0)


def get(variables, key):
	print(variables.get(key))
	
def set(variables, key, value):
	variables[key] = value
	
def unset(variables, key):
	variables.pop(key)
	
def counts(variables, value):
	counter = 0
	for key in variables:
		if variables[key] == value:
			counter += 1
	print(counter)
	
def counts(variables, value):
	for key in variables:
		if variables[key] == value:
			print(key)