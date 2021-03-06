import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """A class that extends the flask_restful Resource class. Allows the user to register for 
    access
    
    Static Attributes:
        parser (obj): Instance of the flask_restful RequestParser class. Allows for validations on
            request bodies from HTTP requests (specifically in JSON)

    Methods:
        post: Creates a new user. Uses the JSON data in the HTTP request body, along with the
            parser static attribute to validate that username and password data are present. If so,
            the new user is added to the sqlite DB, otherwise the validation errors are returned.
    """

    # Request body parser
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'Username cannot be left blank!'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'Password cannot be left blank!'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        # Duplicate username check
        if UserModel.find_by_username(data['username']):
            return {"message": "Username exists, please choose a different username."}, 400

        # dictionary unpacking to fit user model parameters
        # since teh parser is being utilized, you know that the data
        # WILL ALWAYS have the appropirate data to me the UserModel
        # parameters
        user = UserModel(**data) 
        user.save_to_db()

        return {"message": "User created successfully."}, 201