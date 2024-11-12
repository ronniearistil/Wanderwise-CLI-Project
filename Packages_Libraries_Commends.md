## "pipenv graph" to view Packages and Libraries 
appnope==0.1.4
attrs==24.2.0
babel==2.16.0
backcall==0.2.0
click==8.1.7
Faker==30.8.2
├── python-dateutil [required: >=2.4, installed: 2.9.0.post0]
│   └── six [required: >=1.5, installed: 1.16.0]
└── typing_extensions [required: Any, installed: 4.12.2]
ipdb==0.13.13
├── decorator [required: Any, installed: ?]
└── ipython [required: >=7.31.1, installed: ?]
jedi==0.19.1
└── parso [required: >=0.8.3,<0.9.0, installed: 0.8.4]
matplotlib-inline==0.1.7
└── traitlets [required: Any, installed: 5.14.3]
pexpect==4.9.0
└── ptyprocess [required: >=0.5, installed: 0.7.0]
pickleshare==0.7.5
prompt_toolkit==3.0.48
└── wcwidth [required: Any, installed: 0.2.13]
py==1.11.0
pydantic==2.9.2
├── annotated-types [required: >=0.6.0, installed: 0.7.0]
├── pydantic_core [required: ==2.23.4, installed: 2.23.4]
│   └── typing_extensions [required: >=4.6.0,!=4.7.0, installed: 4.12.2]
└── typing_extensions [required: >=4.12.2, installed: 4.12.2]
pytest==8.3.3
├── iniconfig [required: Any, installed: 2.0.0]
├── packaging [required: Any, installed: 24.1]
└── pluggy [required: >=1.5,<2, installed: 1.5.0]
python-dotenv==1.0.1
rich==13.9.4
├── markdown-it-py [required: >=2.2.0, installed: 3.0.0]
│   └── mdurl [required: ~=0.1, installed: 0.1.2]
└── Pygments [required: >=2.13.0,<3.0.0, installed: 2.18.0]
SQLAlchemy==2.0.36
└── typing_extensions [required: >=4.6.0, installed: 4.12.2]
stack-data==0.6.3
├── asttokens [required: >=2.1.0, installed: 2.4.1]
│   └── six [required: >=1.12.0, installed: 1.16.0]
├── executing [required: >=1.2.0, installed: 2.1.0]
└── pure_eval [required: Any, installed: 0.2.3]

## User Commands:
python cli.py add-user – Add a new user.
python cli.py list-users – List all users.

Destination Commands:
python cli.py add-destination – Add a new destination for a user.

Activity Commands:
python cli.py add-activity – Add a new activity for a destination.

Expense Commands:
python cli.py add-expense – Add an expense for an activity.
Validator Methods (from ValidatorMixin in helpers.py)

# Tests Commends:
pytest

## Run Seeds File
python seed.py

