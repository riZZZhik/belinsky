[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965?action=collection%2Ffork&collection-url=entityId%3D18220726-51689aa2-6ff2-4ffa-a278-e46ae40c6965%26entityType%3Dcollection%26workspaceId%3Def145b73-8364-42bb-bcd4-f7bce58058e2)

# How to use

## Run production on one host
`docker-compose up --build`

## Run production on several hosts
`docker-compose -f docker-compose.several.yaml up --build --scale app=$NUM_HOSTS`

## Run tests
`docker-compose -f docker-compose.test.yaml up --build --exit-code-from word_finder_app_test`

# API requests
## 1. highlight-words

### 200

**Request**


```shell
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"text": "мама любит по-любому бананы"}' \
  $APP_URL/highlight-words
``` 

**Response**

```json
{
  "result": {
    "любить любой": [
      [
        5,
        19
      ]
    ],
    "любой": [
      [
        11,
        19
      ]
    ],
    "недолюбливать апельсин": [
      [
        36,
        59
      ]
    ],
    "ненавидеть": [
      [
        61,
        70
      ],
      [
        72,
        79
      ],
      [
        81,
        90
      ]
    ],
    "очень супер длинный фраза": [
      [
        92,
        116
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
  $APP_URL/highlight-words
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
  $APP_URL/highlight-words
``` 

**Response**

```json
{
  "error": "json body not found in request",
  "status": 400
}
```

----------------

## 2. add-new-word

### 200

**Request**

```bash
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"word": "Privet банану"}' \
  $APP_URL/add-new-word
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
  $APP_URL/add-new-word
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
  $APP_URL/add-new-word
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
  --data '{"no_word": "Privet банану"}' \
  $APP_URL/add-new-word
``` 

**Response**

```json
{
  "error": "word already in database",
  "status": 406
}
```

----------------

## 3. get-all-words

### 200

**Request**

```bash
curl $APP_URL/get-all-words
``` 

**Response**

```json
{
  "result": [
    "недолюбливать апельсин",
    "любой",
    "ненавидеть",
    "любить любой",
    "очень супер длинный фраза"
  ],
  "status": 200
}
```

----------------

## 4. clear-all-words

### 200

**Request**

```bash
curl --request POST \
  $APP_URL/add-new-word
``` 

**Response**

```json
{
  "status": 200
}
```

----------------



# Task
Необходимо реализовать сервис поиска и выделения заданных в начальной форме слов и словосочетаний в тексте.
Взаимодействие с сервисом должно быть реализовано через REST API.

## POST: `localhost/highlight-words`

request_body: `{'text': 'мама любит бананы'}`

response_body: `{'result': {'любить банан': [[5, 17],]}}`

## POST: `localhost/add-new-word`

request_body: `{'word': 'молоко'}`

response_body: `{'result': 'ok'}`

## GET: `localhost/get-all-words`

request_body: `{}`

response_body: `{'result': ['любить банан', 'молоко']}`

## Необходимо учесть:
- текст может содержать разные формы слов(любить, любила, любят и т.д.)
- слова и словосочетания в тексте могут начинаться с предлогов с дефисом (например, сервис должен начти слово "любой", в тексте "по-любому сделаю это задание")
- метод highlight-words должен возвращать список найденных слов, которые хранятся в mongodb, в виде словаря, в котором ключами являются найденные слова, а значениями - список списков, имеющих следующую структуру - [позиция_первой_буквы_найденного_слова, позиция_последней_буквы_найденного_слова]
- mongodb необходимо поднимать контейнером рядом с сервисом посредством docker-compose
- код должен быть написан и выложен в открытом репозитории на gitlab или github

## Что будет оценено:
- следование требованиям в задаче
- стиль написания кода
- обработки крайних случаев
- работоспособность сервиса
- README в репозитории

## Необязательно, но будет круто:
- обработка транслита слов в предложении и букв в словах
- покрытие unit-тестами
- оптимизация работы и сравнение алгоритмов
- предложения по улучшению

## Стек
- python3.8
- docker + docker-compose
- flask
- mongodb4.4.3
