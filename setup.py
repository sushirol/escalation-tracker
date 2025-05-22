# setup.py

from setuptools import setup

setup(
    name='escalation-tracker',
    version='0.3',
    py_modules=['escalation_tracker'],
    entry_points={
        'console_scripts': [
            'esc = escalation_tracker:main'
        ]
    },
    author='Your Name',
    description='CLI tool to track support escalations',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
