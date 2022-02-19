web: gunicorn main:app -w 12 -k uvicorn.workers.UvicornWorker  
worker: python -m redis_queue.worker