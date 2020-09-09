from functools import total_ordering


@total_ordering
class Length:

    nextGivenIdx = 2
    nextVarIdx = 1
    watched = []
    switched = []
    givenSymbols = {}

    def __init__(self, newvar=True, d={}):
        """Create Length object based on dict,int,float or empty (w/ or w/o newvar)"""
        if isinstance(d, dict):
            self.value = dict(d)
        elif isinstance(d, (int, float)):
            self.value = {0: d}
        else:
            raise TypeError(f"d as a {type(d)} is not supported")
        if newvar:
            self.value[Length.nextVarIdx] = 1
            Length.nextVarIdx += 1
        self.clean()

    def new_copy(self):
        """Return a new_copy of this object"""
        res = Length(False)
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

    def switch(self, key, switchlen):
        """switch every instance of this key to switchlen"""
        Length.switchWatched(key, switchlen)
        if key not in self.value:
            return
        else:
            times = self.value[key]
            del self.value[key]
            self += switchlen * times
            self.clean()

    def clean(self):
        """clean keys that have a zero value or float to int"""
        for key in [key for key in self.value if self.value[key] == 0]:
            del self.value[key]
        for key in self.value:
            if isinstance(self.value[key], float) and self.value[key].is_integer():
                self.value[key] = int(self.value[key])

    def isknown(self):
        """Check if the Length is known or has variables in it"""
        self.clean()
        for i in self.value:
            if i != 0:
                return False
        return True

    def __add__(self, other):
        """Add the values for the same key and add the missing keys with dict/Length/int/float"""
        res = self.new_copy()
        if isinstance(other, Length):
            for idx, val in other.value.items():
                if idx in res.value:
                    res.value[idx] += val
                else:
                    res.value[idx] = val
        elif isinstance(other, (dict, int, float)):
            return self + Length(newvar=False, d=other)
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
        if isinstance(other, (Length, int, float)):
            return self + (-other)
        elif isinstance(other, dict):
            return self + (-(Length(newvar=False, d=other)))
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
    def str_term(tup, custom):
        idx, val = tup
        if val == 0:
            return ""
        if idx == 0:  # const
            if val > 0:
                return "+" + str(val)
            return str(val)

        EA = "abcdefghijklmnopqrstuvwxyz"
        if isinstance(idx, int):
            str_var = EA[idx - 1] if 0 < idx < len(EA) + 1 else f"L{idx-1}"
        else:
            str_var = Length.givenSymbols[idx]
        if idx in custom:
            str_var = custom[idx]
        if val == 1 or val == -1:
            sgn = "-" if val < 0 else "+"
            return sgn + str_var
        sgn = "" if val < 0 else "+"
        return sgn + str(val) + str_var

    def __str__(self, *custom):
        """Returns a greek letter or L{idx} polynomial"""
        if len(custom) % 2 != 0:
            raise "problem!!!"
        else:
            d = {}
            for i in range(0, len(custom), 2):
                d[custom[i]] = custom[i + 1]
            custom = d

        res = ""
        for i in sorted(self.value.items())[::-1]:
            if res == "":
                if Length.str_term(i, custom)[0] == "+":
                    res = Length.str_term(i, custom)[1:]
                else:
                    res = Length.str_term(i, custom)
            else:
                res += " " + Length.str_term(i, custom)
        return res

    def __repr__(self):
        """Return <str(self)>"""
        return f"<{str(self)}>"

    def __lt__(self, other):
        """Do lexicographic compare between the objects' sorted keys"""
        if other is None:
            raise TypeError("NoneType compared to Length")
        if isinstance(other, (int, float, dict)):
            return self < Length(False, other)
        if isinstance(other, Length):
            return sorted(list(self.value.keys())) < sorted(list(other.value.keys()))
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            if other == 0 and len(self.value) == 0:
                return True
            return len(self.value) == 1 and 0 in self.value and self.value[0] == other
        elif isinstance(other, (Length, dict)):
            return self - other == 0
        else:
            return NotImplemented

    @classmethod
    def reset(cls):
        """Resets the variable count to start over from a"""
        Length.nextVarIdx = 1

    @classmethod
    def variable_reduction(cls, *all_len):
        """Replaces variables' names to fill the EA from the beginning"""
        existing_keys = set(sum([list(i.value.keys()) for i in all_len], []))
        if 0 in existing_keys:
            existing_keys.remove(0)
        xchg = 1
        for i in list(existing_keys)[::-1]:
            if i > len(existing_keys):
                while xchg in existing_keys:
                    xchg += 1
                for leng in all_len:
                    leng.switch(i, Length(False, {xchg: 1}))

    def watch(self):
        """Set watch on this Length (update its value when can)"""
        Length.watched.append(self)

    @classmethod
    def switchWatched(cls, key, leng):
        """Switch key for leng in every Length in watched if it hasn't been done before"""
        if (key, leng) in Length.switched:
            return
        Length.switched.append((key, leng.new_copy()))
        for w in Length.watched:
            w.switch(key, leng)

    @classmethod
    def given(cls, symbol):
        d = Length(False, {})
        d.value[1 / Length.nextGivenIdx] = 1
        Length.givenSymbols[1 / Length.nextGivenIdx] = symbol
        Length.nextGivenIdx += 1
        d.watch()
        return d

