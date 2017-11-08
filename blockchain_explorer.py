# coding=utf-8
import argparse
import ecdsa
import os

import signal

import sys
from blockchain import blockexplorer
from blockchain.exceptions import APIException

from blockchain_info import Explorer
from blockchain_info.address_utils import generate_keys


def parse_arg():
    parser = argparse.ArgumentParser(description="Get Info About BTC addresses")
    parser.add_argument("addresses", nargs='*', help="BTC Addresses")
    parser.add_argument("-b", "--balance", action="store_true", help="Print balance of addresses")
    parser.add_argument("-i", "--incoming", action="store_true", help="Print in transactions of addresses")
    parser.add_argument("-o", "--outcoming", action="store_true", help="Print out transactions of addresses")
    parser.add_argument("-f", "--format", action="store", type=str,
                        help='Custom format for transaction string {d} — Transaction Date {a} — Transaction Address {'
                             's} — BTC Value')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = parse_arg()

        # l = Explorer.get_balance(generate_keys()[2])
        exp = Explorer(args.addresses if len(args.addresses) > 0 else None)
        if len(args.addresses) == 0:
            print exp.print_data(balance=True, secret=True, headers=False)
        else:
            kwargs = {}
            if args.balance:
                kwargs["balance"] = True
            if args.incoming:
                kwargs["incoming"] = True
            if args.outcoming:
                kwargs["outcoming"] = True
            if args.format:
                kwargs["transaction_format"] = args.format
            print exp.print_data(**kwargs)
    except APIException as e:
        print "API Exception ({0})".format(e.message)
    except Exception as e:
        print "Exception! {0}".format(e.message)
    finally:
        print
        print "Stopping"
        sys.exit()
