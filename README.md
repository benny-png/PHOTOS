
# UDSM 2023 Students Existing Dataset for Face Recognition

## Overview

This repo provides details about the UDSM 2023 student dataset, which was intended for use in face recognition tasks based on student IDs. The dataset includes students ID numbers' which exists by sending HTTP request to check photos links existance. The primary purpose of this dataset is to facilitate face recognition tasks and experiments related to student identification. For example, an existing image can be accessed via the following URL: [Sample Image](https://aris3.udsm.ac.tz/uploaded_files/student/photos/2023-04-06833.jpg).

## Dataset Details

- **Source**: Aris UDSM Uploads
- **Image Format**: JPEG
- **Date Range**: April 2023
- **ID Format**: `2023-04-XXXXX` (where `XXXXX` is a 5-digit number)

## Dataset Structure

The dataset consists of image links based on existing IDs with photos:

```
photos/
│
├── 2023-04-00001.jpg
├── 2023-04-00002.jpg
├── ...
└── 2023-04-99999.jpg
```

---

This way, the URL is included as a clickable link without displaying the image directly.

# Fastapi Template

This is a template for fastapi projects. It includes a basic structure for the project, a docker-compose file for development and a dockerfile for production.

The guides on [fastapi](https://fastapi.tiangolo.com/learn/), [SQLmodel ORM](https://sqlmodel.tiangolo.com/) and [docker](https://docs.docker.com/get-started/) are a good place to start.

## Structure

The project structure is as follows:

```text
└── Project Directory
    ├── Virtual Environment(if you have to use one)
    └── Project
        ├── README.md
        ├── README.Docker.md
        ├── Dockerfile
        ├── compose.yaml
        ├── app.py
        ├── requirements.txt
        ├── .gitignore
        └── src
            ├── __init__.py
            ├── database
            │   ├── README.md
            │   ├── __init__.py
            │   ├── connect.py
            │   ├── enums.py
            │   └── models.py
            ├── main
            │   ├── README.md
            │   ├── __init__.py
            │   ├── app.py
            │   └── routes
            │       ├── README.md
            │       ├── __init__.py
            │       └── users.py
            ├── schemas
            │   ├── README.md
            │   └── __init__.py
            ├── tests
            │   └── README.md
            └── utilities
                └── README.md
```

## Usage

1. Clone the repository
2. Create a virtual environment and activate it
    Resources on how to create a virtual environment:
    - [Python Docs](https://docs.python.org/3/library/venv.html)
    - [Real Python](https://realpython.com/python-virtual-environments-a-primer/)
