class Problem:
    def __init__(self, page_num=None, problem_num=None, description=None):
        """Create a new problem"""

        self.page_num = page_num
        self.problem_num = problem_num
        self.description = description

        self.funcs = {}
        self.h = None

    def create(self):
        """Call create function and return Helper object"""
        self.h = self.funcs["create"]()
        return self.h

    def answer(self, sub_problem_number=None):
        """Call answer function and return the answer"""
        if self.h is None:
            self.create()
        return self.funcs["answer"](self.h, sub_problem_number)

    def currect_answer(self, sub_problem_number=None):
        """Call currect_answer function and return the right answer"""
        return self.funcs["currect_answer"](sub_problem_number)

    def set_create(self, f):
        """Set the create function"""
        self.funcs["create"] = f

    def set_answer(self, f):
        """Set the answer function"""
        self.funcs["answer"] = f

    def set_currect_answer(self, f):
        """Set the currect_answer function"""
        self.funcs["currect_answer"] = f

    def set_functions(self, create, answer, currect_answer):
        self.set_create(create)
        self.set_answer(answer)
        self.set_currect_answer(currect_answer)