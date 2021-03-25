from functools import total_ordering


@total_ordering
class Expression:

    next_given_idx = 2
    next_var_idx = 1
    watched = []
    switched = []
    given_symbols = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, newvar=True, d={}):
        """Create Expression object based on dict,int,float or empty (w/ or w/o newvar)"""
        if isinstance(d, dict):
            self.value = dict(d)
        elif isinstance(d, (int, float)):
            self.value = {0: d}
        else:
            raise TypeError(f"d as a {type(d)} is not supported")
        if newvar:
            # create new variable
            self.value[type(self).next_var_idx] = 1
            type(self).next_var_idx += 1
        self.clean()

    def new_copy(self):
        """Return a new_copy of this object"""
        res = type(self)(False)
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

    def switch(self, key, switch_exp):
        """switch every instance of this key to switch_exp"""
        type(self).switch_watched(key, switch_exp)
        if key not in self.value:
            return
        else:
            times = self.value[key]
            del self.value[key]
            self += switch_exp * times
            self.clean()

    def clean(self):
        """clean keys that have a zero value or float to int"""
        # remove zero value keys
        for key in [key for key in self.value if self.value[key] == 0]:
            del self.value[key]
        # convert float keys to int when needed
        for key in self.value:
            if isinstance(self.value[key], float) and self.value[key].is_integer():
                self.value[key] = int(self.value[key])

    def isknown(self):
        """Check if the expression is known or has variables in it"""
        self.clean()
        for i in self.value:
            if i != 0:
                return False
        return True

    def watch(self):
        """Set watch on this expression (update its value when can)"""
        type(self).watched.append(self)

    def __add__(self, other):
        """Add the values for the same key and add the missing keys with dict/Expression/int/float"""
        res = self.new_copy()
        if isinstance(other, type(self)):
            for idx, val in other.value.items():
                if idx in res.value:
                    res.value[idx] += val
                else:
                    res.value[idx] = val
        elif isinstance(other, (dict, int, float)):
            return self + type(self)(newvar=False, d=other)
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
        if isinstance(other, (type(self), int, float)):
            return self + (-other)
        elif isinstance(other, dict):
            return self + (-(type(self)(newvar=False, d=other)))
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

    @classmethod
    def str_term(cls, tup, custom):
        idx, val = tup
        if val == 0:
            return ""
        if idx == 0:  # const
            if val > 0:
                return "+" + str(val)
            return str(val)

        alp = cls.alphabet
        if isinstance(idx, int):
            str_var = alp[idx - 1] if 0 < idx < len(alp) + 1 else f"A{idx-1}"
        else:
            str_var = cls.given_symbols[idx]
        if idx in custom:
            str_var = custom[idx]
        if val == 1 or val == -1:
            sgn = "-" if val < 0 else "+"
            return sgn + str_var
        sgn = "" if val < 0 else "+"
        return sgn + str(val) + str_var

    def __str__(self, *custom):
        """Returns a alphabet letter or A{idx} polynomial"""
        if self == 0:
            return "0"
        if len(custom) % 2 != 0:
            raise "Custom alphabet size should be even!"
        else:
            d = {}
            for i in range(0, len(custom), 2):
                d[custom[i]] = custom[i + 1]
            custom = d

        res = ""
        for i in sorted(self.value.items())[::-1]:
            if res == "":
                if type(self).str_term(i, custom)[0] == "+":
                    res = type(self).str_term(i, custom)[1:]
                else:
                    res = type(self).str_term(i, custom)
            else:
                res += " " + type(self).str_term(i, custom)
        return res

    def __repr__(self):
        """Return <str(self)>"""
        return f"<{str(self)}>"

    def __int__(self):
        """Return the value of the expression"""
        if self.isknown():
            return self.value[0]
        raise ValueError(f"Cannot convert {self} to type int")

    def __lt__(self, other):
        """Do lexicographic compare between the objects' sorted keys"""
        if other is None:
            raise TypeError("NoneType compared to Degree")
        if isinstance(other, (int, float, dict)):
            return self < type(self)(False, other)
        if isinstance(other, type(self)):
            return sorted(list(self.value.keys())) < sorted(list(other.value.keys()))
        return NotImplemented

    def __eq__(self, other):
        """Compare two Expressions"""
        if isinstance(other, (int, float)):
            if other == 0 and len(self.value) == 0:
                return True
            return len(self.value) == 1 and 0 in self.value and self.value[0] == other
        elif isinstance(other, (type(self), dict)):
            return self - other == 0
        else:
            return NotImplemented

    @classmethod
    def reset(cls):
        """Resets the variable count to start over from alpha"""
        cls.nextVarIdx = 1

    @classmethod
    def variable_reduction(cls, *all_exp):
        """Replaces variables' names to fill the alphabet from the beginning"""
        existing_keys = set(sum([list(i.value.keys()) for i in all_exp], []))
        if 0 in existing_keys:
            existing_keys.remove(0)
        xchg = 1
        for i in list(existing_keys)[::-1]:
            if i > len(existing_keys):
                while xchg in existing_keys:
                    xchg += 1
                for exp in all_exp:
                    exp.switch(i, cls(False, {xchg: 1}))

    @classmethod
    def switch_watched(cls, key, exp):
        """Switch key for exp in every Expression in watched if it hasn't been done before"""
        if (key, exp) in cls.switched:
            return
        cls.switched.append((key, exp.new_copy()))
        for w in cls.watched:
            w.switch(key, exp)

    @classmethod
    def given(cls, *symbols):
        res = []
        for symbol in symbols:
            d = cls(False, {})
            d.value[1 / cls.next_given_idx] = 1
            cls.given_symbols[1 / cls.next_given_idx] = symbol
            cls.next_given_idx += 1
            d.watch()
            res.append(d)
        if len(res) == 1:
            return res[0]
        return tuple(res)

    @classmethod
    def reset_all(cls):
        """Reset's the entire class"""
        cls.next_given_idx = 2
        cls.next_var_idx = 1
        cls.watched = []
        cls.switched = []
        cls.given_symbols = {}


@total_ordering
class Degree(Expression):

    next_given_idx = 2
    next_var_idx = 1
    watched = []
    switched = []
    given_symbols = {}
    alphabet = "\u03B1\u03B2\u03B3\u03B4\u03B5\u03B6\u03B7\u03B8\u03B9\u03Ba\u03Bb\u03Bc\u03Bd\u03Be\u03Bf\u03C1\u03C2\u03C3\u03C4\u03C5\u03C6\u03C7\u03C8\u03C9"

    def __init__(self, newvar=True, d={}):
        Expression.__init__(self, newvar, d)


@total_ordering
class Length(Expression):

    next_given_idx = 2
    next_var_idx = 1
    watched = []
    switched = []
    given_symbols = {}

    def __init__(self, newvar=True, d={}):
        Expression.__init__(self, newvar, d)