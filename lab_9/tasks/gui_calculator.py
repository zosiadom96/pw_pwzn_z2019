import tkinter as tk
from functools import partial
from operator import add, mul, sub, truediv


class CalculatorError(Exception):
    pass


class WrongOperation(CalculatorError):
    pass


class NotNumberArgument(CalculatorError):
    pass


class EmptyMemory(CalculatorError):
    pass


class Calculator:
    operations = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
    }

    def __init__(self):
        self._memory = None
        self._short_memory = None

    @staticmethod
    def _cast_to_num(val):
        try:
            return float(val)
        except TypeError:
            return complex(val)

    def run(self, operator, arg1, arg2=None):
        """
        Returns result of given operation.
        :param operator: sign of operation to perform
        :type operator: str
        :param arg1: first argument, must be a numeric value
        :type arg1: float
        :param arg2: optional, second argument, must be a numeric value
        :type arg2: float
        :return: result of operation
        :rtype: float
        """
        try:
            arg2 = arg2 if arg2 is not None else self.memory
            res = self.operations[operator](
                self._cast_to_num(arg1),
                self._cast_to_num(arg2),
            )
            self._short_memory = self._cast_to_num(res)
        except KeyError:
            raise WrongOperation()
        except (ValueError, TypeError):
            raise NotNumberArgument()
        except ZeroDivisionError as _exc:
            raise CalculatorError() from _exc
        else:
            return self._short_memory

    @property
    def memory(self):
        if self._memory is not None:
            return self._memory
        else:
            raise EmptyMemory()

    def memorize(self):
        """Saves last operation result to memory."""
        self._memory = self._short_memory

    def clean_memory(self):
        """Cleans memorized value"""
        self._memory = None

    def in_memory(self):
        """Prints memorized value."""
        print(f"Zapamiętana wartość: {self.memory}")


if __name__ == '__main__':
    b = None
    calc = Calculator()

    try:
        b = calc.run('+', 1, 'a')
    except CalculatorError as exc:
        assert type(exc) == NotNumberArgument
        assert b is None
    try:
        b = calc.run('^', 2, 3)
    except CalculatorError as exc:
        assert type(exc) == WrongOperation
        assert b is None
    try:
        calc.in_memory()
    except CalculatorError as exc:
        assert type(exc) is EmptyMemory
    else:
        raise AssertionError
    try:
        b = calc.run('/', 2)
    except CalculatorError as exc:
        assert type(exc) == EmptyMemory
        assert b is None
    else:
        raise AssertionError

    try:
        b = calc.run('/', 1, 0)
    except CalculatorError as exc:
        assert type(exc.__cause__) == ZeroDivisionError


class CalculatorGUI(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.variables = {}
        self.state = tk.BooleanVar(value=True)
        self.init_variables()
        self.calculator = Calculator()

        self.screen = tk.Label(self, bg='white')
        self.screen.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_pad = self.init_bottom_pad()
        self.bottom_pad.pack(side=tk.BOTTOM)

    def init_variables(self):
        self.variables['var_1'] = ''
        self.variables['var_2'] = ''
        self.variables['operator'] = ''
        self.state.set(True)

    def init_bottom_pad(self):
        bottom_pad = tk.Frame(self)

        # klawiatura numeryczna
        num_pad = tk.Frame(bottom_pad)
        num_pad.pack(side=tk.LEFT)
        ii = 0
        for ii, num in enumerate(range(9, 0, -1)):
            tk.Button(
                num_pad, text=num, width=5,
                command=partial(self.update_var, num)
            ).grid(row=ii // 3, column=(2 - ii) % 3)
        ii += 1
        tk.Button(
            num_pad, text='C', width=5,
            command=self.clear
        ).grid(row=ii // 3, column=ii % 3)
        ii += 1
        tk.Button(
            num_pad, text='0', width=5,
            command=partial(self.update_var, '0')
        ).grid(row=ii // 3, column=ii % 3)
        ii += 1
        tk.Button(
            num_pad, text='=', width=5,
            command=self.calculate_result,
        ).grid(row=ii // 3, column=ii % 3)
        tk.Button(
            num_pad, text='MC', width=5,
            command=self.clean_memory
        ).grid(row=5, column=0)
        ii += 1
        tk.Button(
            num_pad, text='MR', width=5,
            command=self.read_from_memory
        ).grid(row=5, column=1)
        ii += 1
        tk.Button(
            num_pad, text='M+', width=5,
            command=self.memorize
        ).grid(row=5, column=2)
        # klawiatura operacji
        operation_pad = tk.Frame(bottom_pad)
        operation_pad.pack(side=tk.RIGHT)
        for ii, operation in enumerate(self.calculator.operations.keys()):
            tk.Button(
                operation_pad, text=operation, width=5,
                command=partial(self.set_operator, operation),
            ).grid(row=ii, column=0)
        tk.Button(
            operation_pad, text='.', width=5,
            command=partial(self.update_var, '.')
        ).grid(row=5, column=0)

        return bottom_pad

    def memorize(self):
        # breakpoint()
        state = self.state.get()
        if state:
            self.calculator._short_memory = self.variables['var_1'] or self.screen['text']
            self.calculator.memorize()
        else:
            self.calculator._short_memory = self.variables['var_2'] or self.variables['var_1']
            self.calculator.memorize()

    def read_from_memory(self):
        state = self.state.get()
        if state:
            self.variables['var_1'] = float(self.calculator.memory)
        else:
            self.variables['var_2'] = float(self.calculator.memory)
        self.update_screen()

    def clean_memory(self):
        self.calculator.clean_memory()

    def update_screen(self):
        text = f"{self.variables['var_1']}"
        if self.variables['operator']:
            text += f" {self.variables['operator']}"
        if self.variables['var_2']:
            text += f" {self.variables['var_2']}"
        self.screen['text'] = text

    def clear(self):
        state = self.state.get()
        if state:
            self.variables['var_1'] = ''
        else:
            self.variables['var_2'] = ''
        self.update_screen()

    def update_var(self, num):
        state = self.state.get()
        if state:
            try:
                float(self.variables['var_1'] + str(num))
                self.variables['var_1'] += str(num)
                self.variables['var_1'] = self.variables['var_1'].lstrip('0')
            except ValueError:
                print("Invalid input attempt.")

        else:
            try:
                float(self.variables['var_2'] + str(num))
                self.variables['var_2'] += str(num)
                self.variables['var_2'] = self.variables['var_2'].lstrip('0')
            except ValueError:
                print("Invalid input attempt.")
        self.update_screen()

    def set_operator(self, operator):
        if self.variables['var_1']:
            self.variables['operator'] = operator
            self.state.set(not self.state.get())
            self.update_screen()

    def calculate_result(self):
        if self.variables['var_1'] and self.variables['var_2']:
            var_1 = float(self.variables['var_1'])
            var_2 = float(self.variables['var_2'])
            self.screen['text'] = self.calculator.run(
                self.variables['operator'], var_1, var_2
            )
            self.init_variables()


if __name__ == '__main__':
    root = tk.Tk()
    CalculatorGUI(root).pack()
    root.mainloop()