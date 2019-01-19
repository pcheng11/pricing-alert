import uuid
from src.common.database import Database
import src.models.users.errors as UserErrors
from src.common.utils import Utils
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User():
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
    
    def __repr__(self):
        return "<User {}>".format(self.email)
    
    @staticmethod #no specific user
    def is_login_valid(email, password):
        """
        This method verifies that an email/pw combo is valid or not
        :param email: User email
        :param password: A sha512 hashed pw
        :return True/False
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {'email':email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        Register a user using email and password(sha-512)
        :param email: user email
        :param password: sha512 pw
        :return: ture/false
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {'email':email})

        if user_data is not None:
            # already exists
            raise UserErrors.UserAlreadyResiteredError("The email you used is already exists")

        if not Utils.email_is_valid(email):
            # email not right
            raise UserErrors.InvalidEmailError("The email does not have the right format")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email":email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)