import os
import re
import sys

def clean_filename(raw_name):
    """Убирает пометку (РЕВИЗИЯ) в конце имени, удаляет лишние пробелы."""
    name = raw_name.strip()
    # Удаляем суффикс " (РЕВИЗИЯ)" с любым числом пробелов перед ним
    name = re.sub(r'\s*\(РЕВИЗИЯ\)\s*$', '', name)
    # Если после удаления имя заканчивается на .md, оставляем как есть
    if not name.endswith('.md'):
        name += '.md'
    return name

def remove_first_h1(lines):
    """Удаляет первую строку, начинающуюся с '# ' (с учётом возможных ведущих пробелов)."""
    result = []
    removed = False
    for line in lines:
        stripped = line.lstrip()
        if not removed and stripped.startswith('# '):
            removed = True
            continue
        result.append(line)
    # Убираем пустые строки в самом начале результата (опционально)
    while result and result[0].strip() == '':
        result.pop(0)
    return result

def extract_files(source_path, output_dir):
    with open(source_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig убирает BOM, если есть
        text = f.read()

    # Регулярка: ищем блоки FILE START ... FILE END.
    # Используем ^ и $ с MULTILINE, захватываем имя файла и содержимое.
    pattern = r'^--- FILE START: (.+?) ---$\n(.*?)\n--- FILE END ---$'
    matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

    if not matches:
        print("Не найдено ни одного блока FILE START/FILE END.")
        return

    os.makedirs(output_dir, exist_ok=True)
    created = 0

    for raw_filename, content in matches:
        filename = clean_filename(raw_filename)
        lines = content.splitlines(keepends=False)
        # Удаляем первый заголовок первого уровня
        lines = remove_first_h1(lines)
        result_content = '\n'.join(lines)

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result_content)
        print(f'Сохранён: {filepath}')
        created += 1

    print(f'Готово. Создано/обновлено файлов: {created}')

if __name__ == '__main__':
    source = input('Путь к исходному файлу: ').strip()
    if not os.path.isfile(source):
        print(f'Ошибка: файл "{source}" не найден.')
        sys.exit(1)

    output = input('Путь к папке для сохранения: ').strip()
    if not output:
        print('Ошибка: путь к папке не может быть пустым.')
        sys.exit(1)

    extract_files(source, output)