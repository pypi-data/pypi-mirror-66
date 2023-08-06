from setuptools import setup,find_packages

setup(

    name='weather_history',
    version='0.1.4',
    keywords=('pip','weather','history','china','city'),
    description="get chinese city's weather history data",
    long_description="get chinese city's weather history data",
    licence='MIT Licence',

    url='https://github.com/jim0575/desktop-tutorial',
    author='james',
    author_email="jim0575@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[]
    )
