##
# File: UrlRequestUtil.py
#
# Simple wrapper for URL request processing
#
# Updates:
#  17-Mar-2019 jdw adjust return value to include response error code
#  16-Dec-2019 jdw add HTTPException to retry()
#
##

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import contextlib
import logging
import ssl

from rcsb.utils.io.decorators import retry

try:
    from http.client import HTTPException
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request, URLError, HTTPError

    # from http.client import HTTPException, RemoteDisconnected
except ImportError:
    # pylint: disable=ungrouped-imports
    from httplib import HTTPException
    from urllib import urlencode
    from urllib2 import urlopen, Request, URLError, HTTPError

logger = logging.getLogger(__name__)


class UrlRequestUtil(object):
    """ Simple wrapper for URL request processing

    """

    def __init__(self, **kwargs):
        pass

    def postUnWrapped(self, url, endPoint, paramD, **kwargs):
        return self.__post(url, endPoint, paramD, **kwargs)

    @retry((URLError, HTTPError, HTTPException), maxAttempts=3, delaySeconds=5, multiplier=3, defaultValue=(None, None), logger=logger)
    def post(self, url, endPoint, paramD, **kwargs):
        return self.__post(url, endPoint, paramD, **kwargs)

    def __post(self, url, endPoint, paramD, **kwargs):
        """
        """
        ret = None
        retCode = None
        sslCert = kwargs.get("sslCert", "disable")
        exceptionsCatch = kwargs.get("exceptionsCatch", (HTTPError))
        httpCodesCatch = kwargs.get("httpCodesCatch", [])
        optD = {}
        try:
            if sslCert == "disable":
                gcontext = ssl._create_unverified_context()  # pylint: disable=protected-access
                optD = {"context": gcontext}
            #
            urlPath = "%s/%s" % (url, endPoint)
            requestData = urlencode(paramD).encode("utf-8")
            logger.debug("Request %s with data %r", urlPath, requestData)

            with contextlib.closing(urlopen(urlPath, requestData, **optD)) as req:
                # pylint: disable=no-member
                ret = req.read().decode("utf-8")
                retCode = req.getcode()
        #
        except exceptionsCatch as e:
            logger.debug("status code %r", e.code)
            retCode = e.code
            if retCode not in httpCodesCatch:
                raise e
        except Exception as e:
            logger.error("Failing %s %s %r with %s", url, endPoint, paramD, str(e))
            raise e

        return ret, retCode

    def getUnWrapped(self, url, endPoint, paramD, **kwargs):
        return self.__get(url, endPoint, paramD, **kwargs)

    @retry((URLError, HTTPError, HTTPException), maxAttempts=3, delaySeconds=5, multiplier=3, defaultValue=(None, None), logger=logger)
    def get(self, url, endPoint, paramD, **kwargs):
        return self.__get(url, endPoint, paramD, **kwargs)

    def __get(self, url, endPoint, paramD, **kwargs):
        """
        """
        ret = None
        retCode = None
        sslCert = kwargs.get("sslCert", "disable")
        headerL = kwargs.get("headers", None)
        exceptionsCatch = kwargs.get("exceptionsCatch", (HTTPError))
        httpCodesCatch = kwargs.get("httpCodesCatch", [])
        optD = {}
        try:
            if sslCert == "disable":
                gcontext = ssl._create_unverified_context()  # pylint: disable=protected-access
                optD = {"context": gcontext}
            #
            urlPath = "%s/%s" % (url, endPoint)
            requestData = urlencode(paramD)
            logger.debug("Request %s with data %s", urlPath, requestData)

            req = Request("%s?%s" % (urlPath, requestData))
            if headerL:
                for hTup in headerL:
                    req.add_header(hTup[0], hTup[1])

            with contextlib.closing(urlopen(req, **optD)) as req:
                # pylint: disable=no-member
                ret = req.read().decode("utf-8")
                retCode = req.getcode()
        except exceptionsCatch as e:
            retCode = e.code
            if retCode not in httpCodesCatch:
                raise e
        except Exception as e:
            logger.error("Failing %s %s %r with %s", url, endPoint, paramD, str(e))
            raise e

        return ret, retCode
