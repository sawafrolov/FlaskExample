<h1>Welcome to Microblog!</h1>
<p>Приложение <b>Microblog</b> представляет собой пример использования фреймворка <b>Flask</b> совместно с <b>SQLAlchemy</b></p>
<h2>Использованные технологии</h2>
<ul>
    <li><p><b>Python 3</b></p></li>
    <li><p><b>SQLite</b></p></li>
    <li><p><b>Flask</b></p></li>
    <li><p><b>SQLAlchemy</b></p></li>
    <li><p><b>AJAX</b></p></li>
    <li><p><b>Bootstrap</b></p></li>
    <li><p><b>Google Translate API</b></p></li>
    <li><p><b>ElasticSearch</b></p></li>
    <li><p><b>Google SMTP Server</b></p></li>
    <li><p><b>JWT</b></p></li>
    <li><p><b>Moment.js</b></p></li>
</ul>
<h2>Подготовка к запуску приложения</h2>
<h3>Необходимые команды</h3>
<p>Перед запуском приложения необходимо, находясь в корневой папке проекта, выполнить в терминале следующие команды:</p>
<p><b>install_libraries</b></p>
<p>Эта команда установит все необходимые инструменты и библиотеки</p>
<p><b>python db_create.py</b></p>
<p>Эта команда создаст пустую базу данных SQLite</p>
<p><b>python db_migrate.py db init</b></p>
<p>Эта команда инициализирует Alembic - инструмент для миграции баз данных</p>
<p><b>python db_migrate.py db migrate</b></p>
<p>Эта команда создаст скрипт для миграции базы данных и ее отката</p>
<p><b>python db_migrate.py db upgrade</b></p>
<p>Эта команда создаст в базе данных необходимые таблицы</p>
<h3>Запуск ElasticSearch</h3>
<p>Для корректной работы поиска необходимо:</p>
<ul>
    <li><p>Скачать ElasticSearch с <a href="https://www.elastic.co/downloads/elasticsearch">официального сайта</a></p></li>
    <li><p>Распаковать скачанный архив</p></li>
    <li><p>Запустить файл <b>elasticsearch</b> из папки <b>bin</b></p></li>
</ul>
<h3>Настройка почтовой рассылки</h3>
<p>Для корректной работы почтовой рассылки создайте переменные окружения <b>GMAIL_USERNAME</b> и <b>GMAIL_PASSWORD</b> с логином и паролем своего <b>аккаунта Google</b></p>
<h2>Как запустить приложение</h2>
<p>Для запуска приложения необходимо, находясь в корневой папке проекта, выполнить в терминале команду:</p>
<p><b>python main.py</b></p>
<p>Эта команда запустит приложение Microblog на порту 5000 (по умолчанию)</p>