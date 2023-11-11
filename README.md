# AirBnB_clone
Airbnb clone project, first web app
This console project is an abstraction layer for our backend.

In this first part of the project, we store and manipulate objects in a file storage

The structure of the project is as follows:
* A base model from which all other models inherit, ensuring that there is a unique uuid for all objects that inherited from this base model
* A console using the cmd module to handle CRUD operations: create, update (show), update, delete (destroy)
* Next: web statics

## Commands supported by the console
* help
* quit
* EOF (or CTRL + D)
* create
* show
* destroy
* all
* update
* <class_name>.all()
* <class_name>.count()
* <class_name>.update(...) with dictionary support
