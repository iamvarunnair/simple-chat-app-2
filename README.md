# apollo_20200804

Sample multiuser chat application with messages stored in DB using django, channels 2 and redis.

Step 1: run py manage.py migrate.
Step 2: Download and install redis server for windows.
Step 3: Run py manage.py createsuperuser and create a super user and login to django admin (localhost:8000/admin/)
Step 4: Fill all status tables with two values, 'Active' and 'Inactive' and add dummy user names with status 1 (Active).
Step 5: Open localhost:8000/chat/login/ in multple broswer sessions and chat. View stored messages in djnago admin.
