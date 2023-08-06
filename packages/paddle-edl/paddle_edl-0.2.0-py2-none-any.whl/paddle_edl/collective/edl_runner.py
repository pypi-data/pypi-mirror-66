from distributed_program import DistributeProgram 
class ClusterConfig(object):
    def __init__(self):
        cpu = None
        gpu = None
        memory = None

class WorkerRange(object):
    def __init__(self, min_num, max_num):
        self.min = min_num
        self.max = max_num

class Runner(object):
    def __init__(self):
        pass

    # TODO(gongwb): remove the optimizer and loss?
    def init(mode, num_workers=Range(4,8), 
             start_program, main_program, optimizer, loss,  
             dist_strategy, cluster_config=None):
        """
        mode: local or cluster
        """
        self._mode = mode
        self.num_workers = num_workers
        self._start_program = start_program
        self._main_program  = main_program
        self._optimizer = optimizer
        self._loss = loss
        self._dist_strategy = dist_stratey
        self._cluster_config = cluster_config

        #FIXME(gongwb):request them from cluster or start it local
        self.job_server = os.getenv("PADDLE_JOBSERVER")
        self.job_id = os.getenv("PADDLE_JOB_ID")

        edl_env = edl_utils.Edlenv(running_env="PADDLE_EDL", 
                                   job_server=self.job_server,
                                   job_id=self.job_id)

        cluster, _ = edl_env.get_cluster()

    def load_check_point(self):
        pass

    def save_check_point(self):
        pass

    def execute(self, data, fetch_list=[]): 
        while True:
            step_status = 


