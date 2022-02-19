web: gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker  
worker: python -m redis_queue.worker