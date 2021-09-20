<p align="center"> 
 <img src="https://vkssfalumni.com/wp-content/uploads/2016/11/sushikshalogo-300x300.png" alt="Sushiksha-lOGO" border="0" width=300 height=300/>&nbsp; </a></p>

<p class="text-center mb-3" align="center">
<a href="https://github.com/18praneeth/sushiksha-website/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/18praneeth/sushiksha-website?style=for-the-badge"></a>
<a href="https://github.com/18praneeth/sushiksha-website/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/18praneeth/sushiksha-website?style=for-the-badge"></a>
<a href="https://github.com/18praneeth/sushiksha-website/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/18praneeth/sushiksha-website?style=for-the-badge"></a>
</p>

<p class="text-center mb-3" align="center">
<a href="https://sushiksha.konkanischolarship.com/"><img src="https://forthebadge.com/images/badges/made-with-python.svg" border="0" title="Made with Python" /></a>
</p>

<p class="text-center mb-3" align="center">
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>
</p>

Sushiksha Mentoring Program is organized for scholars of Vishwa Konkani Student Scholarship Fund (VKSSF) by members of VKSSF Alumni Association (VAA). Sushiksha was started in 2018 by Royal Denzil Sequeira, a member of VAA since 2015, with 20 mentees. Since then Sushiksha has grown to be family of 170 mentees and 20 mentors. Mentees of Sushiksha are undergraduate scholars of VKSSF who are determined to thrive and be successful in their area of study and career. Mentors of Sushiksha Program are experienced professionals who were once the scholars of VKSSF and have lived through their own share of successes and failures but believe in empowering the scholars early on in their career path.

Sushiksha thrives because of the dedication of its active mentees and mentors – who have contributed countless hours of work to shape their future and make it a highly productive and focused workspace.

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#development">Development</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing / Adding Features</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


1. Backend Framework: **Django**
2. Front-end Framework: **Bootstrap**

## Installation 

1. Fork and Clone
    <ol>
    <li>Fork sushiksha-website the Repo</li>
    <li>Clone the repo to your computer.</li>
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
   
5. Create a `settings.py` in `sushiksha-website/djangoProject/`

    Copy paste the code from below document to `settings.py`
    
    [settings.py](https://github.com/18praneeth/sushiksha-website/blob/master/djangoProject/settings.py)
    
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
   
8. Run server
    ```bash
    python manage.py runserver
    ```
9. Do the Development and send me a PR referencing the issue.

## Development

    git checkout develop-<username>
    //Create the changes and then commit
    git add <filename>
    git commit -m "<Message here>"
    
From your `master` branch or your main branch that you are working on, give a PR to our `develop` branch.

Developers should create a folder /media and put an image named `default.jpg` to avoid errors in creating superuser.

`!IMPORTANT`: Don't give a PR to the master branch
We only accept PR's to `develop` branch.

   

## Contributing
   Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
   While sending the PR please mention the issue in the Comment.

**Note: PR's are accepted that are sent only by Sushiksha members.**

## License
[Apache License 2.0](https://github.com/18praneeth/sushiksha-website/blob/master/LICENSE)
