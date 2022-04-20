import re
import string
from random import choice
from rich.console import Console

c = Console()
digit_pattern = re.compile(r'(\d+)')
solo_digit_pattern = re.compile(r'\s+(\d+)\s+')


def generate_random_text_with_numbers(symbols: int):
    """Випадковий набір символів з числами."""
    for _ in range(symbols):
        yield choice(string.ascii_letters + string.digits + '                  \n')


def all_digits_in_text(text):
    """Підрахунок суми усіх чисел у тексті."""
    solo_total = sum([int(match) for match in solo_digit_pattern.findall(text)])
    total = sum([int(match) for match in digit_pattern.findall(text)])
    return solo_total, total


if __name__ == '__main__':
    c.print("Генеруємо випадковий текст")
    text = ''.join([char for char in generate_random_text_with_numbers(1500)])
    solo_total, total = all_digits_in_text(text)
    text = solo_digit_pattern.sub(' [bold yellow]\\1[/bold yellow] ', text)
    text = digit_pattern.sub('[bold blue]\\1[/bold blue]', text)
    c.print(text)
    c.print(f'\nСума відокремлених чисел: [bold yellow]{solo_total}')
    c.print(f'\nСума усіх чисел у тексті: {total}')
