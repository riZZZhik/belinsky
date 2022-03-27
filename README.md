\
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965?action=collection%2Ffork&collection-url=entityId%3D18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965%26entityType%3Dcollection%26workspaceId%3Def145b73-8364-42bb-bcd4-f7bce58058e2)

# How to use

## Run production
`docker-compose up --build` 

### Envs:
- BELINSKY_SECRET_KEY (default: secrets.token_hex(16)) - App's secret key.
- BELINSKY_WSGI_MODULE (default: app:"create_app()") - WSGI application path in pattern $(MODULE_NAME):-$(VARIABLE_NAME).
- BELINSKY_HOST (default: 0.0.0.0) - Application hostname.
- BELINSKY_PORT (default: 4958) - Application port.
- BELINSKY_NUM_WORKERS (default: 4) - Number of worker processes for handling requests.
- BELINSKY_NUM_THREADS (default: 1) - Number of threads.
  - _NB! The suggested number of workers\*threads is (2*CPU)+1_
- BELINSKY_WORKER_CLASS (default: sync) - Type of workers to use.
- BELINSKY_NUM_WORKER_CONNECTIONS (default: 1000) - Maximum number of simultaneous clients.

## Run observability
`docker-compose -f docker-compose.observability.yaml up --build`

### Envs:
- BELINSKY_OBSERVABILITY_PORT (default: 4800) - Port to forward Grafana on.

## Run tests
`docker-compose -f docker-compose.test.yaml up --build --abort-on-container-exit`

# Authentication requests

## 1. signup

### 200

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $APP_URL/signup
``` 

**Response**

```json
{
  "result": "Successfully signed up as your_username",
  "status": 200
}
```

### 400

**Request**

```shell
curl $APP_URL/signup
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

### 400

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username"}' \
  $APP_URL/signup
``` 

**Response**

```json
{
  "error": "Not enough keys in request. Required keys: username, password",
  "status": 400
}
```

### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $APP_URL/signup
``` 

**Response**

```json
{
  "result": "User with your_username username already exists.",
  "status": 406
}
```

## 2. login

### 200

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $APP_URL/login
``` 

**Response**

```json
{
  "result": "Successfully logged in as your_username",
  "status": 200
}
```

### 400

**Request**

```shell
curl $APP_URL/login
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

### 400

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username"}' \
  $APP_URL/login
``` 

**Response**

```json
{
  "error": "Not enough keys in request. Required keys: username, password",
  "status": 400
}
```

### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "not_your_username", "password": "your_password"}' \
  $APP_URL/login
``` 

**Response**

```json
{
  "result": "User with not_your_username username not found. Please signup first",
  "status": 406
}
```

### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "not_your_password"}' \
  $APP_URL/login
``` 

**Response**

```json
{
  "result": "Invalid password. Please try again.",
  "status": 406
}
```


## 3. logout

### 200

**Request**

```shell
curl $APP_URL/logout
``` 

**Response**

```json
{
  "result": "Successfully logged out.",
  "status": 200
}
```

### 406

**Request**

```shell
curl $APP_URL/logout
``` 

**Response**

```json
{
  "result": "You are not logged in.",
  "status": 406
}
```

## 4. delete-user

### 200

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $APP_URL/delete-user
``` 

**Response**

```json
{
  "result": "Successfully deleted your_username user",
  "status": 200
}
```

### 400

**Request**

```shell
curl $APP_URL/delete-user
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

### 400

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username"}' \
  $APP_URL/delete-user
``` 

**Response**

```json
{
  "error": "Not enough keys in request. Required keys: username, password",
  "status": 400
}
```

### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "not_your_username", "password": "your_password"}' \
  $APP_URL/delete-user
``` 

**Response**

```json
{
  "result": "User with not_your_username username not found. Please signup first",
  "status": 406
}
```

### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "not_your_password"}' \
  $APP_URL/delete-user
``` 

**Response**

```json
{
  "result": "Invalid password. Please try again.",
  "status": 406
}
```


# Phrase finder requests

## 1. find-phrases

### 200

**Request**

```shell
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"text": "мама по-любому любит banan"}' \
  $APP_URL/find-phrases
``` 

**Response**

```json
{
  "result": {
    "мама": [
      [
        0,
        3
      ]
    ],
    "любой любить": [
      [
        5,
        19
      ]
    ],
    "банан": [
      [
        21,
        25
      ]
    ]
  },
  "status": 200
}
```

### 400

**Request**

```bash
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"no_text": "мама любит по-любому бананы"}' \
  $APP_URL/find-phrases
``` 

**Response**

```json
{
  "error": "item 'text' not found in request body",
  "status": 400
}
```

### 400

**Request**

```bash
curl --request POST \
  $APP_URL/find-phrases
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

----------------

## 2. add-phrase

### 200

**Request**

```bash
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"phrase": "Privet банану"}' \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "result": "ok",
  "status": 200
}
```

### 400

**Request**
```bash
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"no_phrase": "Privet банану"}' \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "error": "item 'phrase' not found in request body",
  "status": 400
}
```

### 400

**Request**

```bash
curl --request POST \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

### 406

**Request**

```bash
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"phrase": "Privet банану"}' \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "error": "phrase already in database",
  "status": 406
}
```

----------------

## 3. get-known-phrases

### 200

**Request**

```bash
curl $APP_URL/get-known-phrases
``` 

**Response**

```json
{
  "result": [
    "любой любить",
    "мама",
    "банан"
  ],
  "status": 200
}
```

----------------

## 4. clear-known-phrases

### 200

**Request**

```bash
curl --request POST \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "result": "ok",
  "status": 200
}
```
