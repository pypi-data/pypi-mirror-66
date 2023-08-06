from os.path import dirname, join
from setuptools import setup, find_packages


setup(
    name='custom-django-auth-backend',
    version='0.1.3',
    license='MIT',
    url='https://github.com/Chiorufarewerin/custom-django-auth-backend',
    author='Artur Beltsov',
    author_email='artur1998g@gmail.com',
    description='Easy add some auth backends in django project',
    long_description=open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    keyword=['django', 'auth', 'backend'],
    project_urls={
        'GitHub': 'https://github.com/Chiorufarewerin/custom-django-auth-backend',
    },
    install_requires=[
        'autowrapt>=1.0',
        'django<3.0',
        'lazy-object-proxy==1.4.*',
    ],
)
