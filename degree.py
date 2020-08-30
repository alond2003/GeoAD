from functools import total_ordering


@total_ordering
class Degree:

    nextVarIdx = 1

    def __init__(self, newvar=True, d={}):
        """Create Degree object based on dict,int,float or empty (w/ or w/o newvar)"""
        if isinstance(d, dict):
            self.value = dict(d)
        elif isinstance(d, (int, float)):
            self.value = {0: d}
        else:
            raise TypeError(f"d as a {type(d)} is not supported")
        if newvar:
            self.value[Degree.nextVarIdx] = 1
            Degree.nextVarIdx += 1
        self.clean()

    def new_copy(self):
        """Return a new_copy of this object"""
        res = Degree(False)
        for i, j in self.value.items():
            res.value[i] = j
        return res

    def copy(self, other):
        """Copy other dict to this object"""
        del self.value
        self.value = {}
        for i, j in other.value.items():
            self.value[i] = j
        self.clean()

    def switch(self, key, switchdeg):
        """switch every instance of this key to swithdeg"""
        if key not in self.value:
            return
        else:
            times = self.value[key]
            del self.value[key]
            self += switchdeg * times
            self.clean()

    def clean(self):
        """clean keys that have a zero value or float to int"""
        for key in [key for key in self.value if self.value[key] == 0]:
            del self.value[key]
        for key in self.value:
            if isinstance(self.value[key], float) and self.value[key].is_integer():
                self.value[key] = int(self.value[key])

    def __add__(self, other):
        """Add the values for the same key and add the missing keys with dict/Degree/int/float"""
        res = self.new_copy()
        if isinstance(other, Degree):
            for idx, val in other.value.items():
                if idx in res.value:
                    res.value[idx] += val
                else:
                    res.value[idx] = val
        elif isinstance(other, (dict, int, float)):
            return self + Degree(newvar=False, d=other)
        else:
            return NotImplemented

        res.clean()
        return res

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        self.copy(self + other)
        return self

    def __sub__(self, other):
        if isinstance(other, (Degree, int, float)):
            return self + (-other)
        elif isinstance(other, dict):
            return self + (-(Degree(newvar=False, d=other)))
        else:
            return NotImplemented

    def __rsub__(self, other):
        return other + (-self)

    def __isub__(self, other):
        self.copy(self - other)
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = self.new_copy()
            for i in res.value.keys():
                res.value[i] *= other
            res.clean()
            return res
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self.copy(self * other)
        return self

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self * (1 / other)
        return NotImplemented

    def __itruediv__(self, other):
        self.copy(self / other)
        return self

    def __neg__(self):
        return self * (-1)

    @staticmethod
    def str_term(tup):
        idx, val = tup
        if val == 0:
            return ""
        if idx == 0:  # const
            if val > 0:
                return "+" + str(val)
            return str(val)

        GA = "\u03B1\u03B2\u03B3\u03B4\u03B5\u03B6\u03B7\u03B8\u03B9\u03Ba\u03Bb\u03Bc\u03Bd\u03Be\u03Bf\u03C0\u03C1\u03C2\u03C3\u03C4\u03C5\u03C6\u03C7\u03C8\u03C9"
        str_var = GA[idx - 1] if 0 < idx < len(GA) + 1 else f"A{idx-1}"
        if val == 1 or val == -1:
            sgn = "-" if val < 0 else "+"
            return sgn + str_var
        return str(val) + str_var

    def __str__(self):
        """Returns a greek letter or A{idx} polynomial"""
        res = ""
        for i in sorted(self.value.items())[::-1]:
            if res == "":
                if Degree.str_term(i)[0] == "+":
                    res = Degree.str_term(i)[1:]
                else:
                    res = Degree.str_term(i)
            else:
                res += " " + Degree.str_term(i)
        return res

    def __repr__(self):
        """Return <str(self)>"""
        return f"<{str(self)}>"

    def __lt__(self, other):
        """Do lexicographic compare between the objects' sorted keys"""
        if other is None:
            raise TypeError("NoneType compared to Degree")
        if isinstance(other, (int, float, dict)):
            return self < Degree(False, other)
        if isinstance(other, Degree):
            return sorted(list(self.value.keys())) < sorted(list(other.value.keys()))
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            if other == 0 and len(self.value) == 0:
                return True
            return len(self.value) == 1 and 0 in self.value and self.value[0] == other
        elif isinstance(other, (Degree, dict)):
            return self - other == 0
        else:
            return NotImplemented

    @classmethod
    def reset(cls):
        """Resets the variable count to start over from alpha"""
        Degree.nextVarIdx = 1
