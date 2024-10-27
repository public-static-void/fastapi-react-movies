# Movie Manager Full Stack Showcase Template Project

## Technologies used:

### Backend: Python, FastAPI, Pydantic, SQLalchemy, SQLite3, Poetry, Isort, Flake8, Mypy, Pylint, Black, Pytest, Pre-commit, Commitizen

![pytest](backend/movies_backend/badges/tests.svg)
![coverage](backend/movies_backend/badges/coverage.svg)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pylint](https://img.shields.io/badge/linting-pylint-brightgreen)](https://pylint.pycqa.org/en/latest/)
[![Flake8](https://img.shields.io/badge/flake8-passed-brightgreen)](https://flake8.pycqa.org/en/latest/)
[![Mypy](https://img.shields.io/badge/mypy-passed-brightgreen)](http://mypy-lang.org/)

### Frontend: TypeScript, React, Redux, TaildwindCSS, Vite, Jest, ESLint, Prettier, Stylelint, MSW, Husky, Lint-staged, Commitizen

![Jest Lines Coverage](frontend/movies_frontend/badges/lines.svg)
![Jest Average Coverage](frontend/movies_frontend/badges/average.svg)
![Jest Functions Coverage](frontend/movies_frontend/badges/functions.svg)
![Jest Branches Coverage](frontend/movies_frontend/badges/branches.svg)
![Jest Statements Coverage](frontend/movies_frontend/badges/statements.svg)
[![ESLint](https://img.shields.io/badge/ESLint-4B32C3?logo=eslint&logoColor=white)](https://eslint.org/)
[![Stylelint](https://img.shields.io/badge/stylelint-4B32C3?logo=stylelint&logoColor=white)](https://stylelint.io/)
[![Prettier](https://img.shields.io/badge/Prettier-ff69b4?logo=prettier&logoColor=white)](https://prettier.io/)

### Dev Tools: Docker

#### How to run:

##### Spin up the containers:

    docker-compose up -d --build

###### App will run on localhost Port 80 by default

##### How to stop:

    docker-compose stop

##### How to purge containers and networks:

    docker-compose down

##### How to purge volumes:

    docker-compose down --volumes

##### How to purge images:

    docker-compose down --rmi
