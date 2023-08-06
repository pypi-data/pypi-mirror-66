'''
@File       :   setup.py.py
@Author     :   Jiang Fubang
@Time       :   2020/4/20 17:59
@Version    :   1.0
@Contact    :   luckybang@163.com
@Dect       :   None
'''
from setuptools import setup, find_packages

setup(
    name='fast_requests',
    version='1.0.0',
    keywords = ("spider", "requests"),
    description=(
        '无与伦比的简单且强大的requests'
    ),
    author='Jiang Fubang',
    author_email='luckybang@163.com',
    license='MIT Licence',
    packages=find_packages(),
    platforms=["all"],
    include_package_data = True,
    url='https://github.com/jiangfubang/fast_requests',
    install_requires=[
            'requests',
            'aiohttp',
        ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)