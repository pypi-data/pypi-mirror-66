from setuptools import setup

setup(
    name='wyqhello',
    version='0.1',
    py_modules=['hello'],
    install_requires=[
        'Click',
    ],
    description=(
        '王彦青第一次pyp测试'
    ),
    author='王彦青',
    author_email='18010117861@163.com',
    maintainer='<wyq>',
    entry_points='''
[console_scripts]
hello=hello:hello
''',
)