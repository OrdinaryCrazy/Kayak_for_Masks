# Kayak_for_Masks
# Step 1. 
Set up Python Django environment using environment.yml file (Linux or Window). You can use any virtual Environment, such as Conda. 

 - conda env create -f environment.yml
 - 
# Step 2.
Change the Json file path in the view.py to your local path 

# Step 3.
Migrations (Propagating changes you make every time you make changes on models) 

 - python manage.py makemigrations
 - python manage.py migrate

# Step 4.
Run on your local sever
- python manage.py runserver
 
# Step 5. 
The route for our web is masklink/ 
