import sys
sys.stdout = open("test.txt", "w")
try:

  print('in main')
  import temp_ds18x    
  print('imported temp_ds18x')
  run_ds18x()
  print('returned to main')
  sys.stdout.close()
exept:
  sys.stdout.close()


