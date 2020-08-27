# TODO: figure out sub,rsub,add, radd and return NotImplemented properaly
# TODO: do a method for -Degree
# TODO: make a simpler way to cast int/float to Degree other then Degree.value[0] = int
# TODO: make switch more sense
# TODO: make switch for more than 1 var
# TODO: be careful of types Angle,Int,Float and Degree in switch


class Degree:

    nextVarIdx = 1

    def __init__(self, newvar=True):
        """if (newvar == False) self.value is empty"""
        self.value = {}
        if newvar:
            self.value[Degree.nextVarIdx] = 1
            Degree.nextVarIdx += 1

    def copy(self):
        res = Degree(False)
        for i, j in self.value.items():
            res.value[i] = j
        return res

    def switch(self, key, switchdeg):
        if key not in self.value:
            return
        else:
            times = self.value[key]
            del self.value[key]
            self += switchdeg * times

    def clean_zeros(self):
        for key in [key for key in self.value if self.value[key] == 0]:
            del self.value[key]

    def __add__(self, other):
        """Add the values for the same key and add the missing keys with dict/Degree/int/float"""
        res = Degree(False)
        for i, j in self.value.items():
            res.value[i] = j
        if isinstance(other, Degree):
            for idx, val in other.value.items():
                if idx in res.value:
                    res.value[idx] += val
                else:
                    res.value[idx] = val
        elif isinstance(other, dict):
            for idx, val in other.items():
                if idx in res.value:
                    res.value[idx] += val
                else:
                    res.value[idx] = val
        elif isinstance(other, (int, float)):
            if 0 not in res.value:
                res.value[0] = 0
            res.value[0] += other
        else:
            return NotImplemented

        res.clean_zeros()
        return res

    def __iadd__(self, other):
        if isinstance(other, Degree):
            for idx, val in other.value.items():
                if idx in self.value:
                    self.value[idx] += val
                else:
                    self.value[idx] = val
        elif isinstance(other, dict):
            for idx, val in other.items():
                if idx in self.value:
                    self.value[idx] += val
                else:
                    self.value[idx] = val
        elif isinstance(other, (int, float)):
            if 0 not in self.value:
                self.value[0] = 0
            self.value[0] += other
        else:
            return NotImplemented
        self.clean_zeros()

    def __sub__(self, other):
        """Call add for the negtive other of type dict/Degree/int/float"""
        minus_other = Degree(False)
        if isinstance(other, Degree):
            for i, j in other.value.items():
                minus_other.value[i] = -j
            return self + minus_other
        elif isinstance(other, dict):
            for i, j in other.items():
                minus_other.value[i] = -j
            return self + minus_other
        elif isinstance(other, (int, float)):
            minus_other.value[0] = -other
            return self + minus_other
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            minus_self = Degree(False)
            for i, j in self.value.items():
                minus_self.value[i] = -j
            return minus_self + other
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = self.copy()
            for i in res.value.keys():
                res.value[i] *= other
            return res
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self * (1 / other)
        return NotImplemented

    def __str__(self):
        """Returns a greek letter or A{idx} polynomial"""
        GA = "\u03B1\u03B2\u03B3\u03B4\u03B5\u03B6\u03B7\u03B8\u03B9\u03Ba\u03Bb\u03Bc\u03Bd\u03Be\u03Bf\u03C0\u03C1\u03C2\u03C3\u03C4\u03C5\u03C6\u03C7\u03C8\u03C9"
        res = ""
        for idx, val in sorted(self.value.items()):
            str_var = ""
            if idx == 0:
                pass
            elif 0 <= idx - 1 < len(GA):
                str_var = GA[idx - 1]
            else:
                str_var = f"A{idx-1}"
            if val == 0:
                continue
            else:
                if res != "":
                    res += " +" if val > 0 else " -"
                res += str(abs(val)) + str_var
        return res

    def __lt__(self, other):
        """Do lexicographic compare between the objects' sorted keys"""
        if other is None:
            raise TypeError("NoneType compared to Degree")
        return sorted(list(self.value.keys())) < sorted(list(other.value.keys()))

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            if other == 0 and len(self.value) == 0:
                return True
            return len(self.value) == 1 and 0 in self.value and self.value[0] == other
        elif isinstance(other, (Degree, dict)):
            return self - other == 0
        else:
            return NotImplemented


"""
print(Degree.nextVarIdx)
alpha = Degree(True)
print(Degree.nextVarIdx)
print(alpha)
alpha += {0:180,1:0.5,2:-3}
print(Degree.nextVarIdx)
print(alpha)

"""
