#!/bin/bash

# Функция для выполнения SQL-скрипта
run_sql_m() {
	local file_path="$1"

	if [ ! -f "$file_path" ]; then
		echo "Такого файла не существует: $file_path"
		exit 1
	else
		psql -U postgres -d lab2 -p 5432 -f "$file_path"
	
		if [ $? -eq 0 ]; then
			echo "Скрипт выполнен успешно: $file_path"
		else
			echo "Ошибка при выполнении скрипта: $file_path"
			exit 1
		fi
	fi
}

# Функция для выполнения SQL-запроса и получения результата
execute_query() {
	local query="$1"
	psql -U postgres -d lab2 -p 5432 -t -c "$query" | xargs
}


# Получение списка уже применённых миграций
get_applied_migrations() {
	execute_query "SELECT migration_name FROM migrations;"
}

# Добавление записи о применённой миграции
record_migration() {
	local migration_name="$1"
	local escaped_name=$(printf "%q" "$migration_name")
	local insert_query="INSERT INTO migrations (migration_name) VALUES ('$escaped_name');"
	psql -U postgres -d lab2 -p 5432 -c "$insert_query"
}

# Основная логика применения миграций
apply_migrations() {
	local migrations_dir="./migrations" # путь к вашей директории миграций

# Проверка существования директории миграций
	if [ ! -d "$migrations_dir" ]; then
		echo "Директория миграций не найдена: $migrations_dir"
		exit 1
	fi

# Получение списка уже применённых миграций
	local applied_migrations
	applied_migrations=$(get_applied_migrations)

# Перебор всех .sql файлов в директории миграций
	for migration_file in "$migrations_dir"/*.sql; do
# Проверка, существуют ли файлы миграций
	if [ ! -e "$migration_file" ]; then
		echo "Нет файлов миграций для применения в директории: $migrations_dir"
		exit 0
	fi

# Получение имени файла миграции без пути
	migration_name=$(basename "$migration_file")

# Проверка, была ли миграция уже применена
	if echo "$applied_migrations" | grep -q "^$migration_name$"; then
		echo "Миграция уже применена: $migration_name"
	else
		echo "Применение миграции: $migration_name"
		run_sql "$migration_file"
		record_migration "$migration_name"
	fi
done
}



# Применение миграций
apply_migrations
