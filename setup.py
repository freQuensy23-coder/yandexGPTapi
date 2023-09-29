from setuptools import find_packages, setup

setup(
    name='ygpt',
    packages=find_packages(include=['ygpt', 'ygpt.*', 'ygpt.utils']),
    version='0.1.0',
    description='Yandendex GPT2 api wrapper',
    author='t.me/freQuensy23',
    license='MIT',
    install_requires=['pydantic', 'requests', 'python-dotenv', 'loguru'],
)