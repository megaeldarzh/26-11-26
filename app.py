"""Dark desktop interface for the twelve exception-handling exercises."""

from __future__ import annotations

import importlib.util
import sys
import tkinter as tk
from decimal import Decimal
from pathlib import Path
from tkinter import ttk
from types import ModuleType
from typing import Callable


BASE_DIR = Path(__file__).resolve().parent
BACKGROUND = "#0b1120"
SIDEBAR = "#111827"
SURFACE = "#172033"
SURFACE_LIGHT = "#202c42"
TEXT = "#eef2ff"
MUTED = "#9aa8bf"
ACCENT = "#7c6cff"
ACCENT_HOVER = "#9588ff"
SUCCESS = "#55d6a5"
ERROR = "#ff758f"
FIELD = "#0f172a"

EXERCISES: dict[int, tuple[str, str]] = {
    1: ("Банковский счёт", "Баланс, снятие средств и проверка ошибок"),
    2: ("Среднее списка", "Среднее значение набора чисел"),
    3: ("Сумма из файла", "Чтение чисел из файла с диагностикой строк"),
    4: ("Авторизация", "Вход с блокировкой после трёх ошибок"),
    5: ("Калькулятор", "Арифметические операции и проверка результата"),
    6: ("Склад товаров", "Добавление товаров, остатки и продажи"),
    7: ("Регистрация", "Проверка всех полей пользователя"),
    8: ("Матрица", "Безопасное изменение элемента матрицы"),
    9: ("Заказы", "Заказ товара с проверкой склада и лимита"),
    10: ("Свои исключения", "Возраст, email и надёжность пароля"),
    11: ("Журнал ошибок", "Запись исключения в errors.log"),
    12: ("Библиотека", "Книги, выдача, возврат и сохранение данных"),
}


def load_exercise(number: int) -> ModuleType:
    """Load a numbered exercise module whose filename is not a valid import name."""
    matches = list(BASE_DIR.glob(f"{number:02d}_*.py"))
    if not matches:
        raise FileNotFoundError(f"Exercise module {path.name} was not found.")

    module_name = f"exception_exercise_{number:02d}"
    spec = importlib.util.spec_from_file_location(module_name, matches[0])
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load exercise module: {matches[0].name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class ExerciseApp:
    """Render a themed exercise selector and connect forms to exercise logic."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Exception Lab — Практика Python")
        self.root.geometry("1120x760")
        self.root.minsize(940, 640)
        self.root.configure(bg=BACKGROUND)

        self.modules = {number: load_exercise(number) for number in EXERCISES}
        self.inventory = self.modules[6].Inventory()
        self.authenticator = self.modules[4].Authenticator(
            {"student": "python123"}, max_attempts=3
        )
        self.matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        products = {
            "notebook": self.modules[9].OrderProduct(
                "notebook", Decimal("12.50"), 20
            ),
            "headphones": self.modules[9].OrderProduct(
                "headphones", Decimal("89.99"), 5
            ),
        }
        self.order_service = self.modules[9].OrderService(
            products, Decimal("500.00")
        )
        self.library, self.library_save_enabled, startup_message = (
            self._load_library()
        )
        self.current_number = 1
        self.fields: dict[str, tk.Widget] = {}

        self._configure_styles()
        self._build_layout()
        self.show_exercise(1)
        if startup_message:
            self._show_output(startup_message, is_error=True)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "TFrame",
            background=BACKGROUND,
        )
        style.configure(
            "Surface.TFrame",
            background=SURFACE,
        )
        style.configure(
            "Sidebar.TFrame",
            background=SIDEBAR,
        )
        style.configure(
            "Title.TLabel",
            background=BACKGROUND,
            foreground=TEXT,
            font=("Segoe UI", 25, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=BACKGROUND,
            foreground=MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardTitle.TLabel",
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Field.TLabel",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "SidebarTitle.TLabel",
            background=SIDEBAR,
            foreground=TEXT,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "SidebarCaption.TLabel",
            background=SIDEBAR,
            foreground=MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Exercise.TButton",
            background=SIDEBAR,
            foreground="#cbd5e1",
            borderwidth=0,
            focusthickness=0,
            padding=(12, 9),
            anchor="w",
            font=("Segoe UI", 9),
        )
        style.map(
            "Exercise.TButton",
            background=[("active", SURFACE_LIGHT), ("pressed", SURFACE_LIGHT)],
            foreground=[("active", TEXT), ("pressed", TEXT)],
        )
        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=(18, 11),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", ACCENT_HOVER), ("pressed", ACCENT_HOVER)],
        )
        style.configure(
            "TEntry",
            fieldbackground=FIELD,
            foreground=TEXT,
            insertcolor=TEXT,
            bordercolor=SURFACE_LIGHT,
            lightcolor=SURFACE_LIGHT,
            darkcolor=SURFACE_LIGHT,
            padding=9,
        )
        style.configure(
            "TCombobox",
            fieldbackground=FIELD,
            background=FIELD,
            foreground=TEXT,
            arrowcolor=TEXT,
            bordercolor=SURFACE_LIGHT,
            padding=8,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", FIELD)],
            foreground=[("readonly", TEXT)],
            selectbackground=[("readonly", FIELD)],
            selectforeground=[("readonly", TEXT)],
        )
        style.configure(
            "TScrollbar",
            background=SURFACE_LIGHT,
            troughcolor=SURFACE,
            bordercolor=SURFACE,
            arrowcolor=MUTED,
        )

    def _build_layout(self) -> None:
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", padding=(18, 24))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)

        ttk.Label(
            self.sidebar,
            text="EXCEPTION\nLAB",
            style="SidebarTitle.TLabel",
            justify="left",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            self.sidebar,
            text="PYTHON PRACTICE · 12 TASKS",
            style="SidebarCaption.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(5, 20))

        self.nav_buttons: dict[int, ttk.Button] = {}
        for row, (number, (title, _)) in enumerate(EXERCISES.items(), start=2):
            button = ttk.Button(
                self.sidebar,
                text=f"{number:02d}   {title}",
                style="Exercise.TButton",
                command=lambda selected=number: self.show_exercise(selected),
            )
            button.grid(row=row, column=0, sticky="ew", pady=2)
            self.nav_buttons[number] = button

        ttk.Label(
            self.sidebar,
            text="Каждое задание использует\nсвою проверенную логику.",
            style="SidebarCaption.TLabel",
            justify="left",
        ).grid(row=len(EXERCISES) + 3, column=0, sticky="sw", pady=(26, 0))

        self.main_area = ttk.Frame(self.root, padding=(34, 28, 34, 24))
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(3, weight=1)

        self.heading = ttk.Label(self.main_area, style="Title.TLabel")
        self.heading.grid(row=0, column=0, sticky="w")
        self.subtitle = ttk.Label(self.main_area, style="Subtitle.TLabel")
        self.subtitle.grid(row=1, column=0, sticky="w", pady=(5, 22))

        self.form_card = ttk.Frame(
            self.main_area, style="Surface.TFrame", padding=(22, 18)
        )
        self.form_card.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        self.form_card.grid_columnconfigure(0, weight=1)
        ttk.Label(
            self.form_card, text="Параметры задания", style="CardTitle.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 16))
        self.form_body = ttk.Frame(self.form_card, style="Surface.TFrame")
        self.form_body.grid(row=1, column=0, sticky="ew")
        self.form_body.grid_columnconfigure(0, weight=1)
        self.form_body.grid_columnconfigure(1, weight=2)

        self.action_row = ttk.Frame(self.form_card, style="Surface.TFrame")
        self.action_row.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        self.action_row.grid_columnconfigure(1, weight=1)
        self.run_button = ttk.Button(
            self.action_row,
            text="Выполнить",
            style="Accent.TButton",
            command=self.run_selected,
        )
        self.run_button.grid(row=0, column=0, sticky="w")
        self.form_hint = ttk.Label(
            self.action_row,
            text="",
            style="Field.TLabel",
            wraplength=430,
            justify="left",
        )
        self.form_hint.grid(row=0, column=1, sticky="e", padx=(18, 0))

        self.result_card = ttk.Frame(
            self.main_area, style="Surface.TFrame", padding=(22, 18)
        )
        self.result_card.grid(row=3, column=0, sticky="nsew")
        self.result_card.grid_columnconfigure(0, weight=1)
        self.result_card.grid_rowconfigure(1, weight=1)
        self.result_header = ttk.Frame(self.result_card, style="Surface.TFrame")
        self.result_header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(
            self.result_header, text="Результат", style="CardTitle.TLabel"
        ).pack(side="left")
        self.result_state = tk.Label(
            self.result_header,
            text="ГОТОВО",
            background="#153a35",
            foreground=SUCCESS,
            font=("Segoe UI", 8, "bold"),
            padx=9,
            pady=4,
        )
        self.result_state.pack(side="right")

        output_frame = ttk.Frame(self.result_card, style="Surface.TFrame")
        output_frame.grid(row=1, column=0, sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)
        self.output = tk.Text(
            output_frame,
            height=8,
            wrap="word",
            background=FIELD,
            foreground=TEXT,
            insertbackground=TEXT,
            selectbackground=ACCENT,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=12,
            font=("Cascadia Code", 10),
            state="disabled",
        )
        self.output.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=scrollbar.set)

    def _load_library(self) -> tuple[ModuleType, bool, str]:
        """Load saved books while keeping damaged or inaccessible data explicit."""
        library_module = self.modules[12]
        storage_path = BASE_DIR / "library.json"
        try:
            return library_module.Library.load(storage_path), True, ""
        except FileNotFoundError:
            return library_module.Library(), True, "Библиотека ещё не сохранена. Начата новая."
        except PermissionError as error:
            return (
                library_module.Library(),
                False,
                f"Нет доступа к library.json; библиотека работает без сохранения.\n{error}",
            )
        except library_module.InvalidLibraryDataError as error:
            return (
                library_module.Library(),
                False,
                f"Файл library.json повреждён; он не будет перезаписан.\n{error}",
            )
        except OSError as error:
            return (
                library_module.Library(),
                False,
                f"Не удалось загрузить library.json; сохранение отключено.\n{error}",
            )

    def _field(
        self,
        row: int,
        key: str,
        label: str,
        default: str = "",
        *,
        choices: tuple[str, ...] = (),
        password: bool = False,
    ) -> None:
        ttk.Label(self.form_body, text=label, style="Field.TLabel").grid(
            row=row, column=0, sticky="w", padx=(0, 18), pady=6
        )
        if choices:
            widget: tk.Widget = ttk.Combobox(
                self.form_body,
                values=choices,
                state="readonly",
            )
            widget.set(default or choices[0])
        else:
            widget = ttk.Entry(
                self.form_body,
                show="•" if password else "",
            )
            widget.insert(0, default)
        widget.grid(row=row, column=1, sticky="ew", pady=6)
        self.fields[key] = widget

    def _value(self, key: str) -> str:
        widget = self.fields[key]
        return str(widget.get()).strip()

    def show_exercise(self, number: int) -> None:
        """Display the requested exercise and its input form."""
        if number not in EXERCISES:
            return
        self.current_number = number
        title, description = EXERCISES[number]
        self.heading.configure(text=title)
        self.subtitle.configure(text=f"Задание {number:02d}  ·  {description}")
        self.fields.clear()
        for child in self.form_body.winfo_children():
            child.destroy()

        for exercise_number, button in self.nav_buttons.items():
            if exercise_number == number:
                button.configure(style="Accent.TButton")
            else:
                button.configure(style="Exercise.TButton")

        self._build_form(number)
        self._show_output(
            "Заполни поля и нажми «Выполнить».\n"
            "Ошибки и результаты появятся здесь.",
            is_error=False,
        )

    def _build_form(self, number: int) -> None:
        """Create inputs appropriate to the selected exercise."""
        forms: dict[int, Callable[[], None]] = {
            1: lambda: (
                self._field(0, "balance", "Начальный баланс", "100"),
                self._field(1, "amount", "Сумма снятия", "25"),
            ),
            2: lambda: self._field(
                0, "numbers", "Числа через пробел", "1 2 3 4 5"
            ),
            3: lambda: self._field(
                0, "file_path", "Путь к файлу", "numbers.txt"
            ),
            4: lambda: (
                self._field(0, "username", "Логин", "student"),
                self._field(1, "password", "Пароль", password=True),
            ),
            5: lambda: (
                self._field(0, "left", "Первое число", "8"),
                self._field(
                    1,
                    "operation",
                    "Операция",
                    "+",
                    choices=("+", "-", "*", "/", "//", "%", "**"),
                ),
                self._field(2, "right", "Второе число", "2"),
            ),
            6: self._build_inventory_form,
            7: lambda: (
                self._field(0, "name", "Имя", "Alice"),
                self._field(1, "age", "Возраст", "25"),
                self._field(2, "email", "Email", "alice@example.com"),
                self._field(3, "password", "Пароль", password=True),
            ),
            8: lambda: (
                self._field(0, "row", "Строка (индекс с 0)", "0"),
                self._field(1, "column", "Столбец (индекс с 0)", "0"),
                self._field(2, "new_value", "Новое целое значение", "42"),
            ),
            9: self._build_order_form,
            10: lambda: (
                self._field(0, "name", "Имя", "Alice"),
                self._field(1, "age", "Возраст", "25"),
                self._field(2, "email", "Email", "alice@example.com"),
                self._field(3, "password", "Пароль", password=True),
            ),
            11: lambda: self._field(
                0, "integer", "Целое число (для ошибки введи текст)", "abc"
            ),
            12: self._build_library_form,
        }
        forms[number]()

        hints = {
            4: "Демо-учётная запись: student / python123",
            6: "Остатки сохраняются во время работы приложения.",
            8: f"Матрица: {self._matrix_text()}",
            9: "Товары: notebook и headphones · лимит заказа 500",
            11: "Ошибочный ввод будет записан в errors.log.",
            12: "Изменения библиотеки сохраняются в library.json.",
        }
        self.form_hint.configure(text=hints.get(number, ""))

    def _build_inventory_form(self) -> None:
        self._field(
            0,
            "action",
            "Действие",
            "Посмотреть товары",
            choices=(
                "Посмотреть товары",
                "Добавить товар",
                "Изменить остаток",
                "Продать товар",
            ),
        )
        self._field(1, "product_name", "Название товара")
        self._field(2, "price", "Цена (для добавления)", "10.00")
        self._field(3, "quantity", "Количество", "1")

    def _build_order_form(self) -> None:
        self._field(
            0,
            "product_name",
            "Товар",
            "notebook",
            choices=("notebook", "headphones"),
        )
        self._field(1, "quantity", "Количество", "2")

    def _build_library_form(self) -> None:
        self._field(
            0,
            "action",
            "Действие",
            "Список книг",
            choices=("Список книг", "Добавить книгу", "Найти книгу", "Выдать", "Вернуть"),
        )
        self._field(1, "title", "Название книги")
        self._field(2, "author", "Автор (для добавления)")

    def _show_output(self, message: str, *, is_error: bool) -> None:
        """Render a result and update the status badge."""
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", message)
        self.output.configure(state="disabled")
        self.result_state.configure(
            text="ОШИБКА" if is_error else "ГОТОВО",
            foreground=ERROR if is_error else SUCCESS,
            background="#3b1d2b" if is_error else "#153a35",
        )

    def _matrix_text(self) -> str:
        return "\n".join("  ".join(map(str, row)) for row in self.matrix)

    def _run_bank_account(self) -> str:
        module = self.modules[1]
        balance = module.parse_amount(self._value("balance"), "Баланс")
        amount = module.parse_amount(self._value("amount"), "Сумма")
        account = module.BankAccount(balance)
        new_balance = account.withdraw(amount)
        return f"Операция выполнена.\nНовый баланс: {new_balance}"

    def _run_average(self) -> str:
        module = self.modules[2]
        numbers = module.parse_numbers(self._value("numbers"))
        average = module.calculate_average(numbers)
        return f"Среднее значение: {average:g}"

    def _run_file_sum(self) -> str:
        module = self.modules[3]
        raw_path = self._value("file_path") or "numbers.txt"
        file_path = Path(raw_path)
        if not file_path.is_absolute():
            file_path = BASE_DIR / file_path
        total = module.sum_file_numbers(file_path)
        return f"Файл: {file_path.name}\nСумма чисел: {total:g}"

    def _run_authentication(self) -> str:
        self.authenticator.authenticate(
            self._value("username"),
            self._value("password"),
        )
        return "Вход выполнен успешно."

    def _run_calculator(self) -> str:
        module = self.modules[5]
        left = module.parse_number(self._value("left"), "Первое число")
        right = module.parse_number(self._value("right"), "Второе число")
        operator = self._value("operation")
        result = module.calculate(left, operator, right)
        return f"{left:g} {operator} {right:g} = {result:g}"

    def _run_inventory(self) -> str:
        module = self.modules[6]
        action = self._value("action")
        name = self._value("product_name")
        if action == "Посмотреть товары":
            products = self.inventory.list_products()
            if not products:
                return "Склад пуст. Добавь товар, чтобы начать."
            return "\n".join(
                f"{item.name}  ·  {item.price} за шт.  ·  остаток: {item.quantity}"
                for item in products
            )
        if action == "Добавить товар":
            price = module.parse_price(self._value("price"))
            quantity = module.parse_quantity(
                self._value("quantity"), allow_zero=True
            )
            product = self.inventory.add_product(name, price, quantity)
            return f"Добавлен товар: {product.name}\nЦена: {product.price}\nОстаток: {product.quantity}"
        quantity = module.parse_quantity(
            self._value("quantity"),
            allow_zero=action == "Изменить остаток",
        )
        if action == "Изменить остаток":
            product = self.inventory.update_quantity(name, quantity)
            return f"Остаток для «{product.name}» теперь: {product.quantity}"
        total = self.inventory.sell(name, quantity)
        product = self.inventory.products[name.strip()]
        return (
            f"Продано: {quantity} × {product.name}\n"
            f"Сумма: {total}\nОсталось на складе: {product.quantity}"
        )

    def _run_registration(self) -> str:
        module = self.modules[7]
        age = module.parse_age(self._value("age"))
        user = module.register_user(
            self._value("name"),
            age,
            self._value("email"),
            self._value("password"),
        )
        return f"Регистрация прошла успешно.\nПользователь: {user.name}"

    def _run_matrix(self) -> str:
        module = self.modules[8]
        row = module.parse_index(self._value("row"), "Индекс строки")
        column = module.parse_index(self._value("column"), "Индекс столбца")
        value = module.parse_new_value(self._value("new_value"))
        module.update_matrix(self.matrix, row, column, value)
        return f"Матрица обновлена:\n{self._matrix_text()}"

    def _run_order(self) -> str:
        module = self.modules[9]
        quantity = module.parse_quantity(self._value("quantity"))
        order = self.order_service.create_order(
            self._value("product_name"), quantity
        )
        return (
            f"Заказ принят.\n{order.quantity} × {order.product_name}\n"
            f"Итого: {order.total}"
        )

    def _run_custom_registration(self) -> str:
        module = self.modules[10]
        try:
            age = int(self._value("age"))
        except ValueError as error:
            raise ValueError("Возраст должен быть целым числом.") from error
        user_name = module.register_user(
            self._value("name"),
            age,
            self._value("email"),
            self._value("password"),
        )
        return f"Регистрация прошла успешно.\nПользователь: {user_name}"

    def _run_error_logging(self) -> str:
        module = self.modules[11]
        try:
            value = int(self._value("integer"))
        except ValueError as error:
            try:
                module.log_exception(
                    ValueError(f"{self._value('integer')!r} is not a whole number."),
                    BASE_DIR / "errors.log",
                )
            except PermissionError as log_error:
                raise OSError(
                    f"Ошибка ввода сохранена не была: нет доступа к errors.log ({log_error})"
                ) from log_error
            except OSError as log_error:
                raise OSError(
                    f"Не удалось записать errors.log: {log_error}"
                ) from log_error
            raise ValueError(
                f"«{self._value('integer')}» — не целое число.\n"
                "Ошибка записана в errors.log."
            ) from error
        return f"Введено целое число: {value}"

    def _save_library(self) -> str:
        if not self.library_save_enabled:
            return " Изменение только в памяти: сохранение отключено из-за ошибки загрузки."
        try:
            self.library.save(BASE_DIR / "library.json")
        except PermissionError as error:
            return f"\nНет доступа для сохранения library.json: {error}"
        except OSError as error:
            return f"\nНе удалось сохранить library.json: {error}"
        return "\nИзменения сохранены в library.json."

    def _run_library(self) -> str:
        module = self.modules[12]
        action = self._value("action")
        title = self._value("title")
        if action == "Список книг":
            if not self.library.books:
                return "Библиотека пока пуста."
            return "\n".join(
                f"{book.title} — {book.author} "
                f"[{'выдана' if book.borrowed else 'доступна'}]"
                for book in self.library.books.values()
            )
        if action == "Добавить книгу":
            book = self.library.add_book(title, self._value("author"))
            return f"Добавлена книга «{book.title}».{self._save_library()}"
        if action == "Найти книгу":
            book = self.library.search_book(title)
            status = "выдана" if book.borrowed else "доступна"
            return f"{book.title} — {book.author}\nСтатус: {status}"
        if action == "Выдать":
            book = self.library.borrow_book(title)
            return f"Книга «{book.title}» выдана.{self._save_library()}"
        book = self.library.return_book(title)
        return f"Книга «{book.title}» возвращена.{self._save_library()}"

    def run_selected(self) -> None:
        """Execute the selected assignment and show its result or error."""
        actions: dict[int, Callable[[], str]] = {
            1: self._run_bank_account,
            2: self._run_average,
            3: self._run_file_sum,
            4: self._run_authentication,
            5: self._run_calculator,
            6: self._run_inventory,
            7: self._run_registration,
            8: self._run_matrix,
            9: self._run_order,
            10: self._run_custom_registration,
            11: self._run_error_logging,
            12: self._run_library,
        }
        try:
            message = actions[self.current_number]()
        except self.modules[4].AccountLockedError as error:
            message = str(error)
            self._show_output(message, is_error=True)
            return
        except self.modules[4].InvalidCredentialsError as error:
            message = str(error)
            self._show_output(message, is_error=True)
            return
        except self.modules[7].RegistrationValidationError as error:
            message = "\n".join(f"• {item}" for item in error.errors)
            self._show_output(message, is_error=True)
            return
        except self.modules[10].InvalidAgeError as error:
            message = f"Ошибка возраста: {error}"
            self._show_output(message, is_error=True)
            return
        except self.modules[10].InvalidEmailError as error:
            message = f"Ошибка email: {error}"
            self._show_output(message, is_error=True)
            return
        except self.modules[10].WeakPasswordError as error:
            message = f"Ошибка пароля: {error}"
            self._show_output(message, is_error=True)
            return
        except self.modules[12].BookNotFoundError as error:
            message = f"Книга не найдена: {error}"
            self._show_output(message, is_error=True)
            return
        except self.modules[12].BookAlreadyBorrowedError as error:
            message = f"Книга уже выдана: {error}"
            self._show_output(message, is_error=True)
            return
        except self.modules[12].BookNotBorrowedError as error:
            message = f"Книга не была выдана: {error}"
            self._show_output(message, is_error=True)
            return
        except self.modules[12].BookAlreadyExistsError as error:
            message = f"Такая книга уже есть: {error}"
            self._show_output(message, is_error=True)
            return
        except (
            ValueError,
            KeyError,
            TypeError,
            OSError,
            ArithmeticError,
            RuntimeError,
        ) as error:
            message = str(error)
            self._show_output(message, is_error=True)
            return
        self._show_output(message, is_error=False)

    def _on_close(self) -> None:
        """Persist the current library state when the window is closed."""
        if self.library_save_enabled:
            try:
                self.library.save(BASE_DIR / "library.json")
            except PermissionError as error:
                self._show_output(
                    f"Нет доступа для сохранения library.json: {error}",
                    is_error=True,
                )
                return
            except OSError as error:
                self._show_output(
                    f"Не удалось сохранить library.json: {error}",
                    is_error=True,
                )
                return
        self.root.destroy()


def main() -> None:
    """Launch the desktop application."""
    root = tk.Tk()
    ExerciseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
