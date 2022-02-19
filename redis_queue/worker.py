from rq import  Worker, Connection
from .queues import redis, queues

workers = [ 
    Worker(
        queue,
        connection=redis,
        name=f"{key}-worker",
   )
   for key,queue in queues.items()
] # not used

if __name__ == '__main__':
    with Connection(redis):
        worker = Worker( queues, connection=redis )
        worker.work()