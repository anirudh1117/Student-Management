import datetime
import re
from uuid import UUID
from django.utils.crypto import get_random_string
from . import constants
from .exceptions import SchoolAuthorizationError, SchoolSessionAuthorizationError
from school.models import School


def unix_time_millis():
    return datetime.datetime.now().timestamp() * 1000

def convert_date_time_to_unix_time_millis(dateTime):
    return dateTime.timestamp() * 1000

def convert_date_to_unix_time_millis(date):
    """
    Converts a date object to Unix epoch time, assuming the time is midnight UTC.

    Args:
    - date (datetime.date): The date object to convert.

    Returns:
    - int: The Unix epoch time in seconds.
    """
    # Create a datetime object from the date object at midnight
    dt = datetime.datetime.combine(date, datetime.time.min)
    
    # Make the datetime object timezone-aware, assuming UTC
    dt = dt.replace(tzinfo=datetime.timezone.utc)

    # Convert to epoch time
    epoch_time = int(dt.timestamp())
    return epoch_time

def convert_unix_time_millis_to_date(epoch_time):
    """
    Converts an epoch time (Unix timestamp) to a Python date object.

    Args:
    - epoch_time (int): Epoch time in seconds.

    Returns:
    - datetime.date: The corresponding date object.
    """
    # Convert epoch time to a datetime object
    epoch_time = int(epoch_time)
    dt = datetime.datetime.utcfromtimestamp(epoch_time)
    
    # Extract the date part and return
    return dt.date()


def convert_unix_time_millis_to_date_time(unixTime):
    unixTime = int(unixTime)
    return datetime.datetime.fromtimestamp(unixTime)

def is_valid_uuid(uuid):
    try:
        print(uuid)
        uuid_obj = UUID(str(uuid), version=4)
        return True
    except ValueError:
        print('2')
        return False


def string_to_uuid(uuidValue):
    return UUID(str(uuidValue))


def generate_password(len,allowed_chars):
    return str(get_random_string(length=len, allowed_chars=allowed_chars))

def get_Choices(dataList):
    l = list()
    for i in dataList:
        tup = (i,i.upper())
        l.append(tup)
    return tuple(l)

def slugify(s):
  s = s.upper().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

def common_error_message(message):
    context = {
        "detail" : message
    }
    return context


def check_school_and_current_session(request):
    if request.user:
        school = request.user.school
        if school:
            current_session = school.current_session
            if current_session:
                return school,current_session
            else:
                raise SchoolSessionAuthorizationError()
        else:
            raise SchoolAuthorizationError()
        
def get_school_list():
    schools = School.objects.all()
    l = list()
    l.append((None,'---'))
    for schoolObj in schools:
        choice = schoolObj.name + ' - ' + schoolObj.city + ' - ' + schoolObj.email
        t = (schoolObj.id, choice)
        l.append(t)
    
    return l


def get_initials_from_string(name):
    if len(name) == 0:
        return ''
    
    name = name.replace('.', ' ')
    initial_list = re.split(" ", name)
    initial_name = ''

    for word in initial_list:
        if word != "" or len(word) > 0:
            initial_name = initial_name + word[0].upper()

    print(initial_name)

    return initial_name



