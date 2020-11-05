import requests
from pathlib import Path
from rich.console import Console

c = Console()
CURRENT_DIR = Path(__file__).parent


def get_path_to_file() -> Path:
    """Повертає шлях до файлу. Конвертує відносний шлях у абсолютний."""
    path_to_file = Path(c.input('[cyan]Введіть шлях до файлу[/cyan]\n'))
    if not path_to_file.is_absolute():
        path_to_file = CURRENT_DIR / path_to_file
    if path_to_file.is_dir():
        c.print('[red]Ви ввели путь директорії[/red]')
        return get_path_to_file()
    return path_to_file


def get_file_content(path_to_file: Path) -> str:
    """Повертає вміст файлу."""
    with open(path_to_file, 'r') as file:
        return file.read().replace('\\n\\n', '\n\n')


def get_match_word() -> tuple[str, bool]:
    """Запитує у користувача слово до пошуку та чутливість пошуку до регістру."""
    match_word = c.input('[cyan]Введіть слово яке необхідно підрахувати: ')
    case_sensitive = c.input('[cyan]Чутливість до регістру? [Т/н] ')
    if not len(case_sensitive) or case_sensitive.lower() in 'y yes д да т так':
        case_sensitive = True
    else:
        case_sensitive = False
    return match_word, case_sensitive


def highlight_words_and_count(text: str, match: str, case_sensitive: bool = True) -> int:
    """Виводить текст файлу з підсвічуючи слова та виводячи їх кількість."""
    highlighted_text = text.split(' ')
    if not case_sensitive:
        text = text.lower()
        match = match.lower()
    match_counter = 0
    for index, word in enumerate(text.split(' ')):
        if word == match:
            match_counter += 1
            highlighted_text[index] = f'[bold yellow]{highlighted_text[index]}[/bold yellow]{{{match_counter}}}'
    c.print('\n' + ' '.join(highlighted_text))
    c.print(f'\n{match_counter} слова в тексті\n')
    return match_counter


def write_result_to_file(word: str, count: int):
    """Записує результат пошуку у файл."""
    path_to_result_file = CURRENT_DIR / 'result.txt'
    with open(CURRENT_DIR / 'result.txt', 'w') as file:
        file.write(f'{word}: {count}')
    c.print(f'Результат записано до [blue underline]{path_to_result_file}[/blue underline]')
    return path_to_result_file


def __generate_random_txt():
    """Генерує файл з випадковим текстом."""
    random_txt_path = CURRENT_DIR / 'random.txt'
    response_data = requests.get('https://fish-text.ru/get',
                        params={
                            'type': 'paragraph',
                            'number': 7,
                            'format': 'json'
                        }).json()
    if response_data['status'] == 'success':
        with open(random_txt_path, 'w') as file:
            text = response_data['text']
            file.writelines(text)
    else:
        raise ConnectionError
    return


if __name__ == '__main__':
    c.print("Генеруємо випадковий текст.")
    __generate_random_txt()
    path_to_file = get_path_to_file()
    file_content = get_file_content(path_to_file)
    match_word, case_sensitive = get_match_word()
    match_count = highlight_words_and_count(file_content, match_word, case_sensitive)
    write_result_to_file(match_word, match_count)
