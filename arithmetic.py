from math import log10

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

    def plus(self, other: 'Digit'):
        s = self.d + other.d
        self.d = s % self.M
        return Digit(self.M, s // self.M)

        
    def minus(self, other: 'Digit'):
        s = self.d - other.d
        self.d = s % self.M
        return Digit(self.M, -(s // self.M))
    

class Number:
    def __init__(self, M: int = 10, N: int = 1, digits: list = [Digit], negative: bool = False):
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

    def __getitem__(self, key: int):
        return self.digits[key]

    def __setitem__(self, key: int, value: Digit):
        self.digits[key] = value
    
    def __lt__(self, other: 'Number'):
        for i in range(self.N):
            if self[i] < other[i]: return True
            if self[i] > other[i]: return False
        return False

    def __neg__(self):
        negative_number = Number(self.M, self.N, self.digits, not self.negative)
        return negative_number
    
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

        # if remainder_current:
        #     print(f"remainder = {remainder_current}, number = {new_number}")
        #     return -(self.get_border_num(True) - new_number)
        
        return new_number


if __name__ == "__main__":
    n1 = Number(10, 2, [Digit(10, 0), Digit(10, 1)], False)
    n2 = Number(10, 2, [Digit(10, 1), Digit(10, 0)], False)
    n3 = n1 - n2
    print(n1)
    print(n2)
    print(n3)

    d1 = Digit(10, 5)
    d2 = Digit(10, 8)
    d3 = d1.minus(d2)
    print(d3, d1)

    for i1 in range(5, 10):
        for j1 in range(0, 10):
            n1 = Number(10, 2, [Digit(10, i1), Digit(10, j1)], False)
            for i2 in range(5, 10):
                for j2 in range(0, 10):
                    n2 = Number(10, 2, [Digit(10, i2), Digit(10, j2)], False)
                    print(f"{n1} + {n2} = {n1 + n2}")



