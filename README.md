# Kayak_for_Masks
# Set up Python Django environment using environment.yml file (Linux or Window). You can use any virtual Environment, such as Conda. 
conda env create -f environment.yml
# Change the Json file path in the view.py to your local path 
# Migrations (Propagating changes you make every time you make changes on models) 
 python manage.py makemigrations
 python manage.py migrate 
# Run on your local sever
 python manage.py runserver 
