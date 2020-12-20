# pxSync

An NHS.UK-branded application to be used for synchronising repeat prescriptions.

The application is designed to be used by patients for inputting their prescription information, with a credential-based login for GPs to search for patient-provided reference numbers.

## Getting started

There are several steps involved in getting the application running, depending on your use-case. To just get the application running locally, follow the local installation section. If you're interested in testing, deploying, or customising the application styling/recompiling the NHS.UK toolkit, there are corresponding sections for these areas.

### Prerequisites

This guide assumes that:

- you have pulled a copy of the code into its own folder
- you are in the root of that folder
- you have Python 3 installed
- you have pip installed
- you are able to create virtual environments (this guide uses virtualenv)

### Local installation

1. Create a virtual environment

   ```python
   virtualenv .
   ```

2. Activate virtual environment

   ```python
   Scripts\activate.bat # windows, or...
   source bin/activate # mac
   ```

3. Install dependencies

   ```python
   pip install -r requirements.txt
   ```

4. Create a superuser

   ```python
   python px_sync/manage.py createsuperuser # from root, or...
   python manage.py createsuperuser # from px_sync subfolder
   ```

   Provide a username, password and optionally an email address.

5. Run the server

   ```python
   python px_sync/manage.py runserver # from root, or...
   python manage.py runserver # from px_sync subfolder
   ```

6. Visit application

   There are three URLs of particular importance, these are:

   - http://127.0.0.1:8000/prescriptions/start - The public-facing synchronisation app. No login is required, simply follow the journey through to input prescription information.
   - http://127.0.0.1/prescriber/login - The authenticated application. If you've set up a user, you can log in and search for any synchronisation requests that you've created.
   - http://127.0.0.1/manage - The standard django administration application. As user access will be gated to only prescribers, this is used to add users to the system.

### Testing the application

These steps assume you've already followed the local installation instructions.

Before testing the application, you'll need to install Google Chrome and obtain the selenium webdriver for the version of Chrome you plan to test with. This should be placed in the virtualenv-created folders to scope it to the pxSync application, however you may also wish to install globally.

1. Start the server in a terminal

   ```python
   python px_sync/manage.py runserver # from root, or...
   python manage.py runserver # from px_sync subfolder
   ```

2. In another terminal, start the django test framework (this will run functional and unit tests - this will take a little while)

   ```python
   python px_sync/manage.py test # from root, or...
   python manage.py test # from px_sync subfolder
   ```

Optionally, you may run subsections of the tests:

```python
# skips integration(journey) tests
python manage.py test --exclude-tag=journey
# runs a subset of integration tests. several values can be passed, comma separated.
# valid tags are:
# create - the initial tests for sync creation
# addpx - tests adding and editing prescription objects
# additem - tests adding and editing items on a prescription
# postpx - tests final stages up to viewing a sync request
# login - tests login and validates authenticated pages require authentication
# view - tests searching and viewing requests
python manage.py test --tag=comma,separated,tags
```

### Compiling the NHS.UK toolkit

pxSync uses the NHS.UK front-end toolkit, which is compiled directly from the NHS.UK SASS. A compiled version is supplied in the static resources folder for convenience, however if you do need to make any changes (such as adding custom SASS) then follow these steps.

If you already have Node.js, npm and a means to compile SASS, you can skip portions of this and substitute with your own compilation route.

1. Install Node.js and npm. There are numerous ways to do this, mentioned [here](https://nodejs.org/en/download/package-manager)

2. Navigate to the root folder of pxSync and run the following commands:

   ```
   npm install nhsuk-frontend --save
   npm i --global gulp-cli
   npm i gulp --save-dev
   npm i --save-dev gulp-sass
   npm i --save-dev del
   ```

   If you're curious, this installs the toolkit, the gulp command line interface, gulp itself, the gulp SASS compiler, and the del command necessary to remove old versions of the files.

3. Once you've done this, in future you can just run...

   ```
   gulp
   ```

   ...from the root directory to clear down styles.css and replace it with whatever custom code you've added to style.scss (or a custom.scss you've imported into style.scss if you want to do it that way)

Note: As per NHS.UK guidance, the assets and JS files are grabbed directly from the installed NHS.UK front-end node packages - so if you're updating the toolkit to a newer version, make sure to copy across the amended assets and nhsuk.min.js file.

### Deploying the application

TBC

## Built with

- [Django](https://www.djangoproject.com/) - Python web framework
- [Selenium](https://selenium-python.readthedocs.io/) - User journey automation test framework
- [NHS.UK Design system](https://service-manual.nhs.uk/design-system) - The front-end framework used to style the application to NHS.UK standards

## Authors

- Matt Graham

## License

This project is licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)