variables = {"C": "29", "B": "30"}

for name in variables:
	print("\033[45m", name, "\033[0m", sep=" ", end=" ")
	print("\033[0m", variables[name], "\033[0m", sep="")

while True:
	line = input()
	if line == "END":  # Завершаем работу программы.
		print("Завершение работы программы")
		exit(1)
		
	arguments = line.split()  # Разбиваем ввод на аргументы.
	# print(arguments)
	if len(arguments) <= 1:
		print("Недостаточно аргументов")
		continue
	if len(arguments) > 3:
		print("Слишком много аргументов")
		continue

	command = arguments[0]
	
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