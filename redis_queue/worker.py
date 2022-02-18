from rq import  Worker
from .queues import redis, queues

workers = [ 
    Worker(
        queue,
        connection=redis,
        name=f"{key}-worker"
   )
   for key,queue in queues.items()
]

def run_workers(): 
    worker =  Worker( queues, connection=redis   )
    worker.work() 
    # for worker in workers:
    #     worker.work() 

