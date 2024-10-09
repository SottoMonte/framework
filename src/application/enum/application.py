from enum import Enum

class INTERFACE(Enum):
    API = 1
    CLI = 2
    GUI = 3

class PLATFORM(Enum):
    WEB = 1
    NATIVE = 2

class TARGET(Enum):
    MOBILE = 1
    BROWSER = 2
    DESKTOP = 3
    SERVER = 4

class TYPE(Enum):
    INTERPRETED = 1
    COMPILED = 2
    HYBRID = 3

class LANGUAGES(Enum):
    PHP = 1
    PYTHON = 2
    RUST = 3
    C = 4
    JAVASCRIPT = 5
    GO = 6

class DATABASE(Enum):
    SQL = 1

class FRAMEWORK(Enum):
    FLUTTER = 1
    GTK4 = 2
    LARAVEL = 3
    PANDA = 4

#INTERFACE = {'API':'API','CLI':'CLI','GUI':'GUI'}
#PLATFORM = {'WEB':'WEB','NATIVE':'NATIVE'}
#TARGET = {'MOBILE':'MOBILE','BROWSER':'BROWSER','DESKTOP':'DESKTOP','SERVER':'SERVER'}
#TYPE = {'INTERPRETED':'INTERPRETED', 'COMPILED':'COMPILED', 'HYBRID':'HYBRID'}
#LANGUAGES = {'PHP','PYTHON','RUST','SQL','C','JAVASCRIPT','GO'}
#FRAMEWORK = {'FLUTTER','GTK4','LARAVEL','PANDA'}