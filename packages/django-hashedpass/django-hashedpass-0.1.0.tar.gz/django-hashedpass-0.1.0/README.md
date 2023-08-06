# django-hashedpass

Django management commands for changing users' hashed passwords.


## Installation
Requirements: Django >= 2.2, Python >= 3.5.

Install:
```bash
$ pip install django-hashedpass
```

Then, edit your Django project's `settings.py` file:
```python
INSTALLED_APPS = [
    # ...
    'django_hashedpass',  # NOTE: underscore (_), not dash (-).
    # ...
]
```


## Usage
* `changehashedpass` - Change a user's hashed password.
    ```bash
    $ python3 manage.py changehashedpass 'admin' 'pbkdf2_sha256$150000$yAhqE5ZDGEii$lD5JUoCuz6qRA+BVlvetFPGyGMwLmYl0rCc3awcNYLo='
    Successfully changed the hashed password for "admin".
    ```

* `genhashedpass` - Generate a hashed password from a plaintext password.
    ```bash
    $ python3 manage.py genhashedpass
    Password:
    Password (again):
    pbkdf2_sha256$150000$ZOTZr0AKGQyW$y6+Bdqwn9UsP/riDoEaMQ9Q17Sw8zZoH1jxmlgy94oA=
    ```
    ```bash
    $ python3 manage.py genhashedpass --password '123456'
    pbkdf2_sha256$150000$AnoGZfdqz6pW$GUGUJR5CggZA4e4JUMdtN8GU1CejLYTKs3PIdOnbF4k=
    ```


## Development
To run unit tests: `python3 ./run_tests.py`.

Tested on Django 2.22, Python 3.6.8, Ubuntu 18.04.

Project started on: 2019-07-21


## License
This project is distributed under the BSD 3-Clause License (see LICENSE).
