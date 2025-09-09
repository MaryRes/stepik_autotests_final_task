# Stepik Autotests - Final Task

Проект автоматизированного тестирования интернет-магазина с использованием Page Object Model (POM). Включает комплексные тесты функциональности корзины покупок для авторизованных и гостевых пользователей.

## 🚀 Основные возможности

- **Тестирование корзины покупок** для различных сценариев пользователей
- **Многоязычная поддержка** (en, ru, fr, es и другие)
- **Кросс-браузерное тестирование** (Chrome, Firefox)
- **Профессиональная архитектура** Page Object Model
- **Комплексные проверки** сообщений и состояний корзины
- **Headless-режим** для CI/CD и быстрого выполнения
- **Автоматическая регистрация** пользователей для тестирования

## 📁 Структура проекта

```text
./
  ├── CHANGELOG.md
  ├── conftest.py
  ├── pyproject.toml
  ├── pytest.ini
  ├── README.md
  ├── requirements.txt
  ├── test_login_page.py
  ├── test_main_page.py
  ├── test_product_page.py
  ├── urls.py
  ├── __init__.py
  └── pages/
    ├── base_page.py
    ├── basket_page.py
    ├── locators.py
    ├── login_page.py
    ├── main_page.py
    ├── product_page.py
  └── utils/
    ├── generate_structure.py
    ├── __init__.py
```

## ⚙️ Установка зависимостей

1. **Клонируйте репозиторий (ветка review):**
```bash
git clone -b review https://github.com/MaryRes/stepik_autotests_final_task.git
cd stepik_autotests_final_task
```

2. **Или если уже клонировали main ветку, переключитесь на review:**
```bash
git checkout review
git pull origin review
```

3. Создайте виртуальное окружение (рекомендуется):
```bash
python -m venv venv
```
4. Активируйте виртуальное окружение:
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
5. Установите зависимости:
```bash
pip install -r requirements.txt
```
## 🧪 Запуск тестов

### 🔥 Минимальный пакет тестов для ревью
```bash
pytest -v --tb=line --language=en -m need_review
```

### Базовый запуск (Chrome, английский язык)
```bash
pytest -v
```

### Запуск в headless-режиме (без графического интерфейса)
```bash
# Chrome headless
pytest --headless --language=en -v

# Firefox headless  
pytest --headless --browser_name=firefox --language=en -v
```

### 💡 Преимущества headless-режима:

- **🚀 Быстрее выполнение** - нет рендеринга UI
- **🎯 Стабильнее** - меньше зависимость от графической среды  
- **🏗️ Для CI/CD** - идеально для автоматических пайплайнов
- **📊 Экономия ресурсов** - меньше потребление памяти и CPU

### С выбором языка
```bash
# Spanish
pytest --language=es -v
# French
pytest --language=fr -v  
# Russian
pytest --language=ru -v
```

### С выбором браузера
```bash
# Firefox
pytest --browser_name=firefox --language=es -v
# Chrome (по умолчанию)
pytest --browser_name=chrome --language=es -v
```

### Комбинированные опции
```bash
# Firefox + headless + русский язык
pytest --browser_name=firefox --headless --language=ru -v

# Chrome + headless + французский язык + только важные тесты
pytest --headless --language=fr -m need_review -v
```

### Конкретные тестовые сценарии
```bash
# Только тесты продукта
pytest tests/test_product_page.py -v

# Тесты с маркером need_review
pytest -m need_review -v

# Тесты для гостевых пользователей
pytest -m "login_guest" -v
```

### 🛠️ Пример для CI/CD:
```bash
pytest --headless --tb=line --language=en -m need_review -v
```

## 🎯 Ключевые тестовые сценарии

### 1. Тестирование корзины для гостевых пользователей
- Добавление товара в корзину
- Проверка сообщений об успехе
- Валидация цен и названий товаров

### 2. Тестирование корзины для авторизованных пользователей  
- Автоматическая регистрация пользователя
- Проверка отсутствия сообщений до добавления товара
- Комплексное тестирование процесса покупки

### 3. Навигационные тесты
- Переход на страницу логина
- Доступность ссылок навигации
- Работа с корзиной из разных разделов

## ⚠️ Известные проблемы

Некоторые промо-страницы (например, offer7) имеют известные баги и помечены как `xfail`. Тесты для этих страниц ожидаемо падают.

## 📊 Маркеры тестов

- `@need_review` - основные тесты для проверки ревьюером
- `@new` - новые тесты в разработке  
- `@xfail` - тесты с ожидаемыми падениями (известные баги)
- `@login_guest` - тесты для гостевых пользователей

## 🛠️ Технологический стек

- **Python 3.8+**
- **Pytest** - тестовый фреймворк
- **Selenium WebDriver** - автоматизация браузера
- **Page Object Model** - архитектура тестов
- **WebDriver Manager** - автоматическое управление драйверами
- **GitHub Actions** - CI/CD (опционально)

## 📞 Поддержка

Для вопросов и предложений создавайте issue в репозитории проекта.

---

*Проект разработан в рамках финального задания Stepik по автоматизированному тестированию*