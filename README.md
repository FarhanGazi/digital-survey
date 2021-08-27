# DigitalSurvey

# First configuration
1. clone the repo
```bash
git clone git@github.com:FarhanGazi/digital-survey.git
```

2. connect to postgresql database
```bash
psql
```

3. Execute the first `sql` script located inside `db/` folder of `digital-survey` project
```bash
database => \i ~/path/to/digital-survey/db/script1.sql
```

4. Go inside digital-survey project dir
```bash
cd ~/path/to/digital-survey
```

5. Create `config.yaml` file in the root of `digital-survey` folder in the following format:
```yaml
ds:
  database:
    driver: postgresql
    username: username
    password: password
    host: localhost
    port: 5432
    databasename: databasename
  application:
    secretkey: secret
admin:
  database:
    driver: postgresql
    username: username
    password: password
    host: localhost
    port: 5432
    databasename: databasename
  application:
    secretkey: secret
panelist:
  database:
    driver: postgresql
    username: username
    password: password
    host: localhost
    port: 5432
    databasename: databasename
  application:
    secretkey: secret
```

6. Create virtual evnvironment in `python3` and intsall all the packeges
```bash
cd ~/path/to/digital-survey
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

7. Create project environment variables
```bash
export FLASK_APP=ds
export FLASK_ENV=development
```

8. Run the project
```bash
flask run
```

9. From the project database `ds` execute the second script
```bash
psql ds
ds => \i ~/path/to/digital-survey/db/script2.sql
```

10. That's it! Enjoy Digital Survey ;)
