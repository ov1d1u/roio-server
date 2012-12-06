import os, time

def log(text):
    fh = open('roio_server.log', 'a')
    line = '[' + time.strftime('%Y/%m/%d %H:%M') + '] ' + os.environ["REMOTE_ADDR"] + ': ' + text + '\n'
    fh.write(line)
    fh.close()