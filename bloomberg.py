# SimpleRefDataExample.py

import blpapi
from optparse import OptionParser


def parseCmdLine():
    parser = OptionParser(description="Retrieve reference data.")
    parser.add_option("-a",
                      "--ip",
                      dest="host",
                      help="server name or IP (default: %default)",
                      metavar="ipAddress",
                      default="50.19.46.133")
    parser.add_option("-p",
                      dest="port",
                      type="int",
                      help="server port (default: %default)",
                      metavar="tcpPort",
                      default=8194)

    (options, args) = parser.parse_args()

    return options

def procfromtxt(data_str):
    """ does the best possible job of converting from the string format results to a dictionary

        securityData : {
            security : "SPLK US Equity"
            eidData : {
            },
            fieldExceptions : {
            },
            sequenceNumber : 9
            fieldData : {
                EQY_PO_LEAD_MGR : "MS,BAML,CS,JPM"
                INDUSTRY_SECTOR : "Communications"
                INDUSTRY_GROUP : "Internet"
            },
        },

"EVAC": {
            "eidData" : {
            },
            "fieldExceptions" : {
            },
            "sequenceNumber" : 39,
            "fieldData" : {
                "INDUSTRY_SECTOR" : "Industrial",
                "INDUSTRY_GROUP" : "Machinery-Diversified",
                "INDUSTRY_SUBGROUP" : "Machinery-General Indust",
                "MARKET_SECTOR" : 2,
                "EQY_FUND_IND" : "Industrial",
            },
        },

"""
    results = []
    for line in data_str.split("\n"):
        parts = line.strip().split()
        if line.startswith("        securityData : {"):
            continue
        elif line.startswith('            fieldData : {'):
            continue
        elif line.startswith('            fieldExceptions : {'):
            continue
        elif line.startswith('            eidData : {'):
            continue
        elif line.startswith('            security : "'):
            line = line.replace('            security : ', '').replace(' US Equity','').strip() + ": {"
        elif line.startswith('            sequenceNumber :'):
            continue # I don't think we need this at all
            #line = line.strip().split()[-1] + ","
            line = line + ","
        elif line.endswith('"'):
            line = '                "%s" : %s,' % (parts[0], " ".join(parts[2:]))
        elif line.endswith('{'):
            line = '                "%s" : {' % (parts[0])
        elif len(parts) == 3:
            line = '                "%s" : %s,' % (parts[0], parts[2])
        elif line.startswith('        },'):
            pass # leave the line as it is
        else:
            continue
        results.append(line)
    return "\n".join(results)

def query(tickers=[], fields=[]):
    global options
    options = parseCmdLine()

    # Fill SessionOptions
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print "Connecting to %s:%d" % (options.host, options.port)

    # Create a Session
    session = blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print "Failed to start session."
        return

    if not session.openService("//blp/refdata"):
        print "Failed to open //blp/refdata"
        return

    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("ReferenceDataRequest")

    # append securities to request
    for ticksym in tickers:
        request.append("securities", "%s US Equity" % ticksym)

    # append fields to request
    for field in fields:
        request.append("fields", field)

    print "Sending Request:", request
    session.sendRequest(request)

    results = []
    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
                serial = msg.toString().replace("=",":").replace("}","},").replace("[]","")
                results.append(serial)
            # Response completly received, so we could exit
            if ev.eventType() == blpapi.Event.RESPONSE:
                break
    finally:
        # Stop the session
        session.stop()
    return results

if __name__ == "__main__":
    print "SimpleRefDataExample"
    try:
        ticksyms = []
        with open("results.csv") as fh:
            first = True
            for line in fh:
                if first:
                    first = False
                    continue
                try:
                    parts = line.split(",")
                    ticksyms.append(parts[1])
                except:
                    print "ERROR on line [%s]" % line
        results = query(ticksyms, """
EQY_PO_LEAD_MGR
INDUSTRY_SECTOR
INDUSTRY_GROUP
INDUSTRY_SUBGROUP
MARKET_SECTOR
EQY_FUND_IND
EQY_INST_SH_HELD
EQY_INST_SELLS
EQY_INST_HOLD
EQY_INST_BUYS
EQY_SH_PURCH_SOLD
EQY_INIT_PO_SH_OFFER
EQY_PO_SH_PX
""".split())
        with open('results.py','w') as output_fh:
            for result in results:
                output_fh.write(procfromtxt(result))
    except KeyboardInterrupt:
        print "Ctrl+C pressed. Stopping..."

__copyright__ = """
Copyright 2012. Bloomberg Finance L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above
copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
