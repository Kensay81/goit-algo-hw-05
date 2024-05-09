import timeit
import requests

# Завантаження текстових файлів
url1 = 'https://drive.google.com/file/d/18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh/view?usp=sharing'
response = requests.get(url1)

if response.status_code == 200:
    content1 = response.content.decode('utf-8')  # отримуємо вміст файлу
else:
    print("Помилка завантаження файлу:", response.status_code)

url2 = 'https://drive.google.com/file/d/13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ/view?usp=sharing'
response = requests.get(url2)

if response.status_code == 200:
    content2 = response.content.decode('utf-8')  # отримуємо вміст файлу
else:
    print("Помилка завантаження файлу:", response.status_code)

""" with open('https://drive.google.com/file/d/18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh/view?usp=sharing', 'r') as file:
    text1 = file.read()

with open('https://drive.google.com/file/d/13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ/view?usp=sharing', 'r') as file:
    text2 = file.read()
 """
# Функція для пошуку підрядка за допомогою алгоритму Боєра-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

""" text = "Being a developer is not easy"
pattern = "developer"

position = boyer_moore_search(text, pattern)
if position != -1:
    print(f"Substring found at index {position}")
else:
    print("Substring not found")
    """

# Функція для пошуку підрядка за допомогою алгоритму Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

""" raw = "Цей алгоритм часто використовується в текстових редакторах та системах пошуку для ефективного знаходження підрядка в тексті."

pattern = "алг"

print(kmp_search(raw, pattern)) """


# Функція для пошуку підрядка за допомогою алгоритму Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

""" main_string = "Being a developer is not easy"
substring = "developer"

position = rabin_karp_search(main_string, substring)
if position != -1:
    print(f"Substring found at index {position}")
else:
    print("Substring not found")
 """

# Функція для вимірювання часу виконання алгоритму для одного підрядка
def measure_time_for_one_pattern(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=10)

# Функція для вимірювання часу виконання алгоритму для вигаданого підрядка
def measure_time_for_fake_pattern(algorithm, text):
    pattern = "вигаданий_підрядок"  # ваш вигаданий підрядок
    return timeit.timeit(lambda: algorithm(text, pattern), number=10)

# Пошук підрядка, який існує в тексті, та вимірювання часу виконання
pattern1 = "дві монети по 10 копійок." # паттерн для першого текста
pattern2 = "Розгорнутий зв’язний список (unrolled list)" # паттерн для другого текста

print("Для тексту 1:")
print("Боєра-Мура:", measure_time_for_one_pattern(boyer_moore_search, content1, pattern1))
print("Кнута-Морріса-Пратта:", measure_time_for_one_pattern(kmp_search, content1, pattern1))
print("Рабіна-Карпа:", measure_time_for_one_pattern(rabin_karp_search, content1, pattern1))

print("\nДля тексту 2:")
print("Боєра-Мура:", measure_time_for_one_pattern(boyer_moore_search, content2, pattern2))
print("Кнута-Морріса-Пратта:", measure_time_for_one_pattern(kmp_search, content2, pattern2))
print("Рабіна-Карпа:", measure_time_for_one_pattern(rabin_karp_search, content2, pattern2))

# Пошук вигаданого підрядка та вимірювання часу виконання
print("\nДля вигаданого підрядка:")
print("Боєра-Мура:", measure_time_for_fake_pattern(boyer_moore_search, content2))
print("Кнута-Морріса-Пратта:", measure_time_for_fake_pattern(kmp_search, content2))
print("Рабіна-Карпа:", measure_time_for_fake_pattern(rabin_karp_search, content2))

