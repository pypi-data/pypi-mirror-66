"""
  Copyright (c) Off Chain Data
 
  This source code is licensed under the MIT license found in the
  LICENSE file in the root directory of this source tree.
 """

import os
import json
import urllib.request

# ---------------------------------------------------------------------

class HolidayOracleApi:
    """Provides access to the Holiday Oracle API."""

    _API_URL_BASE = "https://holidayoracle.io/api/v1"

    def __init__( self, token, fixtures_dir=None, event_handler=None ):
        self.token = token or os.environ.get( "OCD_TOKEN" )
        if not self.token:
            raise RuntimeError( "Missing API token." )
        self._fixtures_dir = fixtures_dir
        self._event_handler = event_handler

    def me( self ):
        """Returns information about the API token.
            https://holidayoracle.io/docs/index.html#auth
        """
        return self._call_api( "auth/me", None )

    def date( self, country, **kwargs ):
        """Returns information about the specified date.
            https://holidayoracle.io/docs/index.html#date
        """
        if not kwargs.get("date") and not kwargs.get("timestamp"):
            raise ValueError( "One of 'date' or 'timestamp' must be specified." )
        kwargs["country"] = country
        return self._call_api( "date", kwargs )

    def business_days( self, date1, date2, country, **kwargs ):
        """Calculates business/working days between two dates.
            https://holidayoracle.io/docs/index.html#business-days
        """
        kwargs.update( { "country": country, "date1": date1, "date2": date2 } )
        return self._call_api( "date/business-days", kwargs )        

    def holidays( self, country, year, **kwargs ):
        """Returns a list of holidays.
            https://holidayoracle.io/docs/index.html#holidays
        """
        kwargs.update( { "country": country, "year": year } )
        return self._call_api( "date/holidays", kwargs )

    def locations( self ):
        """Returns a list of supported countries and subdivisions.
            https://holidayoracle.io/docs/index.html#locations
        """
        return self._call_api( "date/locations", None )

    def _call_api( self, endpoint, args ):
        """Call the Holiday Oracle API.

        This is the main entry point into the API, all the other public methods just call into here.
        """

        # check if we're running in test mode
        if self._fixtures_dir:

            # yup - read the response from a file
            fname = endpoint.replace( "/", "-" ) + ".json"
            fname = os.path.join( self._fixtures_dir, fname )
            if self._event_handler:
                self._event_handler( "read-fixture", fname=fname )
            with open( fname, "rb" ) as fp:
                data = fp.read()
            code = 200
            headers = { "Server": "test-suite", "Content-Type": "application/json" }

        else:

            # nope - prepare a request for the live server
            url = "{}/{}".format( HolidayOracleApi._API_URL_BASE, endpoint )
            headers = { "Authorization": "Bearer {}".format( self.token ) }
            if not args:
                data = None
            else:
                data = json.dumps( args ).encode( "utf-8" )
                headers["Content-Type"] = "application/json"

            # send the request
            if self._event_handler:
                self._event_handler( "call-api", url=url, data=data, headers=headers )
            req = urllib.request.Request( url, data, headers )
            try:
                resp = urllib.request.urlopen( req )
            except urllib.error.HTTPError as ex:
                msg = "{} {}".format( ex.code, ex.reason )
                resp = Response( ex.code, ex.headers, None )
                raise ApiError( msg, resp )
            data = resp.read()
            code, headers = resp.code, resp.headers

        # generate the response
        resp = Response( code, headers, data )
        if not resp.json:
            raise ApiError( "Bad JSON response.", resp )
        if resp.json["status"] != "success":
            raise ApiError( resp.json["status"], resp )

        return resp

# ---------------------------------------------------------------------

class Response:
    """Holds an API response."""

    def __init__( self, code, headers, data ):
        self.code = code
        self.headers = dict( headers ) # nb: we return the headers as a *real* dict
        self.raw = data
        try:
            self.json = json.loads( data ) if code == 200 and data else None
        except json.decoder.JSONDecodeError:
            self.json = None

class ApiError( Exception ):
    """Exception class for API errors."""

    def __init__( self, msg, resp ):
        Exception.__init__( self, msg )
        self.message = msg
        self.resp = resp
