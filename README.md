# CRISPR BACKEND API
## To start the project
### - Configurate the environment

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
### - Implement BLAST+

1. Install BLAST+ from [NCBI](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)

2. Make sure that you can execute BLAST+ commands from the terminal, for example:
   ```
   blastn -help
   ```
### - Implement CRISPRidentify

1. Download CRISPRidentify from [CRISPRidentify](https://github.com/BackofenLab/CRISPRidentify) and place it in the root folder of the project

2. Follow the instructions to install CRISPRidentify (you will need to install some dependencies and a new conda environment)

3. In the laborotory_local.py in the line 167 change the name of the conda environment to the one you created for CRISPRidentify
   ```
   conda activate crispr_identify_env
   ```
4. Execute the environment and make sure that you can execute CRISPRidentify commands from the terminal, for example:
   ```
   python CRISPRidentify.py -h
   ```

### - Adding CRISPRCasIdentifier

Download CRISPRCasIdentifier following the instructions in the section "Additional preparations" from [CRISPRidentify](https://github.com/BackofenLab/CRISPRidentify?tab=readme-ov-file) (Taking into account that the folder of CRISPRidentify is in the root folder of the project)


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

## To drop a schema and create a new one
1. Run flask shell
   ```
   flask shell
   ```
2. Import the database instance 
   ```
   from api.db_models import db
   ```
3. Run the `drop_all()` method to drop all tables in the database
   ```
   db.drop_all()
   ```
4. Run the `create_all()` method to create related tables based on the model specified at `api.db_models.`
   ```
   db.create_all()
   ```

## How to add data or modify BLAST+ databases

The BLAST+ databases are located in the `api/dataDB` folder. To add a new database, follow these steps:

1. Copy the content of the desired .fasta file into the .fasta file of the target database, e.g. phylotypes_db.fasta (All sequences must be in the same file to create a BLAST database)
   ```
   cat new_file.fasta >> phylotypes_db.fasta
   ```
2. Create a new BLAST database, for example:
   ```
   makeblastdb -in phylotypes_db.fasta -dbtype nucl -parse_seqids -out phylotypes_db
   ```

If you change the name of the database, you must also change the name of the database in the `api/services/query_services/laboratory_local.py` file in the last two functions of the file respectively.

## Deploy to production
Deploy to Production
1. Follow instructions in [Deploy to production a Flask Application](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/) 
   
