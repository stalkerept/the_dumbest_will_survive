# with open("t.md", encoding='utf-8') as file:
#     sp = file.readlines()


# for i in sp:
#     n = i.split("|")
#     with open(n[0].strip(),"w", encoding="utf-8") as f:
#         k = n[1].split(",")       
#         for item in k:
#             f.write(f"[[{item.strip()}]], ")
#         f.write("\n")


## Перезапись

# with open("new.md", encoding='utf-8') as file:
#     sp = list(map(lambda x: x.split("|")[0].strip(), file.readlines()))


# with open("t.md", encoding="utf-8") as f:
#     old_sp = f.readlines()

# new_sp, cool = [], []
# for i in old_sp:
#     n = i.split("|")[0].strip()
#     if n not in sp:
#         new_sp.append(i)
#     else:
#         cool.append(i)

# with open("t.md", "w", encoding="utf-8") as f2:
#     for i in new_sp:
#         f2.write(i)

# with open("new.md", "w", encoding="utf-8") as f3:
#     for i in cool:
#         f3.write(i)


## Рандромайзер
# from random import shuffle as sh
# with open("t.md", encoding="utf-8") as file:
#     sp = file.readlines()

# for i in range(100000):
#     sh(sp)
# with open("new.md", "w", encoding="utf-8") as f:
#     for i in sp[:18]:
#         n = i.split("|")[0].strip()
#         f.write(f"{n}\n")
#         print(n)


## Запись
import sys
import os

def parse_titles(filepath):
    """Читает файл с названиями и возвращает словарь:
       ключ — название статьи без .md, значение — полное имя файла."""
    mapping = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            # Берём часть до '|' и обрезаем пробелы
            filename = line.split('|')[0].strip()
            if filename.endswith('.md'):
                key = filename[:-3]
                mapping[key] = filename
    return mapping

def parse_content(filepath):
    """Разбирает файл содержания на отдельные статьи, исключая заголовки первого уровня.
       Возвращает список кортежей (заголовок, текст статьи без заголовка)."""
    articles = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # читаем с сохранением символов перевода строки

    current_title = None
    current_lines = []

    def save_article():
        nonlocal current_title, current_lines
        if current_title is not None:
            body = ''.join(current_lines)
            # Убираем лишний завершающий перевод строки (опционально)
            articles.append((current_title, body.rstrip('\n')))
            current_title = None
            current_lines = []

    for line in lines:
        if line.startswith('# ') and not line.startswith('## '):
            save_article()
            current_title = line[2:].strip()
            # Строка заголовка не добавляется в current_lines
        else:
            if current_title is not None:
                current_lines.append(line)

    save_article()  # последняя статья
    return articles

def main():
    if len(sys.argv) >= 3:
        content_file = sys.argv[1]
        titles_file = sys.argv[2]
    else:
        content_file = 'good.md'
        titles_file = 'new.md'

    for fpath in (content_file, titles_file):
        if not os.path.exists(fpath):
            print(f'Ошибка: файл "{fpath}" не найден.')
            return

    title_to_filename = parse_titles(titles_file)
    print(f'Загружено целевых файлов: {len(title_to_filename)}')

    articles = parse_content(content_file)
    print(f'Найдено статей: {len(articles)}')

    written = 0
    written_files = set()
    for title, body in articles:
        if title in title_to_filename:
            target = title_to_filename[title]
            if not os.path.exists(target):
                print(f'Предупреждение: файл "{target}" не существует, пропускаем.')
                continue
            with open(target, 'w', encoding='utf-8') as f:
                f.write(body)
            print(f'Записано: {target}')
            written_files.add(target)
            written += 1
        else:
            print(f'Статья "{title}" не найдена в списке файлов, пропущена.')

    all_targets = set(title_to_filename.values())
    missed = all_targets - written_files
    if missed:
        print(f'Файлы из списка названий, для которых не нашлось статьи: {missed}')

    print(f'\nГотово. Записано файлов: {written}')

if __name__ == '__main__':
    main()