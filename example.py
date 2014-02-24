import argparse
import datetime
import sys

import nmsg
import wdns

def nmsg_input(input):
    while True:
        m = input.read()
        if not m:
            break
        yield m

parser = argparse.ArgumentParser()
parser.add_argument('--output','-o', default='-',
        help='Output to file')
parser.add_argument('input', help='Input file')
args = parser.parse_args()

if args.output == '-':
    out = sys.stdout
else:
    out = open(args.output, 'w')

for m in nmsg_input(nmsg.input.open_file(args.input)):
    print >>out, 'count: %d' % m['count']
    print >>out, 'time_first: %s' % datetime.datetime.fromtimestamp(m['time_first']).isoformat()
    print >>out, 'time_last: %s' % datetime.datetime.fromtimestamp(m['time_last']).isoformat()
    if 'response_ip' in m.fields:
        print >>out, 'response_ip: %s' % m['response_ip']
    print >>out, 'bailiwick: %s' % wdns.domain_to_str(m['bailiwick'])
    print >>out, 'rrname: %s' % wdns.domain_to_str(m['rrname'])
    print >>out, 'rrclass: %s (%d)' % (wdns.rrclass_to_str(m['rrclass']), m['rrclass'])
    print >>out, 'rrtype: %s (%d)' % (wdns.rrtype_to_str(m['rrtype']), m['rrtype'])
    print >>out, 'rrttl: %d' % m['rrttl']
    for rdata in m['rdata']:
        print 'rrdata: %s' % repr(wdns.rdata(rdata, m['rrclass'], m['rrtype']))
    print >>out
