# Feader - A feed reader CRUD Django app

---

## Setup local environment
1. Install virtualenv
```sh
    python -m pip install --user virtualenv
```

2. Init virtualenv and install requirements
```sh
    virtualenv env && source env/bin/activate && pip install -r requirements/base.txt
```

3. Export Django settings
```sh
    export DJANGO_SETTINGS_MODULE="feader.settings.base"
```

4. Setup database
```sh
    ./manage.py migrate
```

5. Fetch rss from urls
```sh
    ./manage.py fetch_rss url1,url2,url3
```

To see the output of the command not only in shell but also in pre-defined log file, run the following command:

```sh
    ./manage.py fetch_rss url1,url2,url3 2>&1 | tee -a <log_file_directory>
```

6. Run the web app
```sh
    ./manage.py runserver
```

Access `127.0.0.1:8000/rss-items/`

7. Unit test

```sh
    export DJANGO_SETTINGS_MODULE="feader.settings.test"
    pip install -r requirements/test.txt
    ./manage.py test
```
