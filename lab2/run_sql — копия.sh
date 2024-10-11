#!/bin/bash
echo 'вавыавы'

run_sql() {
	local file_path="$1"

# Проверка, передан ли аргумент
	if [ -z "$file_path" ]; then
		echo "Ошибка: Путь к SQL-скрипту не указан."
		echo "Использование: $0 путь/к/скрипту.sql"
		return 1
	fi

# Проверка существования файла
	if [ ! -f "$file_path" ]; then
		echo "Такого файла не существует: $file_path"
		return 1
	else
# Выполнение SQL-скрипта с помощью psql
		psql -U postgres -d lab2 -f "$file_path"

# Проверка успешности выполнения psql
		if [ $? -eq 0 ]; then
			echo "Скрипт выполнен успешно: $file_path"
		else
			echo "Ошибка при выполнении скрипта: $file_path"
		return 1
		fi
	fi
}

# Вызов функции run_sql с аргументами скрипта
run_sql "$1"
