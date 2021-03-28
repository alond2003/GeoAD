from tqdm import tqdm


class ProblemCollection:
    @classmethod
    def all(cls):
        """Return all problem functions from class"""
        ans = []
        for p in dir(cls):
            attr = getattr(cls, p)
            if not p.startswith("__") and callable(attr):
                if p not in ["all", "check_all", "check_prob"]:
                    ans.append(attr)
        return ans

    @classmethod
    def check_all(cls, print_proof=False):
        """Check all problem functions from class"""
        problems = tqdm(cls.all())
        for prob in problems:
            try:
                is_solved = ProblemCollection.check_prob(prob, print_proof)
                if not is_solved:
                    problems.close()
                    print("Error in prob", prob)
                    break
            except Exception as e:
                problems.close()
                print(e)
                print("Error in problem", prob)
                break
        else:
            print("All tests are valid!")

    @staticmethod
    def check_prob(func, print_proof=False):
        """"Check a single problem function"""
        ans = func(print_proof)
        return ans[0] == ans[1]
