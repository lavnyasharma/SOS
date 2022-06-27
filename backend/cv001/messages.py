"""
api responses messages
"""


"""
sucess messages
"""
SUCCESS = 'success'


"""
for user
"""
USER_NOT_FOUND = 'user not found'
USER_ALREADY_EXISTS = 'a user is already registered on this number'
ACCOUNT_CREATED = 'account successfully created'
UPDATED = 'data updated'
INVALID_PHONE_NUMBER = 'invalid phone number'
ADDRESS_STORED = 'address saved sucessfully'


"""
for email
"""
EMAIL_CONFIRMED = 'email is confirmed'
EMAIL_TOKEN_EXPIRED = 'verification token expired'
PASSWORD_VERIFICATION_LINK_SENT_EMAIL = 'a verification link has been send to your email account &&email&&xxx'

"""
for otp
"""
OTP_SENT = 'an otp has been send to this number'
OTP_INVALID = 'invalid otp'
OTP_CONF = 'otp confirmed'

"""
for token
"""
TOKEN_NOT_FOUND = 'token not found'
TOKEN_VALID = 'token is valid'
TOKEN_INVALID = 'token is invalid'


"""
for password
"""
PASSWORD_CHANGED = 'password changed'
PASSWORD_SET = 'password set'
PASSWORD_TOKEN_INVALID = 'password token invalid or expired'
INCORRECT_PASSWORD = 'password incorrect'
"""
error messages 
"""


UNABLE_TO_PROCESS = 'we are unable to process your request at this moment'
SOMTHING_WENT_WRONG = 'somthing went wrong'


"""
for phone number
"""
PASSWORD_VERIFICATION_LINK_SENT_PHONE = 'a verification link send to your registred Phone number ending with &&phone&&'



"""
FOR SPECIALIZATIONS 
"""
SPECIALIZATION_ADDED = 'Specialization added'