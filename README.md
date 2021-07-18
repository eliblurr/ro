**_Set Up_**:
> 1. Create a virtual environment
2. Activate the virtual environment
3. Open shell/terminal in project home directory
4. Rename env.example file to .emv and edit accordingly
5. Install application requirements with ***python3 -m pip install -r requirements.txt***
6. Run application with ***uvicorn main:app --reload***

**_Database Configuration_**:
> The database connection url is to be assigned to SQLALCHEMY_DATABASE_URL in your .env file
> Remove ***connect_args={"check_same_thread": False}*** in the database.py file if you are not using sqlite

**_Api Documentation_**:
> See **/doc** or **/redoc** to see api documentation