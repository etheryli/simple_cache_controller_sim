from __future__ import division

import sys
from cache import Cache

if __name__ == '__main__':
    # Tuple list
    trace_list = []
    input_file = ''
    output_file = ''
    if len(sys.argv) != 3:
        input_file = "test.trace"
        output_file = "test.result"
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    with open(input_file) as f:
        for line in f.readlines():
            [command, value] = line.split()
            trace_list.append({'command': command, 'address': int(value, 0)})

    # DEBUG
    # for item in trace_list:
    #    print("%s %s" % (item['command'], item['address']))

    cache_sizes = [1024, 4096, 65536, 131072]
    block_sizes = [8, 16, 32, 128]
    cache_placements = ['DM', '2W', '4W', 'FA']
    write_policies = ['WB', 'WT']

    output = []
    # Proceeds to simulate
    for cache_size in cache_sizes:
        for block_size in block_sizes:
            for cache_placement in cache_placements:
                for write_policy in write_policies:
                    cache_simulator = Cache(trace_list, cache_size, block_size,
                                            cache_placement, write_policy)
                    result = cache_simulator.simulate_controller()
                    output.append(result)

    # Write to output file
    with open(output_file, 'w') as output_file:
        for result in output:
            output_file.write("%s\n" % result)
