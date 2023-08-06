from setuptools import setup
from setuptools import find_packages





setup(
    name="netoprmgr",
    version="v1.1.6",
    description="Project to Manage Network Operation.",
    long_description="Project to Manage Network Operation.\nType 'python -m netoprmgr.__main__' to run program\nNow using flask",
    #long_description_content_type="text/markdown",
    url="https://github.com/FunGuardian/netoprmgr",
    author="Funguardian, Dedar, Luthfi",
    author_email="cristiano.ramadhan@gmail.com",
    license="GPLv3+",
    packages=find_packages(exclude=("test*",)),
    install_requires=[
        'bcrypt==3.1.7',
        'cffi==1.14.0',
        'click==7.1.1',
        'cryptography==2.8',
        'Flask==1.1.2',
        'future==0.18.2',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'lxml==4.5.0',
        'MarkupSafe==1.1.1',
        'netmiko==3.1.0',
        'netoprmgr==1.1',
        'ntc-templates==1.4.0',
        'paramiko==2.7.1',
        'paramiko-expect==0.2.8',
        'pycparser==2.20',
        'PyNaCl==1.3.0',
        'pyserial==3.4',
        'python-docx==0.8.10',
        'scp==0.13.2',
        'six==1.14.0',
        'terminal==0.4.0',
        'textfsm==1.1.0',
        'Werkzeug==1.0.1',
        'xlrd==1.2.0',
        'XlsxWriter==1.2.8',
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    )
)
