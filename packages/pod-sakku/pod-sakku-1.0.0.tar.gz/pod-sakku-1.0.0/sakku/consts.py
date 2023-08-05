# coding=utf-8


class Topics:
    def __init__(self):
        pass

    """دریافت همه تغییرات برنامه"""
    ALL = "ALL"

    """دریافت تغییرات مربوط به دسترسی اعضا به برنامه"""
    MEMBER = "MEMBER"

    """حذف برنامه"""
    DELETE = "DELETE"

    """اجرا و توقف برنامه"""
    RUN_STATE = "RUN_STATE"

    """عمل push در کد پروژه"""
    PUSH = "PUSH"

    """عمل pull در کد پروژه"""
    PULL = "PULL"

    """تغییرات انجام‌شده در گیت برنامه"""
    GIT = "GIT"

    """تغییرات انجام‌شده در داکر برنامه"""
    DOCKER = "DOCKER"

    """هرگونه تغییر در موضوعات برنامه"""
    ISSUE = "ISSUE"


class CollaboratorAccessLevel:
    def __init__(self):
        pass

    """تنها قادر به مشاهده اطلاعات برنامه، تنظیمات، منابع و لاگ آن است."""
    VIEW = "VIEW"

    """علاوه بر قابلیت‌های سطح VIEW، اجازه تغییر وضعیت برنامه و تغییر تنظیمات آن را نیز دارد، اما قادر به حذف برنامه 
    نیست. """
    MODIFY = "MODIFY"

    """همانند ادمین برنامه، دسترسی کامل دارد."""
    MODERATE = "MODERATE"


class ImageRegistryAccess:
    def __init__(self):
        pass

    """دسترسی کامل"""
    ALL = "ALL"

    """بدون دسترسی"""
    NONE = "NONE"

    """دسترسی به push"""
    PUSH = "PUSH"

    """دسترسی به pull"""
    PULL = "PULL"


class DeployType:
    def __init__(self):
        pass

    APP = "APP"
    CODE = "CODE"
    DOCKER_IMAGE = "DOCKER_IMAGE"


class ScalingMode:
    def __init__(self):
        pass

    OFF = "OFF"
    CPU = "CPU"
    MEM = "MEM"
    AND = "AND"
    OR = "OR"


class FeedbackType:
    def __init__(self):
        pass

    IMPROVEMENT = "IMPOROVEMENT"
    NEW_FUTURE = "NEW_FUTURE"
    PROBLEM = "PROBLEM",
    OTHER = "OTHER"


class MetaDataScope:
    def __init__(self):
        pass

    APP = "APP"
    ENV = "ENV"
    CONFIG = "CONFIG"


class RecordType:
    def __index__(self):
        pass

    SOA = "SOA"
    A = "A"
    AAAA = "AAAA"
    CAA = "CAA"
    CNAME = "CNAME"
    MX = "MX"
    PTR = "PTR"
    SPF = "SPF"
    SRV = "SRV"
    TXT = "TXT"
    LOC = "LOC"
    NS = "NS"
