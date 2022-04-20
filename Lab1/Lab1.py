from random import randbytes
from rich import print
from rich.table import Table


class Matrix:
    """Матриця."""
    def __init__(self, width: int, height: int):
        """Ініціалізація."""
        self.width = width
        self.height = height
        self.matrix = [
            [randbytes(1) for _ in range(width)]
            for _ in range(height)
        ]

    def vertical_shift(self, shift: int):
        """Зміщення матриці вертикально."""
        self.display()
        shift %= len(self.matrix)
        self.matrix = self.matrix[shift:] + self.matrix[:shift]
        print(f"Зміщення на {shift}")
        self.display(shift)

    def display(self, shift: int = 0):
        """Вивід матриці."""
        table = Table(expand=True)
        table.add_column('РЕАЛЬНИЙ ІНДЕКС | ІНДЕКС ЗМІЩЕННЯ', justify='center')
        for index, _ in enumerate(range(self.width)):
            table.add_column(f'[bold red]{index + 1}', justify='center')
        for index, row in enumerate(self.matrix):
            real_index = f'{index + 1}'
            shifted_index = (index + 1 + shift)
            if shifted_index > self.height:
                shifted_index = shifted_index % self.height
            table.add_row(f'[bold blue]{str(real_index).rjust(3, "0")}[/bold blue] | [bold red]{str(shifted_index).rjust(3, "0")}[/bold red]', *map(lambda x: f'{str(x)[2:-1]} ({int.from_bytes(x, "big")})', row))
        print(table)


if __name__ == '__main__':
    print("Мазур Олег Володимирович")
    print("Створюємо матрицю 9x20 з випадковими байтами всередені")
    matrix = Matrix(9, 20)
    matrix.vertical_shift(5)
