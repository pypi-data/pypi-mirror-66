from setuptools import setup,find_packages

setup(
    name='wyqhello',
    version='0.5',
    # py_modules=['hello'],
    packages=find_packages(),
    platforms=["all"],
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
hello=wyqhello.hello:hello
''',
)