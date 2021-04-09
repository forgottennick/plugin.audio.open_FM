import gzip
import urllib.error
import urllib.parse
import urllib.request


#
# HTTPCommunicator
#
class HTTPCommunicator:
    #
    # GET
    #
    def get(self, url):
        httpHandler = urllib.request.HTTPHandler(debuglevel=0)

        try:
            request = urllib.request.Request(url)
            request.add_header("Accept", "*/*")
            request.add_header("Accept-Encoding", "gzip")
            request.add_header(
                "User-Agent",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            )
            opener = urllib.request.build_opener(httpHandler)
            f = opener.open(request)
        # Exception
        except urllib.error.HTTPError as e:
            raise Exception("HTTP Error %u: %s" % (e.code, HTTP_REPONSES[e.code]))

        # Compressed (gzip) response...
        if f.headers.get("content-encoding") == "gzip":
            httpData = gzip.decompress(f.read())

            # Debug
            # print "[HTTP Communicator] GET %s" % url
            # print "[HTTP Communicator] Result size : compressed [%u], decompressed [%u]" % ( len( httpGzippedData ), len ( httpData ) )

        # Plain text response...
        else:
            httpData = f.read()

        # Cleanup
        f.close()

        # Return value
        return str(httpData, "utf-8")
