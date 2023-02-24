from dataclasses import dataclass
from typing import List, Union
import json

NUMBERS_FILE = "numbers.txt"
SOLUTION_FILE = "solution.txt"
RESULT_NUMBER = 10
data = []


@dataclass
class Solution:
    operations = ["+", "-", "*", "/"]
    string: str
    number_ordering: List[int]
    operation_ordering: List[chr]
    ordering: List[chr]


@dataclass
class Number:
    individual: List[int]
    string: str
    solution: Solution = None


def load_numbers() -> None:
    with open(NUMBERS_FILE, "r") as file:
        for line in file.readlines():
            number: Number = Number(
                individual=[int(n) for n in [*line.strip()]],
                string=line.strip())
            data.append(number)

def format_number(number:Number):
    return {
        "individual": number.individual,

    }


def save_solutions() -> None:
    json_object = json.dumps(data[0], indent=4)
    with open(SOLUTION_FILE, "w") as file:
        file.write(json_object)


def find_solution(number: Number) -> None:
    for first in number.individual:
        available_numbers_first = number.individual.copy()
        available_numbers_first.remove(first)

        for second in available_numbers_first.copy():
            available_numbers_second = available_numbers_first.copy()
            available_numbers_second.remove(second)

            for third in available_numbers_second.copy():
                available_numbers_third = available_numbers_second.copy()
                available_numbers_third.remove(third)
                forth = available_numbers_third.pop()

                solution = find_operations([first, second, third, forth])
                if solution is None:
                    continue
                number.solution = solution
                return


def find_operations(individual: List[int]) -> Union[Solution, None]:
    for first in Solution.operations:
        # dont_remove_parenthesis()

        for second in Solution.operations:

            for third in Solution.operations:
                operations = [first, second, third]
                if try_solution(individual, [first, second, third]):
                    return Solution(
                        string=create_solution_string(individual, operations),
                        number_ordering=individual,
                        operation_ordering=operations,
                        ordering=[individual[0], first, individual[1], second, individual[2], third, individual[3]]
                    )
                for parenthesis_first in range(3):

                    for parenthesis_second in range(parenthesis_first + 1, 4):
                        numbers = individual.copy()
                        numbers[parenthesis_first] = f"( {numbers[parenthesis_first]}"
                        numbers[parenthesis_second] = f"{numbers[parenthesis_second]} )"
                        if try_solution(numbers, operations):
                            return Solution(
                                string=create_solution_string(numbers, operations),
                                number_ordering=individual,
                                operation_ordering=operations,
                                ordering=[individual[0], first, individual[1], second, individual[2], third,
                                          individual[3]]
                            )
    return None


def try_solution(numbers: List[int], operations: List[chr]) -> bool:
    try:
        if eval(create_solution_string(numbers, operations)) == RESULT_NUMBER:
            return True
    except ZeroDivisionError:
        pass
    return False


def create_solution_string(numbers: List[int], operations: List[chr]) -> str:
    return f"{numbers[0]} {operations[0]} {numbers[1]} {operations[1]} {numbers[2]} {operations[2]} {numbers[3]}"


def main() -> None:
    load_numbers()
    for number in data:
        find_solution(number)

    # for i, number in enumerate(data):
    #     i += 1
    #     if number.solution is None:
    #         print(f"{i:3}: No solutions for: {number.string}")
    #     else:
    #         print(f"{i:3}: {number.solution.string}")

    save_solutions()


if __name__ == '__main__':
    main()
