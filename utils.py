import os, time

def log(text):
    fh = open('roio_server.log', 'a')
    line = '[' + time.strftime('%Y/%m/%d %H:%M') + '] ' + os.environ.get("REMOTE_ADDR", "0.0.0.0") + ': ' + text + '\n'
    fh.write(line)
    fh.close()