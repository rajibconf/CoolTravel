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
    flake8
    python manage.py runserver
    ```
5. ### Import district data from a JSON file (json_file_path = 'fixtures/bd-districts.json')
    - Run `python manage.py import_district_data` to create district with lat, long
    ```shell script
    python manage.py import_district_data
    ```

6. ### CoolTravel's API Instructions
    ### 2. Top 10 Coolest District API (Average temperature at 2 PM for the next 7 days)
    ![GitHub Logo](https://github.com/rajibconf/CoolTravel/blob/main/staticfiles/images/coolest_district.png)

    **API Endpoint**: `GET http://127.0.0.1:8000/api/cool-district/`
    - **Request**:
        - **HTTP Method**: GET
        - **Query Parameters**:
            - `page` (integer): The page number to retrieve cool districts. Defaults to 1.
    
    **Example Request**:
    ```http
    GET http://127.0.0.1:8000/api/cool-district/?page=1
    ```
    ```shell script
    # Example using Python and requests library
    import requests

    url = "http://127.0.0.1:8000/api/cool-district/"
    params = {"page": 1}

    response = requests.get(url, params=params)
    print(response.json())
    ```
    **Response**:
    - **Status Code**:
        - `200 OK`: The request was successful.
        - `400 Bad Request`: The request was invalid or missing parameters.
        - **Response Body** (JSON):
            - `next_page` (integer): The page number of the next set of results, if available.
            - `previous_page` (integer): The page number of the previous set of results, if available.
            - `results` (array of objects): An array of cool districts. Each object represents a district and may include various attributes such as `name`, `average_temperature_2pm`, etc.
    
    **Example Response**:
    ```json
    {
        "count": 64,
        "next": "http://127.0.0.1:8000/api/cool-district/?page=2",
        "previous": null,
        "results": [
            {
                "id": 31,
                "name": "Panchagarh",
                "bn_name": "পঞ্চগড়",
                "lat": "26.3411",
                "long": "88.5541606",
                "average_temperature_2pm": 19.8
            }
        ]
    }
    ```

    ```shell script
    -------
    ```
    
    ### 2. Travel Recommendation API (Temperature at 2 PM at the source location and destination location on a given day and the day must be within the next 7 days.)
    
    ![GitHub Logo](https://github.com/rajibconf/CoolTravel/blob/main/staticfiles/images/travel_recommendation.png)

    **API Endpoint**: `POST http://127.0.0.1:8000/api/travel-recommendation/`
    - **Request**:
        - **HTTP Method**: POST
        - **Query Parameters**:
            - `source_location` (string): The source location for the travel recommendation.
            - `destination_location` (string): The destination location for the travel recommendation.
            - `travel_date` (string): The date of travel in the format "DD-MM-YYYY".

    **Example Request**:
    ```http
    POST http://127.0.0.1:8000/api/travel-recommendation/?source_location=barishal&destination_location=rajshahi&travel_date=29-10-2023
    ```

    ```shell script
    # Example using Python and requests library
    import requests

    url = "http://127.0.0.1:8000/api/travel-recommendation/"
    params = {
        "source_location": "barishal",
        "destination_location": "rajshahi",
        "travel_date": "29-10-2023"
    }

    response = requests.post(url, params=params)
    print(response.json())
    ```
    **Response**:
    - **Status Code**:
        - `200 OK`: The request was successful.
        - `400 Bad Request`: The request was invalid or missing parameters.
    - **Response Body** (JSON):
        - `recommendation` (string): A travel recommendation based on the provided locations and date.

    **Example Response**:
    ```json
    {
        "source_location": "Barishal",
        "destination_location": "Rajshahi",
        "source_temperature_2pm": "32.4°C",
        "destination_temperature_2pm": "31.8°C",
        "recommendation_message": "Your Barishal is warmer than your destination Rajshahi. Traveling is a good idea."
    }
    ```

   > _NOTE: Browse to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site. Admin site is at url [/manage](http://127.0.0.1:8000/manage) changed from default to keep the project secure. Admin url can be changed in `settings.py` --> `ADMIN_URL`_
 
```
  Happy coding!
```
