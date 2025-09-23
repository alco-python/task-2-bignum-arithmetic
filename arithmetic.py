from math import floor

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
        out = ("-" if self.negative else "") + ".".join([str(i.d) for i in self.digits])
        return out


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
    
    def __rshift__(self, shift: int):
        new_number = Number(self.M, self.N, self.digits)
        for i in range(shift):
            new_number.digits.pop(-1)
            new_number.digits.insert(0, Digit(self.M))
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
            return -(self.get_border_num(False) - new_number)
            
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
            return new_number
            for i in range(other.d):
                new_number += self
            return new_number
                
        
        elif isinstance(other, Number):
            new_number = Number(self.M, max(self.N, other.N))
            c = 0
            component = Number(self.M, self.N)
            for i in range(other.N - 1, -1, -1):
                component = ((self * other[i]) << c)
                new_number = new_number + (component if component.negative else component)
                c += 1
                # print(component)
            return -new_number if self.negative else new_number




def f_alt(n: int) -> str:
    m = (n - 7682) // 334
    q, r = divmod(m, 6)
    base = [-314, 20, 354, 688, -977, -643]
    v = base[r] + 5 * q
    print(v)
    return f"{'-' if v < 0 else ''}{abs(v):03d}"


if __name__ == "__main__":

    c = 4
    # for k in range(0, 2):
    #     for c in range(0, 10):
    #         n1 = Number(10, 3, [Digit(10, 3), Digit(10, 1), Digit(10, 7)], False)
    #         n2 = Number(10, 2, [Digit(10, k), Digit(10, c)], False)
    #         d1 = Digit(10, 4)
    #         print(f"{n1} * {n2} = {n1 * n2}")
    #         n3 = Number(10, 3)
    #         for i in range(k * 10 + c):
    #             n3 = n3 + n1
    #         print(f"\t      {n3}")
    n1 = Number(10, 3, [Digit(10, 3), Digit(10, 3), Digit(10, 4)], False)
    n2 = Number(10, 3, [Digit(10, 0), Digit(10, 0), Digit(10, 4)], False)
    d1 = Digit(10, c)
    print(f"{n1} * {n2} = {n1 * n2}")
    print(f"{n1} * {d1} = {n1 * d1}")
    print(~n1)

    
    for i in range(3):
        for j in range(10):
            n2 = Number(n1.M, n1.N, [Digit(n1.M, i), Digit(n1.M, j)])
            n3 = n1 * n2
            print(f"{n1} * {n2} = {n3}", end = ' ')
            # print(f"{334 * (i*10 + j)} -> {str(n3).replace('.', '')} -> {f_alt(334 * (i*10 + j))}")
            n3 = Number(n1.M, n1.N)
            for k in range(i * 10 + j):
                n3 = n3 + n1
            print(f"({n3})\n")

    print("-"*64)

    n1 = Number(10, 3, [Digit(10, 3), Digit(10, 3), Digit(10, 4)], False)
    n2 = Number(10, 3, [Digit(10, 0), Digit(10, 0), Digit(10, 4)], False)
    print(f"{n1} + {n2} = {n1 + n2}")



