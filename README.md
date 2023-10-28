# Cool Travel
## __Usage:__
>
> _Please make sure `python-3.10`, and `postgresq-15 or newest` is installed in the system._
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
    - Using `psql`
    - Create a `database` for your project.
    ```shell script
    psql -U postgres -h localhost
    # psql console 
    CREATE DATABASE cooltravel_db;
    \q
    ```

4. ### Run the project
    - Run `makemigrations` and `migrate`.
    - Create superuser to access the admin panel.
    - Run django `server` to view the project or application.
    - Run `linting` to assure nothing is broken. (Make sure your virtual environment is named venv)
    ```shell script
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    flake8
    ```
5. ### Import district data from a JSON file (json_file_path = 'fixtures/bd-districts.json')
    - Run `python manage.py import_district_data` to create district with lat, long
    ```shell script
    python manage.py import_district_data
    ```
6. ### API Instructions
    - Top 10 Coolest District API
    ![GitHub Logo](https://github.com/yourusername/yourrepository/blob/main/staticfiles/images/coolest_district.png)

    - Travel Recommendation API
    ![GitHub Logo](https://github.com/yourusername/yourrepository/blob/main/staticfiles/images/travel_recommendation.png)

   > _NOTE: Browse to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site. Admin site is at url [/manage](http://127.0.0.1:8000/manage) changed from default to keep the project secure. Admin url can be changed in `settings.py` --> `ADMIN_URL`_
 
```
  Happy coding!
```
