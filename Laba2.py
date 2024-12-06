name = "Bober"
last_name = "Naber"
age = 23
Hello_World = "hello world"

print(name,type(name))
print(last_name,type(last_name))
print(age,type(age))
print(Hello_World,type(Hello_World))

count_int = 0 # лічильники типів
count_str = 0
count_bool = 0
count_set = 0
count_list = 0
count_tuple = 0
count_float = 0
lst_notnull = []
max_value = -1
lst_count_types = [count_set, count_bool, count_tuple, count_list, count_float, count_str, count_int] # список лічильників
lst_name_type = [set, tuple, list, bool, float, str, int] # список назв
lst = [name, lastname, age]
for item in lst: # цикл що рахує кількість типів
    if type(item) == int:
        print(lst_count_types[-1])
        lst_count_types[-1] += 1
    elif type(item) == str:
        lst_count_types[-2] += 1
    elif type(item) == float:
        lst_count_types[-3] += 1

for item in lst_count_types: # цикл що перевіряє чи не є значення нульвим
    if item != 0:
        lst_notnull.append(item) # метод списку, який додає новий елемент у кінець списку
    if len(lst_notnull) == 0:
        print('Good')
    else:
        if item == max_value:
            print('Not')
            break # якщо значення item дорівнює макс.значення то виведе not

        elif item > max_value:
            max_value = item # код виконує перевірку іtem, якщо вона проходить, оновлює значення змінної max_value

inndex = lst_count_types.index(max_value) #в зміну заганяємо індекс максимального значення

print(lst_name_type[inndex]) # виводимо значення елемента з індексом або ключем inn із колекції lst_name_type

for item in lst:
    if type(item) != lst_name_type[inndex]:
        lst.remove(item)
