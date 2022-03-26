
# ainBot

A bot that **will** fit all your needs (once it's done lmao)

Feel free to fork and recreate a private version of ainBot or whatever,
but don't make any bots made from a fork public. Especially don't sell them. 

## Installation
```sh
git clone https://github.com/aindrigo0/ainBot /ainBot
cd /ainBot
pip install -R requirements.txt
```
You must have a PostgreSQL installation.

## Config
The config template is stored at config.json.template.
To get the default blacklist, remove .template from blacklist.json.template
The following is a basic example:
```json
{
    "token": "TOKEN HERE",
    "postgres_user": "POSTGRES USERNAME HERE",
    "postgres_pass": "POSTGRES PASSWORD HERE",
    "postgres_db": "POSTGRES DB HERE"
}
```