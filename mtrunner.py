from random import randint
from math import inf 
runs = 1000000
players = 2500

def run():
    rounds = 0
    lastplamt = inf
    plamt = players
    two_finale = False
    while plamt != 1:
        rounds += 1
        lastplamt = plamt
        plamt = randint(1, plamt)
        if lastplamt == plamt: plamt -= 1
        if plamt == 2: two_finale = True
    return (rounds, two_finale)

trounds = 0
ttfinals = 0
for _ in range(runs):
    murgame = run()
    trounds += murgame[0]
    ttfinals += murgame[1]

print(f'== {runs} runs of {players} players ==')
print(f'Total rounds: {trounds}')
print(f'Total two-player finales: {ttfinals}')
print('')
print(f'Average number of rounds per run: {trounds / runs}')
print(f'Average number of two-player finales per run: {ttfinals / runs} ({ttfinals / runs * 100}%)')