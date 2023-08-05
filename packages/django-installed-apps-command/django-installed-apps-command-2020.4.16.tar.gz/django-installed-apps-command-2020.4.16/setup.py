from setuptools import setup

setup(
    name='django-installed-apps-command',
    version='2020.4.16',
    install_requires=[
        'Django',
        'setuptools',
    ],
    packages=[
        'django_installed_apps_command',
        'django_installed_apps_command.management',
        'django_installed_apps_command.management.commands',
    ],
)
