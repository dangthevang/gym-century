from colorama import Fore, Back, Style

def errorColor(message):
  print(Fore.RED + message+"(Neu su dung action_space), thi day la action skip", end='')
  print(Style.RESET_ALL)
  pass

def successColor(message):
  print(Fore.BLUE + message, end='')
  print(Style.RESET_ALL)
  pass

def RecommendColor(message):
  print(Fore.YELLOW, message, end='')
  print(Style.RESET_ALL)
  pass