# Bread App

[![License: GPL--3.0](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://github.com/aidan-mcbride/bread-app/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/aidan-mcbride/bread-app.svg?branch=master)](https://travis-ci.org/aidan-mcbride/bread-app)

> Data-driven baking application

## Quick-start: user

### Prerequisites

<!-- must have docker installed to run -->
<!-- must have pipenv installed to develop -->

### Install

```sh
pipenv install
```

### Usage

```sh
pipenv run ?
```

### Run tests

```sh
pipenv run pytest
```

## Quick-start: developer

### Prerequisites

Package requirements are saved in a `Pipfile`, so you will need [Pipenv](https://pipenv.readthedocs.io/en/latest/) to install them.

### Install

```sh
pipenv install --dev
```

### Usage

Start uvicorn development server:

```sh
pipenv run uvicorn api.main:app --reload
```

You should then be able to access the api:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - interactive api documentation
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - alternative interactive api documentation

### Run tests

```sh
pipenv run python -m pytest
```

---

## Author

👤 **Aidan McBride**

- Github: [@aidan-mcbride](https://github.com/aidan-mcbride)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/aidan-mcbride/bread-app/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Aidan McBride](https://github.com/aidan-mcbride).

This project is [GPL--3.0](https://github.com/aidan-mcbride/bread-app/blob/master/LICENSE) licensed.

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
