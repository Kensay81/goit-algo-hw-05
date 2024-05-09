def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0
    element_found = False
 
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
            element_found = True
            return (element_found, iterations, mid, arr[mid])
 
    # якщо елемент не знайдений
    if (arr[mid] - arr[mid-1]) > (arr[mid+1] - arr[mid]):
        nearest_element = arr[mid+1]
        nearest_element_index = mid+1
    elif (arr[mid] - arr[mid-1]) < (arr[mid+1] - arr[mid]):
        nearest_element = arr[mid-1]
        nearest_element_index = mid-1
    else:
        nearest_element = (arr[mid-1], arr[mid+1])
        nearest_element_index = (mid-1, mid+1) 

    return (element_found, iterations, nearest_element_index, nearest_element)

arr = [0.2, 0.3, 0.4, 1.0, 4.0]
x = 0.35
element_found, iterations, mid, element = binary_search(arr, x)
if element_found:
    print(f"Element {element} is present at index {mid} , number of iterations was {iterations}")
else:
    print(f"Element is not present in array, nearest element index is {mid}, value is {element}, number of iterations was {iterations}")

