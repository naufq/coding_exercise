# Coding Exercise

## Env Information  
- Including venv requirements in a file `requirements.txt`
- Elasticsearch service is running on localhost without basic auth or tls encryption
- ES Version `7.12.1`  
- Python version `3.8.5`  
- Ubuntu version `20.04.2 LTS (focal)`  
- Ansible version `2.10.9`  
- Working directory will be the `coding_exercise` folder

## Test 1 - Service status script, flask webservice, and elasticsearch

### a) Check status and write to file

#### Filename `status_check.py`

#### Notes
- Service names
  - apache2 (using apache2 instead of httpd to check and store the status as the test vm is ubuntu)
  - rabbitmq-server
  - postgresql    
- Assuming that the client only needs to store the most recent service status to ascertain current app health
- It is assumed that this script will be scheduled on the concerning machines. Hence, it will run once, write the status to file, execute API to index the results into ES, and terminate.
- Service names are hardcoded into the file

### b) Web service to write and read app status
#### Filename `app.py`

#### Notes
- Assuming that the client only needs to store the most recent service status to ascertain current app health
- Assuming that the ES index storing the service status does not contain any other records  
- Run app via command line using `flask run --cert=adhoc`
- The json_payloads folder will be created in the working dir  

#### Examples

`curl -k -XPOST https://localhost:5000/add
{"msg":"Service status stored","success":true}`

`curl -k -XGET https://localhost:5000/healthcheck
{"app_status":"UP","success":true}`

`curl -k -XGET https://localhost:5000/healthcheck/apache2
{"service_status":"UP","success":true}`

## Test 2 - Ansible

### Files and Folders of Concern 
#### `roles/` `services_play.yml`

### Notes  

- variable name being used is `act` as action is a reserved var
- valid `act` values are
  - verify_install
  - check_disk _(client can specify the mount that needs to be checked - defaults to /)_
  - check_status
- sample commands
  - `ansible-playbook services_play.yml -i inventory.ini -e "act=verify_install"` _(root required to install)_  
  - `ansible-playbook services_play.yml -i inventory.ini -e "act=check_disk sender_address=mymail@domain.com password=my_pass recipient_address=receivermail@domain.com"`  
  - `ansible-playbook services_play.yml -i inventory.ini -e "act=check_status"` _(assumes status_check script updates es with latest status at a 'near-real-time' rate)_  


## Test 3 - Dataframe script


### File 
#### `data_filter.py`

### Notes
- Average price of property per square foot is taken as 220 USD for the entire state of California
- Data file should be present in the working directory _(i.e. the coding_exercise folder)_
- 0 sqft rows will not be counted - considered erroneous rows
