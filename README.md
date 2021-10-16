![Logo](https://github.com/maticha84/oc_p9_repository/blob/master/litreview/litapp/static/litapp/img/logo_small.png) 
#LitReview project
## __*book reviews*__
___
___
### Description
___
This application allows you to share opinions on literary works. 

It is possible to create a user account to access the application and then request reviews. 

Finally, it is also possible to share reviews and respond to requests for reviews from people to whom the user is subscribed. 

It is possible to subscribe to a user by entering their username.
___
### Installation
___
At first, you have to install python3 (I use the 3.9.6 version). You can find on the official site Python your version for Windows /Linux/ Mac.

Then you need to install a new environment for running the application, containing the packages included in the file requirement.txt .To do this, please follow the instructions below:

Create a virtual environment at the root of the project, using the command python -m venv env. Then, activate this environment :

---
    Windows: venv\Scripts\activate.bat
---
    Linux & Mac: source venv/Scripts/activate
---
After that, install the requirement.txt with using this command : pip install -r requirements.txt

Then, go to the project folder, named litreview, and run the following command: 

---
    ../litreview> manage.py runserver
---

It will be start the server to this address : [127.0.0.1:8080](http://127.0.0.1:8080)

The administration is done from the page [content](http://127.0.0.1:8080/content)
Superuser for administration by default: 

`login = adminuser - mdp = Mdp@dminUs3r!`. 

This password must be changed the first time you log in.
___
### Instructions for use
***
On the start page, you can choose the appilcation you want to use.  For this project, only one application exists. 
Click on the `litapp` button to enter the user interface of the application.
___
#### _* Login view *_
___
This is the page that is displayed as long as no user is logged in. 

From this page you can : 
- Create a new account
- Log in with an existing account. 

_*In this project, no request was made to handle password reset or change. This feature is not implemented 
at this time.*_

___
#### _* Create new account *_
___

If you click the button `s'inscrire`, a new page is displayed, allowing you to create a new user account.
You can then enter a user name, a password and a confirmation password. 

If the username is already in use, the password is not complex enough and/or the password and its confirmation do not 
match, an error message is displayed. 

In the opposite case, a message displays the success of the account creation, and you can return to the login 
page to log in.
___
#### _* Home view - Flow_*
___

On login, the first page that appears is the `Flux` page.  On this page appear : 
- your tickets and reviews 
- the tickets and reviews of people you follow
- a `Demander une cirtique` button
- a `Créer une critique` button

On your tickets and those of the people you follow, if no reviews have been posted, you can post a review by clicking on
the `Créer une critique` button.
1. New ticket view

When you click on the `Demander une critique` button, a new page ticket create is displayed 

You must then fill in a Title, a Description and you can also upload an image to illustrate your review request. 
Once you have completed the form, click on the `Envoyer` button to post your request.

You will then be directly redirected to the `Posts` page, which allows you to manage your publications 
2. New review view

When you click on the `Créer une critique` button, a new page review create is displayed 

You must then fill in a Title, a Description and you can also upload an image to illustrate your review request. 
And after, you have to give a rate, with a Headline and a comment for publish your review.

Once you have completed the form, click on the `Envoyer` button to post your request.

You will then be directly redirected to the `Posts` page, which allows you to manage your publications 

3. New review on an existing ticket

When you click on the `Créer une critique` button, a new page review create is displayed 

The ticket is displayed before the review form.
You have to give a rate, with a Headline and a comment for publish your review.

Once you have completed the form, click on the `Envoyer` button to post your request.

You will then be directly redirected to the `Posts` page, which allows you to manage your publications 

