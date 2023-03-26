from ..log import logger, log
@log
def fibonacci(n: int, start: int = 3) -> list[int]:
  """
  Creates a list of fibonacci numbers of length n starting at start
  :param n: The number of fibonacci numbers to return
  :param start: The index of the first fibonacci number to return
  :return: A list of fibonacci numbers
  """
  fibonacci_numbers = []
  a, b = 0, 1
  for _ in range(n+start):
    fibonacci_numbers.append(a)
    a, b = b, a + b
  return fibonacci_numbers[start:]