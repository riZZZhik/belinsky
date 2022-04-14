[![Tests](https://github.com/riZZZhik/belinsky/workflows/Tests/badge.svg)](https://github.com/riZZZhik/belinsky/actions/workflows/tests.yaml)
[![Code analyzis](https://github.com/riZZZhik/belinsky/workflows/Code%20analyzis/badge.svg)](https://github.com/riZZZhik/belinsky/actions/workflows/code_analyzis.yaml)
[![Build and push](https://github.com/riZZZhik/belinsky/workflows/Push%20new%20release%20to%20Docker%20Hub/badge.svg)](https://github.com/riZZZhik/belinsky/actions/workflows/push_docker_image.yaml)

# How to use

## Run production
`docker-compose up --build` 

### Envs:
- BELINSKY_PORT (default: 4958) - Port to forward belinsky on.
- BELINSKY_SECRET_KEY (default: secrets.token_hex(16)) - App's secret key.
- BELINSKY_NUM_WORKERS (default: 4) - Number of worker processes for handling requests.
- BELINSKY_NUM_THREADS (default: 1) - Number of threads.
  - _NB! The suggested maximum number of workers\*threads is (2*CPU)+1_
- BELINSKY_WORKER_CLASS (default: sync) - Type of workers to use.
- BELINSKY_NUM_WORKER_CONNECTIONS (default: 1000) - Maximum number of simultaneous clients.

## Run observability
`docker-compose -f docker-compose.observability.yaml up --build`

### Envs:
- BELINSKY_OBSERVABILITY_PORT (default: 4800) - Port to forward Grafana on.

## Run tests
`docker-compose -f docker-compose.test.yaml up --build --abort-on-container-exit`

# API routes
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965?action=collection%2Ffork&collection-url=entityId%3D18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965%26entityType%3Dcollection%26workspaceId%3Def145b73-8364-42bb-bcd4-f7bce58058e2)

## Authentication requests

### 1. signup

#### JSON Body:
* username (str): Username.
* password (str): Password.

#### 200

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $BELINSKY_URL/signup
``` 

**Response**

```json
{
  "result": "Successfully signed up as your_username",
  "status": 200
}
```

#### 400

**Request**

```shell
curl $BELINSKY_URL/signup
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

#### 400

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username"}' \
  $BELINSKY_URL/signup
``` 

**Response**

```json
{
  "error": "Not enough keys in request. Required keys: username, password.",
  "status": 400
}
```

#### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $BELINSKY_URL/signup
``` 

**Response**

```json
{
  "result": "User with your_username username already exists.",
  "status": 406
}
```

----------------

### 2. login

#### JSON Body:
* username (str): Username.
* password (str): Password.

#### 200

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $BELINSKY_URL/login
``` 

**Response**

```json
{
  "result": "Successfully logged in as your_username",
  "status": 200
}
```

#### 400

**Request**

```shell
curl $BELINSKY_URL/login
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

#### 400

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username"}' \
  $BELINSKY_URL/login
``` 

**Response**

```json
{
  "error": "Not enough keys in request. Required keys: username, password",
  "status": 400
}
```

#### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "not_your_username", "password": "your_password"}' \
  $BELINSKY_URL/login
``` 

**Response**

```json
{
  "result": "User with not_your_username username not found. Please signup first",
  "status": 406
}
```

#### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "not_your_password"}' \
  $BELINSKY_URL/login
``` 

**Response**

```json
{
  "result": "Invalid password. Please try again.",
  "status": 406
}
```

----------------

### 3. logout

#### 200

**Request**

```shell
curl $BELINSKY_URL/logout
``` 

**Response**

```json
{
  "result": "Successfully logged out.",
  "status": 200
}
```

#### 406

**Request**

```shell
curl $BELINSKY_URL/logout
``` 

**Response**

```json
{
  "result": "You are not logged in.",
  "status": 406
}
```

### 4. delete-user

#### JSON Body:
* username (str): Username.
* password (str): Password.

#### 200

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "your_password"}' \
  $BELINSKY_URL/delete-user
``` 

**Response**

```json
{
  "result": "Successfully deleted your_username user",
  "status": 200
}
```

#### 400

**Request**

```shell
curl $BELINSKY_URL/delete-user
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

#### 400

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username"}' \
  $BELINSKY_URL/delete-user
``` 

**Response**

```json
{
  "error": "Not enough keys in request. Required keys: username, password",
  "status": 400
}
```

#### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "not_your_username", "password": "your_password"}' \
  $BELINSKY_URL/delete-user
``` 

**Response**

```json
{
  "result": "User with not_your_username username not found. Please signup first",
  "status": 406
}
```

#### 406

**Request**

```shell
curl \ 
  --header "Content-Type: application/json" \
  --data '{"username": "your_username", "password": "not_your_password"}' \
  $BELINSKY_URL/delete-user
``` 

**Response**

```json
{
  "result": "Invalid password. Please try again.",
  "status": 406
}
```

----------------


## Phrase finder requests

### 1. find-phrases

#### JSON Body:
* text (str): Text to be processed.
* phrases (List[str]): Phrases to be found.
* language (str)[Optional] - Language.

#### 200

**Request**

```shell
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"text": "мама по-любому любит banan", "phrases": ["банан"]], "languages": "ru"]}' \
  $BELINSKY_URL/find-phrases
``` 

**Response**

```json
{
  "result": {
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

#### 400

**Request**

```bash
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"text": "мама любит по-любому бананы"}' \
  $BELINSKY_URL/find-phrases
``` 

**Response**

```json
{
  "error": "Required keys not found in request body: text, phrases.",
  "status": 400
}
```

#### 400

**Request**

```bash
curl --request POST \
  $BELINSKY_URL/find-phrases
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```