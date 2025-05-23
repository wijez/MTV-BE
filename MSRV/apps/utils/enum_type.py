from enum import Enum


class EnumType(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))

    def __str__(self):
        return self.value

class SystemRoleEnum(EnumType):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'

class TypeEmailEnum(EnumType):
    REGISTER = "REGISTER"
    RESET_PASSWORD = "RESET_PASSWORD"
    REGISTER_FROM_ADMIN = "REGISTER_FROM_ADMIN"

class DegreeEnum(EnumType):
    TS = 'TS'
    THS = 'THS'
    PGS = 'PGS'
    GS = 'GS'
    UN_TS_III = 'UN_TS_III'
    TS_III = 'TS_III'
    UN_TS_II = 'UN_TS_II'
    TS_II = 'TS_II'

class DepartmentEnum(EnumType):
    HR = "HR"
    IT = "IT"
    LEGAL = "LEGAL"
    SALES = "SALES"
    TOURISM = "TOURISM"
    FINANCE = "FINANCE"
    MARKETING = "MARKETING"
    OPERATIONS = "OPERATIONS"
    ENGINEERING = "ENGINEERING"
    ARCHITECTURE = "ARCHITECTURE"
    ADMINISTRATION = "ADMINISTRATION"
    GRAPHIC_DESIGN = "GRAPHIC_DESIGN"
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE"
    FOREIGN_LANGUAGES = "FOREIGN_LANGUAGES"
    INFORMATION_TECHNOLOGY = "INFORMATION_TECHNOLOGY"

class GroupEnum(EnumType):
    RESEARCH_PROJECTS = "RESEARCH_PROJECTS" #"Nhóm đề tài NCKH"
    ARTICLES_BOOKS = "ARTICLES_BOOKS" #"Nhóm bài viết, sách"
    STUDENT_GUIDANCE = "STUDENT_GUIDANCE" #"Nhóm hướng dẫn sinh viên"
    WORKS_PUBLICATIONS = "WORKS_PUBLICATIONS" #"Nhóm công trình, tác phẩm GV"
    OTHER_ACTIVITIES = "OTHER_ACTIVITIES" #"Nhóm hoạt động khác"

class StatusSREnum(EnumType):
    OPEN = "OPEN"
    PROCESS = "PROCESS"
    COMPLETE = "COMPLETE"
    NOT_COMPLETED ="NOT_COMPLETED"
    DELETED ="DELETED"

class StatusSPEnum(EnumType):
    OPEN = "OPEN"
    PASSED = "PASSED"
    NOT_PASSED = "NOT_PASSED"
    CANCELLED = "CANCELLED"

class TypeFileEnum(EnumType):
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"

class FolderEnum(EnumType):
    AVATAR = "AVATAR"
    BANNER = "BANNER"
    DATA ="DATA"
