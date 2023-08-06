from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='django-hashedpass',
    version='0.1.0',
    description="Django management commands for changing users' hashed passwords.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Foo Chuan Wei',
    author_email='chuanwei.foo@hotmail.com',
    url='https://github.com/cwfoo/django-hashedpass',
    license='BSD 3-Clause License',
    license_file='LICENSE',
    packages=find_packages(exclude=['run_tests.py', 'tests']),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=['Django>=2.2'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
