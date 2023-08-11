# Eat me Up

This is an app  for manaing your macros and recipes. 

You need Docker to run this application.


# Some functionalities: 
Create Recipes
Make shopping lists for chosen recipes
Share your recipes

# To run the project
run this command: sudo docker-compose -f docker-compose-deploy.yml up --build

# To add a superuser:
sudo docker exec -it eat_me_next_tri_app_1 python manage.py createsuperuser




