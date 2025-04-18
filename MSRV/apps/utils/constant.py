from enum import Enum


class AppStatus(Enum):
    FALSE = "FALSE", 400, "FALSE"
    TRUE = "TRUE", 200, "TRUE"

    USER_IS_ACTIVE = "USER_IS_ACTIVE", 200, "User is active."
    REGISTER_USER_SUCCESS = 'REGISTER_USER_SUCCESS', 200, "Register user successfully, please check your email."
    IMPORT_VIDEO_SUCCESS = 'IMPORT_VIDEO_SUCCESS', 200, "Video imported successfully."

    EMAIL_FULLNAME_NOT_FOUND = "EMAIL_FULLNAME_NOT_FOUND", 400, "Email or name not found"
    EMAIL_ALREADY_EXIST = "EMAIL_ALREADY_EXIST", 400, "Email already exist."
    REGISTER_USER_FAIL = "REGISTER_USER_FAIL", 400, "Register user failed."
    TOKEN_INVALID = "TOKEN_INVALID", 400, "The token is invalid or expired."
    TOKEN_IS_INCORRECT = "TOKEN_IS_INCORRECT", 400, "The token is incorrect."
    CSV_FILE_NOT_FOUND = "CSV_FILE_NOT_FOUND", 400, "The CSV file not found."
    REGISTER_SCIENTIFIC_RESEARCH_FAIL = "REGISTER_SCIENTIFIC_RESEARCH_FAIL", 400, "The registration scientific research failed."
    FILE_INVALID = "FILE_INVALID", 400, "The file is invalid."


    USER_NOT_EXIST = "USER_NOT_EXIST", 404, "User does not exist."
    USER_NOT_FORBIDDEN = "USER_NOT_FORBIDDEN", 403, "User not forbidden"
    SCIENTIFIC_RESEARCH_PERMISSION_DENIED = "SCIENTIFIC_RESEARCH_PERMISSION_DENIED", 403, "User does not have permission for this scientific research."

    @property
    def message(self):
        return {
            'message': str(self.value[2]),
            'code': str(self.value[1]),
            'data': 'success' if self.value[1] in [200, 201] else 'failed'
        }
