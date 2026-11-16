# Встановлення та запуск на macOS

## Вимоги

- macOS;
- Python 3;
- RadioMaster TX12 у режимі USB HID;
- Google Chrome;
- Terminal або iTerm із дозволом керувати Google Chrome.

## 1. Отримати проєкт

Клонуйте репозиторій та перейдіть у його каталог:

```bash
git clone https://github.com/vstrk1/Yeke-Yeke.git
cd Yeke-Yeke
```

## 2. Створити середовище Python

Не копіюйте стару папку `tx12-venv` з іншого Mac. Віртуальне середовище містить платформозалежні бінарні файли. Створіть нове:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Якщо потрібна лише основна програма, достатньо встановити HID-залежність:

```bash
pip install hidapi
```

## 3. Дозволити JavaScript у Chrome

У Google Chrome відкрийте:

**View → Developer → Allow JavaScript from Apple Events**

У різних версіях Chrome назви пунктів меню можуть трохи відрізнятися.

## 4. Дозволи macOS

Під час першого запуску macOS може попросити дозволити Terminal або iTerm керувати Google Chrome. Дозвольте доступ у системному діалозі. Якщо запит не з'являється, перевірте **System Settings → Privacy & Security → Automation**.

## 5. Перевірити TX12

```bash
python src/tx12_hid_test.py
python src/tx12_buttons.py
```

У другій команді натисніть і відпустіть A та D. Очікувані значення першого байта: `01` для A, `02` для D, `03` для обох.

## 6. Запустити контролер

Відкрийте вкладку YouTube у Google Chrome і виконайте:

```bash
python src/tx12_youtube.py
```

Зупинка: `Ctrl+C`.

## Керування

- коротке A — попереднє відео;
- утримання A — перемотування назад;
- коротке D — наступне відео;
- утримання D — перемотування вперед.

Параметри часу та кроку перемотування налаштовуються на початку `src/tx12_youtube.py`.
