from math import log10

class Digit:
    def __init__(self, M = 0, value = 0):
        self.M = M
        if value >= M:
            self.d = 0
            print(f"Out of M ({M}) by value ({value})")
        self.d = value
    
    def copy(self, other):
        self.M = other.M
        self.d = other.d

    def plus(self, other):
        s = self.d + other.d
        self.d = s % self.M
        return Digit(self.M, s // self.M)

        
    def minus(self, other):
        s = self.d - other.d
        self.d = s % self.M
        return Digit(self.M, s // self.M)
    

class Number:
    def __init__(self, M = 10, N = 0):
        self.M = M
        self.N = N
        self.digits = [Digit(self.M) for i in range(self.N)]
        # print(self.digits)

    def set_value(self, new_digits):
        self.digits = [Digit(self.M) for i in range(self.N - len(new_digits))] + new_digits
        return self
    
    def to_string(self):
        out = ".".join([str(i.d) for i in self.digits])
        return out

    def __getitem__(self, key):
        return self.digits[key]

    def __setitem__(self, key, value):
        self.digits[key] = value
    
    def __add__(self, other):
        if self.M != other.M:
            print("M of first number != M of second number")
            return self
        
        new_number = Number(self.M, self.N).set_value(self.digits)

        remainder_current = Digit(self.M)
        remainder_prev = Digit(self.M)
        for i in range(new_number.N - 1, -1, -1):
            remainder_prev = remainder_current

            remainder_current = new_number[i].plus(other[i])
            remainder_current.plus(new_number[i].plus(remainder_prev))
        return new_number


if __name__ == "__main__":
    n1 = Number(10, 10).set_value([Digit(10, 1), Digit(10, 5)])
    n2 = Number(10, 10).set_value([Digit(10, 2), Digit(10, 6)])
    n3 = n1 + n2
    print(n3.to_string())
        




