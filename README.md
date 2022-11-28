# Run this project
1) Install all dependencies:
    > pip install -r requirements.txt
   - I encourage you install all dependencies in virtual environments.
2) Run server:
    - First, you need set two variable environments, in linux os, type:
    > export FLASK_APP=run_dev_app.py

    > export FLASK_ENV=development
   
   - Then, make sure you have MongoDB running at *mongodb://localhost:27017* or you must config at DevConfig class at url-tracking/core/settings.py

   - Next, run app:
   > flask run

# Docs
- Docs page: after run app, go to *http://127.0.0.1:5000/docs*