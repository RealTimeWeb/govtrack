from __future__ import print_function
import sys
import json

HEADER = {'User-Agent': 'RealTimeWeb GovTrack library for educational purposes'}
PYTHON_3 = sys.version_info >= (3, 0)

if PYTHON_3:
    import urllib.error
    import urllib.request as request
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus

# Auxilary


def _parse_float(value, default=0.0):
    """
    Attempt to cast *value* into a float, returning *default* if it fails.
    """
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _iteritems(_dict):
    """
    Internal method to factor-out Py2-to-3 differences in dictionary item
    iterator methods

    :param dict _dict: the dictionary to parse
    :returns: the iterable dictionary
    """
    if PYTHON_3:
        return _dict.items()
    else:
        return _dict.iteritems()


def _urlencode(query, params):
    """
    Internal method to combine the url and params into a single url string.

    :param str query: the base url to query
    :param dict params: the parameters to send to the url
    :returns: a *str* of the full url
    """
    return query + '?' + '&'.join(
        key + '=' + quote_plus(str(value)) for key, value in _iteritems(params))


def _get(url):
    """
    Internal method to convert a URL into it's response (a *str*).

    :param str url: the url to request a response from
    :returns: the *str* response
    """
    if PYTHON_3:
        req = request.Request(url, headers=HEADER)
        response = request.urlopen(req)
        return response.read().decode('utf-8')
    else:
        req = urllib2.Request(url, headers=HEADER)
        response = urllib2.urlopen(req)
        return response.read()


def _recursively_convert_unicode_to_str(input):
    """
    Force the given input to only use `str` instead of `bytes` or `unicode`.

    This works even if the input is a dict, list, or a string.

    :params input: The bytes/unicode input
    :returns str: The input converted to a `str`
    """
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(
            key): _recursively_convert_unicode_to_str(value) for key, value in
                input.items()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in
                input]
    elif not PYTHON_3:
        return input.encode('utf-8')
    elif PYTHON_3 and isinstance(input, str):
        return str(input.encode('ascii', 'replace').decode('ascii'))
    else:
        return input


# Cache

_CACHE = {}
_CACHE_COUNTER = {}
_EDITABLE = False
_CONNECTED = True
_PATTERN = "repeat"


def _start_editing(pattern="repeat"):
    """
    Start adding seen entries to the cache. So, every time that you make a request,
    it will be saved to the cache. You must :ref:`_save_cache` to save the
    newly edited cache to disk, though!
    """
    global _EDITABLE, _PATTERN
    _EDITABLE = True
    _PATTERN = pattern


def _stop_editing():
    """
    Stop adding seen entries to the cache.
    """
    global _EDITABLE
    _EDITABLE = False


def _add_to_cache(key, value):
    """
    Internal method to add a new key-value to the local cache.
    :param str key: The new url to add to the cache
    :param str value: The HTTP response for this key.
    :returns: void
    """
    if key in _CACHE:
        _CACHE[key].append(value)
    else:
        _CACHE[key] = [_PATTERN, value]
        _CACHE_COUNTER[key] = 0


def _clear_key(key):
    """
    Internal method to remove a key from the local cache.
    :param str key: The url to remove from the cache
    """
    if key in _CACHE:
        del _CACHE[key]


def _save_cache(filename="cache.json"):
    """
    Internal method to save the cache in memory to a file, so that it can be used later.

    :param str filename: the location to store this at.
    """
    with open(filename, 'w') as f:
        json.dump({"data": _CACHE, "metadata": ""}, f)


def _lookup(key):
    """
    Internal method that looks up a key in the local cache.

    :param key: Get the value based on the key from the cache.
    :type key: string
    :returns: void
    """
    if key not in _CACHE:
        return ""
    if _CACHE_COUNTER[key] >= len(_CACHE[key][1:]):
        if _CACHE[key][0] == "empty":
            return ""
        elif _CACHE[key][0] == "repeat" and _CACHE[key][1:]:
            return _CACHE[key][-1]
        elif _CACHE[key][0] == "repeat":
            return ""
        else:
            _CACHE_COUNTER[key] = 1
    else:
        _CACHE_COUNTER[key] += 1
    if _CACHE[key]:
        return _CACHE[key][_CACHE_COUNTER[key]]
    else:
        return ""


def connect():
    """
    Connect to the online data source in order to get up-to-date information.

    :returns: void
    """
    global _CONNECTED
    _CONNECTED = True


def disconnect(filename="../src/cache.json"):
    """
    Connect to the local cache, so no internet connection is required.

    :returns: void
    """
    global _CONNECTED, _CACHE
    try:
        with open(filename, 'r') as f:
            _CACHE = _recursively_convert_unicode_to_str(json.load(f))['data']
    except (OSError, IOError) as e:
        raise GovTrackException(
            "The cache file '{}' was not found.".format(filename))
    for key in _CACHE.keys():
        _CACHE_COUNTER[key] = 0
    _CONNECTED = False


# Exceptions

class GovTrackException(Exception):
    pass


# Domain Objects

class Bill(object):

    """
    A Bill contains
    """

    def __init__(self, is_alive=None, is_current=None, title=None, number=None,
                 description=None, congress_session=None, introduced_date=None):

        """
        Creates a new bill

        :param is_alive: Denotes if the bill is alive
        :type is_alive: str
        :param is_current: Denotes if the bill is current
        :type is_current: str
        :param title: The title for the bill
        :type title: str
        :param number: The bill number
        :type number: str
        :param description: The description for the bill
        :type description: str
        :param congress_session: The congress session during which the bill was introduced
        :type congress_session: str
        :param introduced_date: The introduced date for the bill
        :type introduced_date: str

        :returns: Bill
        """

        self.is_alive = is_alive
        self.is_current = is_current
        self.title = title
        self.number = number
        self.description = description
        self.congress_session = congress_session
        self.introduced_date = introduced_date

    def __unicode__(self):
        string = """ <Bill {0} Number: {1}> """
        return string.format(self.title, self.number)

    def __repr__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def __str__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def _to_dict(self):
        return dict(is_alive=self.is_alive,
                    is_current=self.is_current,
                    title=self.title,
                    number=self.number,
                    description=self.description,
                    congress_session=self.congress_session,
                    introduced_date=self.introduced_date)

    @staticmethod
    def _from_json(json_data):
        """
        Creates a Bill from json data.

        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: PublicOfficial
        """

        try:
            bill = Bill(is_alive=json_data['is_alive'],
                            is_current=json_data['is_current'],
                            title=json_data['title'],
                            number=json_data['number'],
                            description=json_data['current_status_description'],
                            congress_session=json_data['congress'],
                            introduced_date=json_data['introduced_date'])


            return bill

        except KeyError:
            raise GovTrackException("The given information was incomplete.")


class PublicOfficial(object):
    """
    A PublicOfficial contains
    """

    def __init__(self, website=None, start_date=None, end_date=None, state=None,
                 title=None, name=None, leadership_title=None, district=None):

        """
        Creates a new PublicOfficial

        :param website: The Public Official's website
        :type website: str
        :param start_date: The Public Official's start date
        :type start_date: str
        :param end_date: The Public Official's end date
        :type end_date: str
        :param state: The Public Official's representing state
        :type state: str
        :param title: The Public Official's title
        :type title: str
        :param name: The Public Official's name
        :type name: str
        :param leadership_title: The Public Official's leadership title (Majority Whip, Minority Whip, etc.)
        :type leadership_title: str
        :param district: The Public Official's representing district
        :type district: float

        :returns: PublicOfficial
        """
        self.website = website
        self.start_date = start_date
        self.end_date = end_date
        self.state = state
        self.title = title
        self.name = name
        self.leadership_title = leadership_title
        self.district = district

    def __unicode__(self):
        string = """ <{0} Name: {1}> """
        return string.format(self.title, self.name)

    def __repr__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def __str__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def _to_dict(self):
        return dict(website=self.website,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    state=self.state,
                    title=self.title,
                    name=self.name,
                    leadership_title=self.leadership_title,
                    district=self.district)

    @staticmethod
    def _from_json(json_data):
        """
        Creates a PublicOfficial from json data.

        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: PublicOfficial
        """

        try:
            leadership_title = "" if json_data['leadership_title'] is None else json_data['leadership_title']
            district = "" if json_data['district'] is None else json_data['district']
            official = PublicOfficial(website=json_data['website'],
                                      start_date=json_data['startdate'],
                                      end_date=json_data['enddate'],
                                      state=json_data['state'],
                                      title=json_data['title_long'],
                                      name=json_data['person']['name'],
                                      leadership_title=leadership_title,
                                      district=district)

            return official

        except KeyError:
            raise GovTrackException("The given information was incomplete.")


# Service Methods


def _fetch_govtrack_info(params, element):
    """
    Internal method to form and query the server

    :param dict params: the parameters to pass to the server
    :returns: the JSON response object
    """
    from collections import OrderedDict

    baseurl = 'https://www.govtrack.us/api/v2/'

    baseurl += element
    ordered_dict = OrderedDict(sorted(_iteritems(params), key=lambda x:x[1], reverse=True))
    query = _urlencode(baseurl, ordered_dict)

    if PYTHON_3:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib.error.HTTPError:
            raise GovTrackException("Make sure you entered a valid query")
    else:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib2.HTTPError:
            raise GovTrackException("Make sure you entered a valid query")

    if not result:
        raise GovTrackException("There were no results")

    result = result.replace("// ", "")  # Remove Double Slashes
    result = " ".join(result.split())  # Remove Misc 1+ Spaces, Tabs, and New Lines

    try:
        if _CONNECTED and _EDITABLE:
            _add_to_cache(query, result)
        json_res = json.loads(result)
    except ValueError:
        raise GovTrackException("Internal Error")

    return json_res


def get_senators(query):
    """
    Forms and poses the query to get information from the database
    :param query: the values to retrieve
    :return: the JSON response
    """

    if not isinstance(query, str):
        raise GovTrackException("Please enter a valid query")

    q = {'role_type': "senator",
         'current': "True",
         'party': query}

    json_res = _fetch_govtrack_info(q, "role")
    json_list = json_res['objects']

    senators = []
    for json_dict in json_list:
        senator = PublicOfficial._from_json(json_dict)
        senators.append(senator._to_dict())

    return senators


def get_representatives(query):
    """
    Forms and poses the query to get information from the database
    :param query: the values to retrieve
    :return: the JSON response
    """

    if not isinstance(query, str):
        raise GovTrackException("Please enter a valid query")

    q = {'role_type': "representative",
         'current': "True",
         'party': query}

    json_res = _fetch_govtrack_info(q, "role")
    json_list = json_res['objects']

    reps = []
    for json_dict in json_list:
        rep = PublicOfficial._from_json(json_dict)
        reps.append(rep._to_dict())

    return reps


def get_bills_by_keyword(query):
    """
   Forms and poses the query to get information from the database
   :param query: the values to retrieve
   :return: list of bills
   """

    if not isinstance(query, str):
        raise GovTrackException("Please enter a valid query")

    q = {'q': query}
    json_res = _fetch_govtrack_info(q, "bill")
    json_list = json_res['objects']

    bills = []
    for json_dict in json_list:
        bill = Bill._from_json(json_dict)
        bills.append(bill._to_dict())

    return bills
