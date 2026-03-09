raw = 'ÐŁÑĢÐ¾'
print([hex(ord(c)) for c in raw])
try:
    b = raw.encode('latin1')
    print('bytes', b)
    print('decoded', b.decode('utf-8'))
except Exception as e:
    print('error', e)
