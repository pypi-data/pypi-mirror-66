from setuptools import setup, find_packages

with open('LICENSE', 'rt', encoding='utf8') as lic, open('README.md', 'rt', encoding='utf8') as readme:
    setup(
        name='simple_zuora_client',
        maintainer='Sergey Yakimov',
        maintainer_email='sergwy@gmail.com',
        version='0.1.0',
        url='https://gitlab.com/sergwy/simple-zuora-client',
        license=lic.read(),
        description='Simple Zuora Client',
        long_description=readme.read(),
        packages=find_packages(),
        install_requires=['requests', 'requests-oauth2', 'requests-oauthlib']
    )
