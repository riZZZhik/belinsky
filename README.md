[![Tests](https://github.com/riZZZhik/belinsky/workflows/Tests/badge.svg)](https://github.com/riZZZhik/belinsky/actions/workflows/tests.yaml)
[![Code analyzis](https://github.com/riZZZhik/belinsky/workflows/Code%20analyzis/badge.svg)](https://github.com/riZZZhik/belinsky/actions/workflows/code_analyzis.yaml)
[![Build and push](https://github.com/riZZZhik/belinsky/workflows/Push%20new%20release%20to%20Docker%20Hub/badge.svg)](https://github.com/riZZZhik/belinsky/actions/workflows/push_docker_image.yaml)

# How to use

## Run production
`docker-compose up --build` 

### Environments:
#### Application envs:
- BELINSKY_SECRET_KEY (default: secrets.token_hex(16)) - App's secret key.
- BELINSKY_PORT (default: 4958) - Port to forward belinsky on.

#### Gunicorn envs:
- BELINSKY_GUNICORN_CONFIG (defalut: gunicorn_config.py) - Path to Gunicorn config file.
- BELINSKY_NUM_WORKERS (default: 4) - Number of worker processes for handling requests.
- BELINSKY_NUM_THREADS (default: 1) - Number of threads.
  - _NB! The suggested maximum number of workers\*threads is (2*CPU)+1_
- BELINSKY_WORKER_CLASS (default: sync) - Type of workers to use.
- BELINSKY_NUM_WORKER_CONNECTIONS (default: 1000) - Maximum number of simultaneous clients.

## Run observability
`docker-compose -f docker-compose.observability.yaml up --build`

### Environments:
- BELINSKY_OBSERVABILITY_PORT (default: 4800) - Port to forward Grafana on.

## Run tests
`docker-compose -f docker-compose.test.yaml up --build --abort-on-container-exit`

# API routes

## Authentication requests
You can add _raw=true_ to any request body to receive response as json instead of web page.

### 1. signup

#### Form Body:
* username: Username.
* password: Password.

**Request**

```shell
curl -X POST $BELINSKY_URL/signup \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=your_username&password=your_password"
```

----------------

### 2. login

#### Form Body:
* username: Username.
* password: Password.

#### 200

**Request**

```shell
curl -X POST $BELINSKY_URL/login \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=your_username&password=your_password"
```

----------------

### 3. logout

#### 200

**Request**

```shell
curl $BELINSKY_URL/logout
```

----------------

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

### 1. phrase-finder

#### Form Body:
* text: Text to be processed.
* phrases: Phrases to be found.
* language [Optional]: Language. If not provided, will be determined automatically.

**Request**

```shell
curl -X POST $BELINSKY_URL/phrase-finder \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "text='мама по-любому любит banan'&phrases=банан"
```