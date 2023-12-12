# CRISPR BACKEND API
## To start the project
If already have the conda environment and requirements ready for the server, go to step 5; otherwise, start from step 1
1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) with python version 3.10	
2. Create the environment from the `environment.yml` file:
    ```
    conda env create -f environment.yml
    ```
3. Verify that the new environment was installed correctly:
    ```
    conda env list
    ```
4. Activate the environment: 
   ```
   conda activate crisprBack
   ```

5. Install python requirements
   ```
   pip install -r requirements.txt
   ```
   
6. Copy env-example to file .env
   ```
   cp env-example .env
   ```
7. Config values into .env file

8. Run the server
   ```
   flask run
   ```       
## To add tables
To create tables in database
1. Run flask shell
   ```
   flask shell
   ```
2. Import the database instance 
   ```
   from api.db_models import db
   ```
3. Run the `create_all()` method to create related tables based on the model specified at `api.db_models.`
   ```
   db.create_all()
   ```
## To insert data into tables
1. Run flask shell
   ```
   flask shell
   ```
2. Import the insert data function
   ```
   from api.utils.update import insert_data_into_db
   ```
3. Run the function
   ```
   insert_data_into_db()
   ```
## Deploy to production
Deploy to Production
1. Follow instructions in [Deploy to production a Flask Aplication](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/) 
   
