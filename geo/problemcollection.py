from tqdm import tqdm


class ProblemCollection:
    @classmethod
    def all(cls):
        ans = []
        for p in dir(cls):
            attr = getattr(cls, p)
            if not p.startswith("__") and not p == "all" and callable(attr):
                ans.append(attr)
        return ans

    @classmethod
    def check_all(cls, print_proof=False):
        problems = tqdm(cls.all())
        for prob in problems:
            if not ProblemCollection.check_prob(prob, print_proof):
                problems.close()
                print("Error in prob", prob)
                break
        else:
            print("All tests are valid!")

    @staticmethod
    def check_prob(func, print_proof=False):
        ans = func(print_proof)
        return ans[0] == ans[1]
