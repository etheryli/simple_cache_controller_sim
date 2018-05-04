from __future__ import division


# Cache class take in args and run simulator
class Cache:
    # Constructor
    def __init__(self, trace_list, cache_size, block_size, cache_placement,
                 write_policy):
        self._instructions = trace_list
        self._cache_size = cache_size
        self._block_size = block_size
        self._cache_placement = cache_placement
        self._write_policy = write_policy

        # Keep track of hit count and cache and memory data transfer amounts
        self._hit_count = 0
        self._cache_to_memory_data = 0
        self._memory_to_cache_data = 0
        self._global_clock = 0

        # Caclulations for n-way to one-way associativity
        # rows = set count
        # cols = blocks per set
        self._block_count = int(cache_size / block_size)
        self._blocks_per_set = self._find_blocks_per_set()
        self._set_count = int(self._block_count / self._blocks_per_set)
        self._set_size = int(self._cache_size / self._blocks_per_set)

        # Initialize empty cache list of unordered sets of blocks
        self._cache_list = [[{
            'valid': False,
            'dirty': False,
            'tag': -1,
            'age': 0
        } for each_block in range(self._blocks_per_set)]
                            for each_set_line in range(self._set_count)]

    def _find_blocks_per_set(self):
        # The cache acts like a 1-way associative for direct-mapped and
        # n-way is limited by cache size / block size for fully associative
        if self._cache_placement == 'DM':
            return 1
        elif self._cache_placement == '2W':
            return 2
        elif self._cache_placement == '4W':
            return 4
        return int(self._cache_size / self._block_size)

    def simulate_controller(self):
        for instruction in self._instructions:
            # Always increment global clock for each insruction
            self._global_clock += 1

            command = instruction['command']
            address = instruction['address']

            set_index = int(address / self._block_size) % self._set_count
            tag = int(address / self._set_size)

            set_line_tags = [
                block['tag'] for block in self._cache_list[set_index]
            ]

            # Determine if tag is in the set and check its valid bit for cache hit
            cache_hit = False
            block_index = int()

            if tag in set_line_tags:
                block_index = set_line_tags.index(tag)
                if self._cache_list[set_index][block_index]['valid']:
                    cache_hit = True

            if cache_hit:
                # increment hit count
                self._hit_count += 1

                # update age value
                self._cache_list[set_index][block_index][
                    'age'] = self._global_clock

                # write handling
                if command == 'write':
                    if self._write_policy == 'WT':
                        self._cache_to_memory_data += 4
                    elif self._write_policy == 'WB':
                        self._cache_list[set_index][block_index][
                            'dirty'] = True
            else:  # cache_miss
                # fetch from memory
                self._memory_to_cache_data += self._block_size

                # Special handling for LRU or allocate new block
                set_line_ages = [
                    block['age'] for block in self._cache_list[set_index]
                ]
                block_index = set_line_ages.index(min(set_line_ages))

                # Update tag, age, and valid bit of that block
                self._cache_list[set_index][block_index]['tag'] = tag
                self._cache_list[set_index][block_index]['valid'] = True
                self._cache_list[set_index][block_index][
                    'age'] = self._global_clock

                # Flush buffered data if write-back and dirty
                if self._write_policy == 'WB':
                    if self._cache_list[set_index][block_index]['dirty']:
                        self._cache_to_memory_data += self._block_size
                        self._cache_list[set_index][block_index][
                            'dirty'] = False

                # Write handling
                if command == 'write':
                    if self._write_policy == 'WT':
                        self._cache_to_memory_data += 4
                    elif self._write_policy == 'WB':
                        self._cache_list[set_index][block_index][
                            'dirty'] = True

        # Flush all dirty bits to memory
        for set_line in self._cache_list:
            for block in set_line:
                if block['dirty']:
                    self._cache_to_memory_data += self._block_size

        return self._output()

    def _output(self):
        # Format string for output to file
        hit_ratio = self._hit_count / len(self._instructions)

        data = (self._cache_size, self._block_size, self._cache_placement,
                self._write_policy, hit_ratio, self._memory_to_cache_data,
                self._cache_to_memory_data)

        formatted_string = ("%d\t%d\t%s\t%s\t%.2f\t%d\t%d" % data)
        # formatted_string = ("%d, %d, %s, %s, %.2f, %d, %d" % data)

        return formatted_string
