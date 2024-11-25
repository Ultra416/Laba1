def remove_duplicates(input_list):
    # Забераєм однакові дані
    return list(set(input_list))

def sort_mixed_list(input_list):
    # Розділяємо числа та рядки
    numbers = sorted([x for x in input_list if isinstance(x, (int, float))])
    strings = sorted([x for x in input_list if isinstance(x, str)])
    
    # Об'єднуємо числа і рядки
    return numbers + strings

mylist = [1, 2, 3, 4, 5, 6, 3, 4, 5, 7, 6, 5, 4, 3, 4, 5, 4, 3, 'Привіт', 'анаконда']

clened_list = remove_duplicates(mylist) # Виклик списка без повторів
sorted_list = sort_mixed_list(clened_list) # Виклик відсортованого списка без повторів

print(clened_list)
print(sorted_list)
