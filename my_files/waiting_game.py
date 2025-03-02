import time, random
def waiting_game():
  wait_time = random.randrange(1,10)
  print(f'Your target time is {wait_time} seconds')
  input('------ Press Enter to Begin -----')
  start = time.time()
  input(f'... Press Enter again in {wait_time} seconds ...')
  end = time.time()
  elapsed = end - start
  if wait_time == elapsed:
    print('Congratulations')
  elif elapsed > wait_time:
    print(f'Elapsed time: {elapsed}\n({elapsed - wait_time} too slow)')
  else:
    print(f'Whoa whoa hold your horses')

# Banner
print("#"*17)
print("# Waiting Game #")
print("#"*17)
waiting_game()