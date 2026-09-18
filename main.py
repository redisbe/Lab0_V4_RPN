import yaml
from tabulate import tabulate

OPS = {"+": 2,"-": 2, "*": 2, "/": 2} #добавлен минус


def load_cases(path):
    with open(path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data["cases"] #cases, а не case


def apply_op(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return int(a / b) #Деление целочисленное к нулю


def solve(seq):
    stack = []
    mx = None
    for token in seq:
        if token in OPS:
            if len(stack) < 2:
                return None, mx, "not enough operands"
            b = stack.pop() #правый операнд
            a = stack.pop() #левый операнд
            if token == "/" and b == 0:
                return None, mx, "division by zero"
            value = apply_op(token, a, b)
            stack.append(value)
        else:
            value = int(token) #преобразование строки в целое число
            stack.append(value)
        if mx is None or value > mx:
            mx = value

    if len(stack) != 1: #в стеке должно остаться только одно значение
        return None, mx, "leftover values on stack"
    return stack[0], mx, None


def main():
    rows = []
    best_n, best_v = None, None
    for n, case in enumerate(load_cases("data.yaml"), 1):
        value, mx, err = solve(case)
        rows.append([n, " ".join(case), value if err is None else "", mx if err is None else "", err or ""])
        if err is None and (best_v is None or value > best_v):
            best_n, best_v = n, value
    print(tabulate(rows, headers=["line", "expression", "value", "max_intermediate", "error"], tablefmt="github"))
    print("\nBest case: %s, value = %s" % (best_n, best_v))


if __name__ == "__main__":
    main()
