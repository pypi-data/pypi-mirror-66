import paddle
import paddle.fluid as fluid
from paddle.fluid.incubate.fleet.collective import fleet, DistributedStrategy
import paddle.fluid.incubate.fleet.base.role_maker as role_maker

class DistributeProgram(object):
    def __init__(self):
        pass

    def build_program(optimizer, 
                      cost,
                      start_program, 
                      main_program,
                      dist_stratey):
        with fluid.program_guard(main_program, start_program)
            #TODO: modify fleet to build the program without optimizer and cost
            dist_optimizer = fleet.distributed_optimizer(optimizer, 
                                                         strategy=dist_strategy)
            dist_optimizer.minimize(cost)

