import multiprocessing

bind = ":80"
#worker_class = 'uvicorn.workers.UvicornH11Worker'
workers = multiprocessing.cpu_count() * 2 + 1
chdir = '/root/myweb'
pidfile = 'gun.pid'
daemon = True

accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
capture_output = True
enable_stdio_inheritance = True

keyfile = None
certfile = None


# keyfile = 'cert/scs1634265093478_www.realtoraccess.com_server.key'
# certfile = 'cert/scs1634265093478_www.realtoraccess.com_server.crt'
