# gmail-cli
> This python project enables the user to access their Gmail inbox from CLI.
> Users can grant access to their inbox with read and modify access. 
> Once this is done, the project will be able to import the recent 100 mails to local database.
> You can perform actions on the inbox by specifying the same in handlers/rules.py


**How to set-up ?**
1. git clone https://github.com/sibinms/gmail-cli.git
2. cd gmail-cli
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. Add the Oauth2 credentials.json file at the root of the project by creating a new Google application
7. python3 main.py

![](/Users/sibin/Desktop/Screenshot 2024-03-24 at 11.40.08 AM.png)