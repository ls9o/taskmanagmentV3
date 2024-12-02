import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from common.greeter import Greeter


def main():
    greeter = Greeter()
    greeter.say_hello()


if __name__ == "__main__":
    main()
