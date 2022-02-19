web: gunicorn main:app -w 8 -k uvicorn.workers.UvicornWorker  
worker: python -m redis_queue.worker