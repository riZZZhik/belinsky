\
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965?action=collection%2Ffork&collection-url=entityId%3D18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965%26entityType%3Dcollection%26workspaceId%3Def145b73-8364-42bb-bcd4-f7bce58058e2)

# How to use

## Run production
`docker-compose up --build --scale app=[NUM_HOSTS]`

## Run tests
`docker-compose -f docker-compose.test.yaml up --build --abort-on-container-exit`

# API requests

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
  --data '{"word": "Privet банану"}' \
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
  --data '{"no_word": "Privet банану"}' \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "error": "item 'word' not found in request body",
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
  --data '{"word": "Privet банану"}' \
  $APP_URL/add-phrase
``` 

**Response**

```json
{
  "error": "word already in database",
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