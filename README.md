<h2>Personal_Telegram_Bot </h2>
<br>
<div>
<b>This project provides an API service that allows users to:</b>
<ul>
<li>Register with a login, password, and username.</li>
<li>Authenticate using their login and password.</li>
<li>Connect a Telegram bot to their account.</li>
</ul>
</div>
<br>
:sparkles:<b>Tech Stack</b>:sparkles:<br>
FastApi, PostgreSQL, Docker, Pytest, Aiogram
<hr> 
<div>
<h3>Docker Deploy on Windows</h3>

```commandline
    git clone https://github.com/735Andrew/Personal_Telegram_Bot 
    cd Personal_Telegram_Bot   
```
<br>
Create a <b>.env</b> file in the root directory with the following variables: <br>
<b><span style="color:orange;">/app/.env</span></b>

```commandline 
    POSTGRES_USER = <USER_VARIABLE>
    POSTGRES_PASSWORD = <PASSWORD_VARIABLE>
    POSTGRES_DB = <DB_VARIABLE>
    POSTGRESQL_DATABASE_URL = postgresql://<USER_VARIABLE>:<PASSWORD_VARIABLE>@db:5432/<DB_VARIABLE>
    JWT_SECRET_KEY = <JWT_VARIABLE>
```
<br>
Open a terminal in the root directory and run the following command: 

```commandline
    docker-compose up -d 
```
</div>
<hr>
<h3>API Specification</h3>

- User creation `POST /users/sign_up`

Request example:
```json
{
  "login": "string",
  "password": "string",
  "name": "string"
}
```

Response example:
```json
{
  "auth_token": "string",
  "login": "string",
  "password": "string",
  "u_id": "integer",
  "name": "string"
}
```
<br>

- User authentication `POST /users/log_in`

Request example:
```json
{
  "login": "string",
  "password": "string"
}
```

Response example:
```json
{
  "access_token": "string"
}
```
<br>

- Connection to bot `POST /users/bot_connect`

Request example:
```json
{
  "bot_token": "string" // You should take it from @BotFather
}
```
Headers:
```commandline
access_token <token>
```
<br>
Response example:

```json
{
  "bot_connection": "success"
}
```
