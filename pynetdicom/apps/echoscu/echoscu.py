#!/usr/bin/env python

"""
    A dcmtk style echoscu application. 
    
    Used for verifying basic DICOM connectivity and as such has a focus on
    providing useful debugging and logging information.
"""

import argparse
import logging
import os
import socket
import sys

from pynetdicom.applicationentity import AE
from pynetdicom.SOPclass import VerificationSOPClass
from pydicom.uid import ExplicitVRLittleEndian

logger = logging.Logger('echoscu')
stream_logger = logging.StreamHandler()
formatter = logging.Formatter('%(levelname).1s: %(message)s')
stream_logger.setFormatter(formatter)
logger.addHandler(stream_logger)
logger.setLevel(logging.ERROR)

def _setup_argparser():
    # Description
    parser = argparse.ArgumentParser(
        description="The echoscu application implements a Service Class User (SCU) "
                    "for the Verification SOP Class. It sends a DICOM C-ECHO "
                    "message to a Service Class Provider (SCP) and waits for a "
                    "response. The application can be used to verify basic "
                    "DICOM connectivity.", 
        usage="echoscu [options] peer port")
        
    # Parameters
    req_opts = parser.add_argument_group('Parameters')
    req_opts.add_argument("peer", help="hostname of DICOM peer", type=str)
    req_opts.add_argument("port", help="TCP/IP port number of peer", type=int)

    # General Options
    gen_opts = parser.add_argument_group('General Options')
    gen_opts.add_argument("--version", 
                          help="print version information and exit", 
                          action="store_true")
    output = gen_opts.add_mutually_exclusive_group()
    output.add_argument("-q", "--quiet", 
                          help="quiet mode, print no warnings and errors", 
                          action="store_true")
    output.add_argument("-v", "--verbose", 
                          help="verbose mode, print processing details", 
                          action="store_true")
    output.add_argument("-d", "--debug", 
                          help="debug mode, print debug information", 
                          action="store_true")
    gen_opts.add_argument("-ll", "--log-level", metavar='[l]', 
                          help="use level l for the logger (fatal, error, warn, "
                               "info, debug, trace)", 
                          type=str, 
                          choices=['fatal', 'error', 'warn', 
                                   'info', 'debug', 'trace'])
    gen_opts.add_argument("-lc", "--log-config", metavar='[f]', 
                          help="use config file f for the logger", 
                          type=str)

    # Network Options
    net_opts = parser.add_argument_group('Network Options')
    net_opts.add_argument("-aet", "--calling-aet", metavar='[a]etitle', 
                          help="set my calling AE title (default: ECHOSCU)", 
                          type=str, 
                          default='ECHOSCU')
    net_opts.add_argument("-aec", "--called-aet", metavar='[a]etitle', 
                          help="set called AE title of peer (default: ANY-SCP)", 
                          type=str, 
                          default='ANY-SCP')
    net_opts.add_argument("-pts", "--propose-ts", metavar='[n]umber', 
                          help="propose n transfer syntaxes (1..128)", 
                          type=int)
    net_opts.add_argument("-ppc", "--propose-pc", metavar='[n]umber', 
                          help="propose n presentation contexts (1..128)", 
                          type=int)
    net_opts.add_argument("-to", "--timeout", metavar='[s]econds', 
                          help="timeout for connection requests", 
                          type=int)
    net_opts.add_argument("-ta", "--acse-timeout", metavar='[s]econds', 
                          help="timeout for ACSE messages", 
                          type=int,
                          default=30)
    net_opts.add_argument("-td", "--dimse-timeout", metavar='[s]econds', 
                          help="timeout for DIMSE messages", 
                          type=int,
                          default=-1)
    net_opts.add_argument("-pdu", "--max-pdu", metavar='[n]umber of bytes', 
                          help="set max receive pdu to n bytes (4096..131072)", 
                          type=int,
                          default=16384)
    net_opts.add_argument("--repeat", metavar='[n]umber', 
                          help="repeat n times", 
                          type=int)
    net_opts.add_argument("--abort", 
                          help="abort association instead of releasing it", 
                          action="store_true")
                          
    # TLS Options
    tls_opts = parser.add_argument_group('Transport Layer Security (TLS) Options')
    tls_opts.add_argument("-dtls", "--disable-tls",
                          help="use normal TCP/IP connection (default)", 
                          action="store_true")
    tls_opts.add_argument("-tls", "--enable-tls", 
                          metavar="[p]rivate key file, [c]erficiate file",
                          help="use authenticated secure TLD connection", 
                          type=str)
    tls_opts.add_argument("-tla", "--anonymous-tls",
                          help="use secure TLD connection without certificate", 
                          action="store_true")
    tls_opts.add_argument("-ps", "--std-password",
                          help="prompt user to type password on stdin (default)", 
                          action="store_true")
    tls_opts.add_argument("-pw", "--use-password", metavar="[p]assword",
                          help="use specified password", 
                          type=str)
    tls_opts.add_argument("-nw", "--null-password",
                          help="use empty string as password", 
                          action="store_true")
    tls_opts.add_argument("-pem", "--pem-keys",
                          help="read keys and certificates as PEM file "
                                                                    "(default)", 
                          action="store_true")
    tls_opts.add_argument("-der", "--der-keys",
                          help="read keys and certificates as DER file", 
                          action="store_true")
    tls_opts.add_argument("-cf", "--add-cert-file", 
                          metavar="[c]ertificate filename",
                          help="add certificate file to list of certificates", 
                          type=str)
    tls_opts.add_argument("-cd", "--add-cert-dir", 
                          metavar="[c]ertificate directory",
                          help="add certificates in d to list of certificates", 
                          type=str)
    tls_opts.add_argument("-cs", "--cipher", 
                          metavar="[c]iphersuite name",
                          help="add ciphersuite to list of negotiated suites", 
                          type=str)
    tls_opts.add_argument("-dp", "--dhparam", 
                          metavar="[f]ilename",
                          help="read DH parameters for DH/DSS ciphersuites", 
                          type=str)
    tls_opts.add_argument("-rs", "--seed", 
                          metavar="[f]ilename",
                          help="seed random generator with contents of f", 
                          type=str)
    tls_opts.add_argument("-ws", "--write-seed", 
                          help="write back modified seed (only with --seed)", 
                          action="store_true")
    tls_opts.add_argument("-wf", "--write-seed-file", 
                          metavar="[f]ilename",
                          help="write modified seed to file f", 
                          type=str)
    tls_opts.add_argument("-rc", "--require-peer-cert", 
                          help="verify peer certificate, fail if absent "
                                        "(default)", 
                          action="store_true")
    tls_opts.add_argument("-vc", "--verify-peer-cert", 
                          help="verify peer certificate if present", 
                          action="store_true")
    tls_opts.add_argument("-ic", "--ignore-peer-cert", 
                          help="don't verify peer certificate", 
                          action="store_true")

    return parser.parse_args()

args = _setup_argparser()

if args.quiet:
    for h in logger.handlers:
        logger.removeHandler(h)
        
    logger.addHandler(logging.NullHandler())
    
    pynetdicom_logger = logging.getLogger('pynetdicom')
    for h in pynetdicom_logger.handlers:
        pynetdicom_logger.removeHandler(h)
        
    pynetdicom_logger.addHandler(logging.NullHandler())

if args.verbose:
    logger.setLevel(logging.INFO)
    pynetdicom_logger = logging.getLogger('pynetdicom')
    pynetdicom_logger.setLevel(logging.INFO)
    
if args.debug:
    logger.setLevel(logging.DEBUG)
    pynetdicom_logger = logging.getLogger('pynetdicom')
    pynetdicom_logger.setLevel(logging.DEBUG)

logger.debug('$echoscu.py v%s %s $' %('0.2.0', '2016-02-16'))
logger.debug('')

called_ae = {'AET' : args.called_aet, 
             'Address' : args.peer, 
             'Port' : args.port}

# Create local AE
# Binding to port 0, OS will pick an available port
ae = AE(AET=args.calling_aet, 
        port=0, 
        SOPSCU=[VerificationSOPClass], 
        SOPSCP=[], 
        SupportedTransferSyntax=[ExplicitVRLittleEndian],
        MaxPDULength=args.max_pdu)

# Request association with remote AE
assoc = ae.request_association(args.peer, 
                               args.port, 
                               args.called_aet)

if assoc.Established:
    
    for ii in args.repeat:
        status = assoc.send_c_echo()
    
    # Abort or release association
    if args.abort:
        assoc.Abort()
    else:
        assoc.Release()

# Quit
ae.Quit()


