# Rain Api

Rain Api Cli tool enables you to download a full pagination end point from Your Api. with 3 simple steps you can copy your data to another database. Use 'rain_api --help' to see full commands list 


### Prerequisites 

    1. Isntall python
    2. Make sure you have pip installed 
        '$ pip -V' 
    
### Development 
    3. install pipenv `$ pip install pipenv`
    6. inside the folder `$ pipenv install`
    you can run dev mode in this folder `$ pipenv run main`
    Note:
    5. to add new package to setup `pipenv lock && pipenv run pip freeze > requirements.txt`
    
### Production
   
    '$ pip install git-path/rain_api'
    
   check with 
   
    '$ pip install rain_api'

# How To Use
   
   Install Script: '$ pip install git-path/rain_api'
    
    1. Build a folder for the custom api setup  `$ rain_api create --name="API_NAME" --url="API_URL"`
    2. Download data from api `rain_api start --name="API_NAME"`
    3. Import data to sql `rain_api to-sql --name="API_NAME"`
    4. Create html templates by id `rain_api to-html --name="API_NAME"`

    Enjoy!
