try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='django-context-extra-view',
    version='2020.4.19',
    packages=[
        'django_context_extra_view',
    ],
)
