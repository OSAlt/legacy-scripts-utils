# Deprecated

# This project is no longer maintained.  It had a use case for turning a google sheet form response into a database, but is no longer relevant. Archiving in case there is some use case later down the line.


# Running Project

## Requirements

Project has been migrated to Python 3.x.  Please make sure you are using
the correct version of python while executing.

### Dependencies


```bash
pip3 install -r requirements.txt

OR

python3 -m pip install -r requirements.txt

```

## Database 

A postgres Database is required.  Docker contain is provided for ease of use 
or execute the SQL in sql/ folder against your own SQL server and configure 
the app accordingly.

For docker the server configuration is defined in docker_environment.  Please make a copy
of docker_environment.template and name it docker_environment and update any settings/configurations
as needed.

## App Config

Update the config/config.yaml accordingly.  Any settings like DB credentials should 
match the values you set in your docker_environment.

Please copy the responses to responses/responses.xlsx and run the paser.py.

The results will be saved to the postgres database.



