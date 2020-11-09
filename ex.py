import sys

def log(msg):
    print(msg, file=sys.stderr)

log('oh no, bad news')
log('oh god, somehow it got worse')
log('everything is fine now')
log('jk, we are NOT FINE')
print('this is just normal output')
