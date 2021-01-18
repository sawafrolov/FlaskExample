from os import system as execute

if execute('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
    raise RuntimeError('extract command failed')
if execute('pybabel update -i messages.pot -d app/translations'):
    raise RuntimeError('update command failed')
