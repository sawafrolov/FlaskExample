from os import system as execute

if execute('pybabel compile -d app/translations'):
    raise RuntimeError('compile command failed')
