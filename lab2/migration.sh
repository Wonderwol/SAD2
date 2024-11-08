#!/bin/bash

# Функция для выполнения SQL-скрипта
run_sql() {
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
    execute_query "SELECT trim(migration_name) FROM migrations;"
}

# Добавление записи о применённой миграции
record_migration() {
    local migration_name="$1"

    # Убираем пробелы и проверяем, есть ли уже такая миграция в базе
    migration_name=$(echo "$migration_name" | xargs)
    
    existing_migration=$(psql -U postgres -d lab2 -p 5432 -t -c "SELECT 1 FROM migrations WHERE trim(migration_name) = '$migration_name' LIMIT 1;")
    
    if [[ -z "$existing_migration" ]]; then
        # Если записи нет, вставляем её в таблицу
        local escaped_name=$(printf "%q" "$migration_name")
        local insert_query="INSERT INTO migrations (migration_name) VALUES ('$escaped_name');"
        psql -U postgres -d lab2 -p 5432 -c "$insert_query"
    else
        echo "Миграция с именем $migration_name уже применена"
    fi
}

# Применение миграций
apply_migrations() {
    local migrations_dir="./migrations"

    # Проверка существования директории миграций
    if [ ! -d "$migrations_dir" ]; then
        echo "Директория миграций не найдена: $migrations_dir"
        exit 1
    fi

    # Получение списка уже применённых миграций
    applied_migrations=$(get_applied_migrations)

    # Применение миграций
    for migration in "$migrations_dir"/*.sql; do
        migration_name=$(basename "$migration")
        
        # Преобразуем имя миграции для корректного сравнения
        normalized_name=$(echo "$migration_name" | xargs)  # Убираем лишние пробелы

        if ! echo "$applied_migrations" | grep -q "$normalized_name"; then
            echo "Применяется миграция: $migration_name"
            run_sql "$migration"
            record_migration "$migration_name"
        else
            echo "Миграция уже применена: $migration_name"
        fi
    done
}

export PGPASSWORD="postgres"

# Запуск применения миграций
apply_migrations
