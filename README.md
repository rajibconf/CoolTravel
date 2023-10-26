# Cool Travel
## __Usage:__
>
> _Please make sure `python`, `postgresql` and `rabbitmq` is installed in the system._
>
> _NOTE for Windows users: Please use `Powershell or Git Bash` for the following steps_

1. ### Prepare project directory
    - Make your project directory (must be the same name as your github repository name)
    - Work from the project directory as current directory using `cd`.
    - Create a virtual environment using `python`. (Test via `python -V`. Must be python 3.10 or plus)
    - `Activate` the virtual environment. (Windows: `.\venv\Scripts\activate`)
    ```shell script
    cd CoolTravel
    python -m venv venv
    source venv/bin/activate
    # Windows: .\venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
2. ### Configure the project
    - Copy `local_settings.example` to `local_settings.py`.
    ```shell script
    cp examples/local_settings.example CoolTravel/local_settings.py
    ```

3. ### Create Database and User.
    - Using `psql`, create a `user` with encrypted `password`.
    - Create a `database` for your project.
    - Give privileges to the `user` for the `database`.
    - Alter `user` to allow for `test database` creation.
    ```shell script
    psql -U postgres -h localhost
    # psql console 
    CREATE USER cooltravel_user WITH ENCRYPTED PASSWORD 'admin';
    CREATE DATABASE cooltravel_db;
    GRANT ALL PRIVILEGES ON DATABASE cooltravel_db TO cooltravel_user;
    ALTER USER cooltravel_user CREATEDB;
    \q
    ```

4. ### Run the project
    - Run `makemigrations` and `migrate`.
    - Create superuser to access the admin panel.
    - Run django `server` to view the project or application.
    - Run `linting` to assure nothing is broken.
    ```shell script
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    flake8
    ```
   > _NOTE: Browse to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site. Admin site is at url [/manage](http://127.0.0.1:8000/manage) changed from default to keep the project secure. Admin url can be changed in `settings.py` --> `ADMIN_URL`_
 
```
  Happy coding!
```
