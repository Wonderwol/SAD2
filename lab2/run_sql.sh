#!/bin/bash

run_sql() {
local file_path="$1"

	if [ ! -f "$file_path" ]; then

		echo "Такого файла не существует"

	else

		psql -U postgres -d lab2 -p 5432 -f "$file_path"
		echo "Скрипт выполнен"
	fi
}

run_sql "$1"
