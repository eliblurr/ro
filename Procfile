release: python3 -m pip install -r ./requirements.txt
web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app