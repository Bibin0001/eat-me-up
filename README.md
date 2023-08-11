<h1>Eatme</h1> 
<p>A macromanagement app. You can create ingredients, recipes, eating plans and shopping lists. The project uses Django</p>

<h2>Getting started:</h2>

<h3>1. Clone this repository e.g.</h3>

    git clone https://github.com/Bibin0001/eat-me-up.git

<h3>2. Navigate to the app folder</h3>
    
    cd eat-me-up

<h3>3. Run the docker-compose files</h3>

    sudo docker-compose -f docker-compose-deploy.yml up --build

<h3>4. Create a superuser</h3>

    sudo docker exec -it eat_me_next_tri_app_1 python manage.py createsuperuser
<h3>5. The app is running on 127.0.0.1:8080</h3>
  
