# TX12 YouTube Controller

Керування відтворенням YouTube у Google Chrome за допомогою кнопок **A** та **D** передавача RadioMaster TX12, підключеного до macOS через USB.

## Можливості

| Дія | Коротке натискання | Утримання |
|---|---|---|
| A | Попереднє відео | Перемотування назад |
| D | Наступне відео | Перемотування вперед |

Поточні параметри утримання:
- поріг довгого натискання: 0,45 с;
- крок перемотування: 5 секунд;
- інтервал повторення: 0,5 с.

Одночасне натискання A + D задумане як команда, що ігнорується.

## Стан проєкту

Це робочий прототип. HID-ідентифікатори та бітову маску кнопок перевірено на TX12. Повний наскрізний тест керування YouTube через AppleScript/Chrome ще потрібно виконати на цільовому Mac.

## Структура

```text
.
├── src/
│   ├── tx12_youtube.py
│   ├── tx12_buttons.py
│   ├── tx12_hid_test.py
│   ├── tx12_read.py
│   └── tx12_test.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── HARDWARE.md
│   ├── INSTALLATION.md
│   └── TROUBLESHOOTING.md
├── requirements.txt
└── .gitignore
```

## Швидкий запуск

1. Підключіть TX12 до Mac через USB.
2. Встановіть Python 3 та залежності:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Надайте Terminal/iTerm дозвіл на керування Google Chrome, якщо macOS запитає.
4. У Chrome увімкніть **View → Developer → Allow JavaScript from Apple Events**.
5. Відкрийте вкладку YouTube та запустіть:
   ```bash
   python src/tx12_youtube.py
   ```

Детальні інструкції: [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Перевірка TX12

Перед запуском основної програми можна перевірити пристрій та кнопки:

```bash
python src/tx12_hid_test.py
python src/tx12_buttons.py
```

Інші діагностичні скрипти описані в [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Важливо

- Програма шукає відкриту вкладку, URL якої містить `youtube.com`, у вікнах Google Chrome.
- Підтримується саме Google Chrome з дозволеним JavaScript через Apple Events; інші браузери не реалізовані.
- Програма читає HID-звіти TX12 напряму через `hidapi`.
- Віртуальне середовище `.venv/` та встановлені бінарні залежності не зберігаються в Git.
