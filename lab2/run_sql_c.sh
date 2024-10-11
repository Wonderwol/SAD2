#!/bin/bash

run_sql_c() {
	local call="$1"

	psql -U postgres -d lab2 -p 5432 -t -c "$call"

	# Проверка успешности выполнения команды psql

	if [ $? -eq 0 ]; then

		echo "Запрос выполнен успешно: $call"

	else

		echo "Неверный запрос"	
	fi
}

run_sql_c "$1"
