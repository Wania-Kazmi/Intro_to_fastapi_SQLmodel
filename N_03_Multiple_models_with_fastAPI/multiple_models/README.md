# Multiple Models with FastAPI

- We have been using the same Hero model to declare the schema of the data we receive in the API, the table model in the database, and the schema of the data we send back in responses which is not good approach.
- In our previous code, client can send an id in the JSON body of the request which means client could try to use the same ID that already exists in the database for another hero.
- We want that client can only send name, secret_name and age, and ID is generated automatically by the DB

# Check the API request schema through swagger UI:

- Schema tell us that required fields are name and secret_name. ID and age is optional
- The ID is optional because it could be None in memory until we save it in the database and we finally get the actual ID.
- But in the responses, we always send a model from the database, so it always has an ID. So the id in the responses can be declared as required.

# So Why is it Important to Have Required IDs

- Otherwise developers using those clients in their languages would have to be checking all the time in all their code if the id is not None before using it anywhere. That's a lot of unnecessary checks and unnecessary code that could have been saved by declaring the schema properly.
- It would be a lot simpler for that code to know that the id from a response is required and will always have a value

So when recieving and response back data id requirement is different. When we recieve data from client we really don't need an ID but when we response back data it is required. So for that we have multiple models

# Multiple Hero Schemas:

## Hero Model - declares data in the database

- id, optional on creation, required on database
- name, required
- secret_name, required
- age, optional

## HeroCreate - Data recieve from client when creating a new Hero

Here id will be created automatically by the database

- name, required
- secret_name, required
- age, optional

## HeroRead - response that will read by client

Here id is annotated with id: int, instead of id: Optional[int], to make it clear that it is required in responses read from the clients:
* id, required
* name, required
* secret_name, required
* age, optional

## Note: 
This filtering could be very important and could be a very good security feature, for example, to make sure you filter private data, hashed passwords, etc.
