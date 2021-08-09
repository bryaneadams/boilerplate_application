import jwt

class UserCredentials():
    def __init__(self, user_data, refresh_token, app_id):
        self.user_email = user_data['email']
        self.username = user_data['username']
        
        '''
        The token contains the user's roles by application in keycloak
        '''
        self.auths = jwt.decode(refresh_token, algorithms=['HS256'], options={'verify_signature':False})

        print(f"### Auths {self.auths}", flush = True)

        self.app_user = True
        self.app_admin = True
    
    def is_app_user(self):
        return True

    def is_app_admin(self):
        return True