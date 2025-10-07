class Digit:
    def __init__(self, M: int = 0, value: int = 0):
        self.M = M
        if value >= M:
            self.d = 0
            print(f"Out of M ({M}) by value ({value})")
        self.d = value
    

    def __str__(self):
        return str(self.d)
    

    def __bool__(self):
        return bool(self.d)
    

    def __lt__(self, other: 'Digit'):
        return self.d < other.d


    def __gt__(self, other: 'Digit'):
        return self.d > other.d
    

    def __invert__(self):
        return Digit(self.M, self.M - 1 - self.d)


    def plus(self, other: 'Digit'):
        s = self.d + other.d
        self.d = s % self.M
        return Digit(self.M, s // self.M)


    def minus(self, other: 'Digit'):
        s = self.d - other.d
        self.d = s % self.M
        return Digit(self.M, -(s // self.M))
    

    def multiply(self, other: 'Digit'):
        s = self.d * other.d
        self.d = s % self.M
        return Digit(self.M, s // self.M)
    

class Number:
    def __init__(self, M: int = 10, N: int = 1, digits: list[Digit] = [], negative: bool = False):
        self.M = M
        self.N = N
        self.negative = negative if digits else False
        self.set_value(digits)


    def set_value(self, new_digits: list[Digit]):
        self.digits = [Digit(self.M) for i in range(self.N - len(new_digits))] + [Digit(self.M, i.d) for i in new_digits]
        return self
    

    def get_border_num(self, negative = False):
        return Number(self.M, self.N, [Digit(self.M, self.M - 1) for i in range(self.N)], negative)
    
    
    def __str__(self):
        out = ("-" if self.negative else "")
        flag = True
        for i in range(self.N):
            if self[i].d != 0:
                flag = False
                out += ".".join([str(j.d) for j in self.digits[i:]])
                break
        if flag:
            return "0"
            
        return out
    

    def __bool__(self):
        for i in self.digits:
            if i.d != 0:
                return True
        return False


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.digits[key]
        elif isinstance(key, slice):
            new_digits = []
            step_counter = 0
            step = key.step if key.step else 1
            for i in range(self.N - 1, -1, -1):
                if i >= key.start and i < key.stop:
                    if step_counter == 0:
                        new_digits.insert(0, self.digits[i])
                    else:
                        new_digits.insert(0, Digit(10))
                    step_counter += 1
                    step_counter %= step
                else:
                    new_digits.insert(0, Digit(10))

            new_number = Number(self.M, self.N, new_digits)
            return new_number

    def __setitem__(self, key: int, value: Digit):
        self.digits[key] = value
    
    
    def __lt__(self, other: 'Number'):
        for i in range(self.N):
            if self[i] < other[i]: return True
            if self[i] > other[i]: return False
        return False
    

    def __lshift__(self, shift: int):
        new_number = Number(self.M, self.N, self.digits, self.negative)
        for i in range(shift):
            new_number = (new_number * Digit(new_number.M, new_number.M - 1)) + new_number
        return new_number
        
        
    def __neg__(self):
        flag = False
        for i in range(self.N - 1, -1, -1):
            if self[i].d != 0:
                flag = True
                break
        negative_number = Number(self.M, self.N, self.digits, ((not self.negative) if flag else self.negative))
        return negative_number
    

    def __invert__(self):
        new_number = Number(self.M, self.N, [~d for d in self.digits], self.negative)
        return new_number
    

    def __add__(self, other: 'Number'):
        global overflow_flag
        if self.M != other.M:
            print(f"M({self.M}) of first number != M({other.M}) of second number")
            return self
        
        if self.negative:
            if other.negative: return -(-self + -other)
            else: return other - -self
        else:
            if other.negative: return self - -other
        
        new_number = Number(self.M, self.N, self.digits)

        remainder_current = Digit(self.M)
        remainder_prev = Digit(self.M)
        for i in range(new_number.N - 1, -1, -1):
            remainder_prev = remainder_current

            remainder_current = new_number[i].plus(other[i])
            remainder_current.plus(new_number[i].plus(remainder_prev))
        
        if remainder_current:
            if overflow_flag:
                return -(self.get_border_num() - new_number)
            print("\nПри выполнении операции случилось переполнение!")
            return Number(self.M, self.N)
        return new_number
    

    def __sub__(self, other: 'Number'):
        if self.M != other.M:
            print(f"M({self.M}) of first number != M({other.M}) of second number")
            return self
        
        if self < other:
            return -(other - self)
        
        if self.negative:
            if other.negative: return -other - -self
            else: return -(-self + other)
        else:
            if other.negative: return self + -other
        
        new_number = Number(self.M, self.N, self.digits)

        remainder_current = Digit(self.M)
        remainder_prev = Digit(self.M)
        for i in range(new_number.N - 1, -1, -1):
            remainder_prev = remainder_current

            remainder_current = new_number[i].minus(other[i])
            remainder_current.plus(new_number[i].minus(remainder_prev))
        return new_number
    

    def __mul__(self, other):
        if isinstance(other, Digit):
            new_number = Number(self.M, self.N)

            if not overflow_flag:
                remainder_current = Digit(self.M)
                remainder_prev = Digit(self.M)

                for i in range(new_number.N - 1, -1, -1):
                    remainder_prev = remainder_current
                    new_number[i].plus(self[i])
                    remainder_current = new_number[i].multiply(other)
                    remainder_current.plus(new_number[i].plus(remainder_prev))
                
                # print(f"\tremainder = {remainder_current.d % 2}")
                new_number = -new_number if self.negative else new_number

                if remainder_current.d % 2:
                    return -~new_number
                
            else:
                for i in range(other.d):
                    new_number += self
            
            return new_number
        
        elif isinstance(other, Number):
            new_number = Number(self.M, max(self.N, other.N))
            c = 0
            component = Number(self.M, self.N)
            for i in range(other.N - 1, -1, -1):
                component = ((self * other[i]) << c)
                new_number = new_number + component
                c += 1
                # print(component)
            return -new_number if self.negative else new_number
    
    
    def __floordiv__(self, other: 'Number'):
        if not other:
            print("Деление на ноль не доступно!")
            return(Number(self.M, self.N))
        self_copy = Number(self.M, self.N + 1, self.digits)
        res = Number(self.M, self.N)
        while True:
            other_copy = Number(other.M, self.N + 1, other.digits)
            if self_copy < other_copy:
                if self.negative:
                    res = res + Number(res.M, res.N, [Digit(self.M, 1)])
                    if not other.negative:
                        res.negative = True
                else:
                    if other.negative:
                        res.negative = True
                return res
            
            coef = 0
            while other_copy << 1 < self_copy:
                other_copy = other_copy << 1
                coef += 1
            for i in range(self.M):
                self_copy = self_copy - other_copy
                if self_copy.negative:
                    self_copy = self_copy + other_copy
                    break
                res = res + (Number(self.M, self.N, [Digit(self.M, 1)]) << coef)


def string_to_number(s: str):
    global M, N
    negative = False
    digits = []
    flag_M = False
    flag_N = False
    c = 0
    current_i = ""
    if s.startswith("-"):
        s = s[1:]
        negative = True
    for i in s.replace(" ", "").split("."):
        current_i = i
        if i.isdigit():
            d = int(i)
            if d < M:
                digits.append(Digit(M, d))
                c += 1
                if c > N:
                    flag_N = True
                    break
            else:
                flag_M = True
                break
        else:
            flag_M = True
            break
    if flag_M:
        print(f"""Ошибка. "{current_i}" не является цифрой данной системы счисления. Попробуйте ещё раз.""")
        return None
    if flag_N:
        print(f"""Ошибка. Число вышло за пределы разрядной сетки. Попробуйте ещё раз.""")
        return None
    return Number(M, N, digits, negative)


def harv_input(text: str, min: int, max: int):
    while True:
        user_input = input(text)
        if user_input.isdigit() and int(user_input) in range(min, max + 1):
            return int(user_input)
        else:
            print("\n\nНеправильный ввод. Попробуйте ещё раз.")


def expression(s: str):
    s = s.replace("//", "/")
    numbers = []
    for i in s.translate(str.maketrans("+-*/", ",,,,")).replace(" ", "").split(","):
        number = string_to_number(i)
        if number != None:
            numbers.append(number)
        else:
            print_menu(13)
            return
    signs = [""]
    for i in s:
        if i in "+-*/":
            signs.append(i if i != "/" else "//")
    result_str = ""
    for i in range(len(signs)):
        result_str += signs[i] + f"numbers[{i}]"
    print(f"Результат: {eval(result_str)}")
    print_menu(0)


def print_menu(i: int, action: int = 0):
    global M, N, overflow_flag, number1, number2
    user_input = ""
    match i:
        case 0:
            menu = f"""
Настройки программы:
    1. Основание системы счисления: {M};
    2. Максимальная разрядность: {N};
    3. Циклический перенос при переполнении: {"включён" if overflow_flag else "выключен"};
Меню действий:
    4. Сложение (+) двух чисел;
    5. Вычитание (-) двух чисел;
    6. Умножение (*) двух чисел;
    7. Целочисленное деление (//) двух чисел;
    8. Вычисление выражения;
    9. Выход;

Для изменения настроек или выполнения действий введите соответствующий номер: """
            print_menu(harv_input(menu, 1, 9))
            
        case 1:
            menu = """
Введите новое основание системы счисления (1 < M < 32769): """
            M = harv_input(menu, 2, 32768)
            print_menu(0)

        case 2:
            menu = """
Введите новую максимальную разрядность (0 < N < 1000): """
            N = harv_input(menu, 1, 999)
            print_menu(0)

        case 3:
            menu = """
Включить циклический перенос при переполнении (0 - Нет, 1 - Да): """
            overflow_flag = harv_input(menu, 0, 1)
            print_menu(0)

        case 4 | 5 | 6 | 7:
            menu = f"""
При вводе чисел разделяйте разряды с помощью '.', например -1728 -> -1.7.2.8

Введите первое число({number_names[i - 4][0]}): """
            number1 = string_to_number(input(menu))
            if not number1:
                print_menu(i)
            else:
                print_menu(i + 6, i)
        
        case 8:
            menu = """
Введите выражение, состоящее только из чисел и знаков +, -, *, //: 
"""
            expression(input(menu))
        
        case 9:
            print(f"{'-'*10} Выход из программы {'-'*10}")

        case 10 | 11 | 12 | 13:
            menu = f"""
Введите второе число({number_names[i - 10][1]}): """
            number2 = string_to_number(input(menu))
            if number2 == None:
                print_menu(i)
            else:
                print_menu(14, action)

        case 14:
            menu = f"""
Результат ({result_names[action - 4]}): {eval("number1 " + actions[action - 4] + " number2")}"""
            print(menu)
            print_menu(0)
        

number_names = [
    [
        "Слагаемое",
        "Слагаемое"
    ],
    [
        "Уменьшаемое",
        "Вычитаемое"
    ],
    [
        "Множитель",
        "Множитель"
    ],
    [
        "Делимое",
        "Делитель"
    ]
]

result_names = [
    "Сумма",
    "Разность",
    "Произведение",
    "Частное"
]

actions = ["+", "-", "*", "//"]

if __name__ == "__main__":
    M = 10
    N = 5
    overflow_flag = False
    number1 = Number(M, N)
    number2 = Number(M, N)
    
    print(f"{'-'*10} Программа для работы с длинной арифметикой {'-'*10}")
    print_menu(0)
        



