# Response Model:

## Swagger UI:

- Swagger UI can read a big JSON file.
- This JSON file contains all the information about how an API works, including the different types of data it uses (like what a user's information looks like or how a product is described).
- This JSON file follows a standard called OpenAPI.

<b>Here we will discuss the schema of the responses our app sends back. </b>

- Without defining a response model we see "Successful Response" with a code 200, but we have no idea how the response data would look like.
- FastAPI will do automatic data validation and filtering of the response with the response_model.

* The most visible advantage of using the response_model is that it shows up in the API docs UI
* The schemas are defined in using a standard, there are many tools that can take advantage of this.
