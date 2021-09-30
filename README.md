## Setup
### 1. Install Python3 interpreter
Additional information on https://www.python.org/downloads/

### 2. Clone this repository into your directory

    mkdir ecommerce_project && cd ecommerce_project
    git clone https://github.com/DenisDanchyk/ecommerce_project.git
    cd ecommerce_project


### 3. Create virtual environment

    python -m venv venv
    venv\scripts\activate.bat


### 4. Install requirements


    pip install -r requirements.txt
    cd core

  
### 5. Set you Google account credentials for authentication system
In `core/settings.py` add your Google account credentials to `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`. If you don't have Google account - <a href="https://accounts.google.com/signup">create it</a>. Alternitavely, you can use other SMTP host.
Instructions, how to set Django SMTP described 
<a href="https://medium.com/@_christopher/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e">here</a>.

    SECRET_KEY = '1234567890'
    DEBUG = False
    
    
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    # TODO:
    EMAIL_HOST_USER = ""
    # TODO:
    EMAIL_HOST_PASSWORD = ""
    

### 6. Make migrations and run server
    python manage.py makemigrations 
    python manage.py migrate 
    python manage.py runserver
