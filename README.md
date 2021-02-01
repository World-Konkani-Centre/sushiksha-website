# Sushiksha-website 

<p class="text-center mb-3" align="center">
<a href="https://github.com/18praneeth/sushiksha-website/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/18praneeth/sushiksha-website?style=for-the-badge"></a>
<a href="https://github.com/18praneeth/sushiksha-website/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/18praneeth/sushiksha-website?style=for-the-badge"></a>
<a href="https://github.com/18praneeth/sushiksha-website/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/18praneeth/sushiksha-website?style=for-the-badge"></a>
</p>

<p class="text-center mb-3" align="center">
<a href="https://tutorvita.herokuapp.com/"><img src="https://forthebadge.com/images/badges/made-with-python.svg" border="0" title="Made with Python" /></a>
</p>

<p class="text-center mb-3" align="center">
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>
</p>

#### Project description

1. Backend Framework: **Django**
2. Front-end Framework: **Bootstrap**

## Installation 

1. Fork and Clone
    <ol>
    <li>Fork sushiksha-website the Repo</li>
    <li>Clone the repo to you computer.</li>
    </ol>

2. Create a Virtual Environment for the Project

    In Windows
    ```bash
    python -m venv venv
    
    venv\Scripts\activate
    ```

    In Ubuntu/MacOS
    ```bash
    python -m virtualenv venv
    
    source venv/bin/activate
    ```
   
   If you are giving a different name then `venv`, then please mention it in `.gitigonre` first

3. Install all the requirements

    ```bash
    pip install -r requirements.txt
    ```
   
4. Checkout to develop branch
     ```git
    git status
    git pull
    git branch
    git checkout develop
    ```
   
5. Create a `setting.py` in `sushiksha-website/djangoProject/`

    Copy paste the code from below document to `settings.py`
    
    [settings.py](https://github.com/18praneeth/sushiksha-website/blob/test/djangoProject/settings.py)
    
    Change the config parameters,
    ```python
   
   SECRET_KEY = 'Enter random character string'
   EMAIL_USER = 'your email username'
   EMAIL_PASS = 'Enter you email password'
   SLACK_AUTH_TOKEN: "token here"

    ```
   
   comment line #44 of users/signals.py (send_email.delay(array)) during development and uncomment before sending PR

6. Make migrations/ Create db.sqlite3

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. Create a super user.
    In django if you want to access admin page, you need to create an account first.
    ```djangotemplate
    python manage.py createsuperuser
    ```
   Then select your username and password.
   
7. Run server
    ```bash
    python manage.py runserver
    ```
8. Do the Development and send me a PR referencing the issue.
   

## Contributing
   Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
