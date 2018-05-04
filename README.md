# simple_cache_controller_sim

# Hung Nguyen
Simple stats for Direct-mapped, 2-way, 4-way, fully-associative, LRU, Write-through/Write-back cache of variable block/cache sizes.

Instruction: 

Usage with input and output specifications: 

    python simulate.py <input trace file> <output file>

or  use this if you want to default to input = test.trace and output = test.result 

    python simulate.py


Both python2 and 3 should be supported, try either.

Fast run:
for f in {1..3}; do python3 main.py test$f.trace test$f.out; done


Multi diff:
for f in {1..3}; do cat test$f.result | diff test$f.out - && echo $; done


Single diff:
cat test3.result | diff test3.out - && echo $
