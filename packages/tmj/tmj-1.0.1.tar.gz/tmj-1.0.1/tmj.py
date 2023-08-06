import dataclasses
import queue
import time
from typing import List, Callable

import colorama
from colorama import Fore, Style


@dataclasses.dataclass
class Exercise:
    name: str
    reps: int
    hold_time: float
    rep_delay: float = 2

    def _perform(self) -> None:
        for i in range(self.reps):
            print(
                f"\tNow doing rep: {i + 1}, hold for {self.hold_time} seconds")
            time.sleep(self.hold_time)
            print("\tGet ready to do the next rep!")
            time.sleep(self.rep_delay)
            print(
                f"\tExercise done! Press {Fore.GREEN}ENTER{Style.RESET_ALL} to continue."
            )

    def exec_buf(self) -> List[Callable[[], None]]:
        return [
            lambda: print(
                f"Press {Fore.GREEN}ENTER{Style.RESET_ALL} when ready to "
                f"do exercise {Fore.YELLOW}'{self.name}'{Style.RESET_ALL}"),
            self._perform
        ]


def welcome_msg():
    print(f"Press {Fore.GREEN}ENTER{Style.RESET_ALL} to begin")


def main():
    colorama.init()

    exercises = map(lambda name: Exercise(name, 10, 10),
                    ["Push up", "Pull down", "Push left", "Push right"])
    exercise_funcs = [
        func for exercise in exercises for func in exercise.exec_buf()
    ]

    exec_queue = queue.SimpleQueue()
    exec_queue.put(welcome_msg)
    for exercise_func in exercise_funcs:
        exec_queue.put(exercise_func)

    while not exec_queue.empty():
        exec_queue.get()()
        input()


if __name__ == "__main__":
    main()