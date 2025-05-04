# nltask

## Getting Started

Follow the steps below to set up and run the project.

### Clone the Repository

```bash
git clone https://gitlab.com/nltask/nltask.git nltask
cd nltask
```

## Setting Up the Virtual Environment

### Windows

```bash
virtualvenv env
./env/Scripts/activate
```
### Ubuntu

``` bash
python3 -m venv env
. env/bin/activate
```
## Install Dependencies

```bash
pip install -r ./requirements.txt
```
## Run Migrations

```bash
./manage.py migrate
```
## Start the Development Server

```bash
./manage.py runserver
```
## Usage

After running the server, you can access the application in your browser at http://127.0.0.1:8000.