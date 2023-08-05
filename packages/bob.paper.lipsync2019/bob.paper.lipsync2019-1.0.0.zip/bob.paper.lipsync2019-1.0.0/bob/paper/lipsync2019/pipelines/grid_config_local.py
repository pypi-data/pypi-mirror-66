# Config script for running algorithms on a single machine

import bob.bio.base

# uncomment this part and comment out the rest of the lines
# if you do not want to parallelize (good for debugging)

grid = None

# for running on a single local machine in 4 parallel processes
# grid = bob.bio.base.grid.Grid(
#    grid_type='local',
#    number_of_parallel_processes=4
# )
# run_local_scheduler = True
# nice = 10
