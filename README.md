# dby

Migrate database structures

## About

Is usual the some database thoughtout time start to get complex and out of context, so when it happens is normal to do a database normalization and restrutur. After having a new database is required to keep the old data, at least, so *dby* is a tool that can help you with that.

## Features

- Database table migration

## Setup

First create your *yaml* config, something like the following:

```yaml
source_type: mysql
source_db: source
source_user: root
source_password: root
source_url: source_db

destination_type: mysql
destination_db: destination
destination_user: root
destination_password: root
destination_url: destination_db

migrations:
  posts:
    post_title: s.posts.post_name
    post_status: 1
    post_type:
      condition: "'Page' in s.posts.post_name"  
      true: "page"
      false: "post"
```

The exec the following command

```bash
python3 main.py file.yaml
```

## Testing

For now I am using docker to test it.

```bash
make up # will launch the containers
```

```bash
make enter # will enter on the test container

python main.py # run the app
```

That's it!