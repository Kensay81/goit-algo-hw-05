def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0
 
    while low <= high:
 
        mid = (high + low) // 2
        iterations += 1
 
        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1
 
        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1
 
        # інакше x присутній на позиції і повертаємо його
        else:
            return (iterations, mid)
 
    # якщо елемент не знайдений
    return -1

arr = [0.2, 0.3, 0.4, 1.0, 4.0]
x = 1.0
iterations, mid = binary_search(arr, x)
if iterations != -1:
    print(f"Element is present at index {mid} , number of iterations was {iterations}")
else:
    print("Element is not present in array")
