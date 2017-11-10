# coding=utf-8
import argparse
import sys
from urllib2 import URLError


def parse_arg():
    parser = argparse.ArgumentParser(description="Get Info About BTC addresses")
    parser.add_argument("addresses", nargs='*', help="BTC Addresses")
    parser.add_argument("-b", "--balance", action="store_true", help="Print balance of addresses")
    parser.add_argument("-i", "--incoming", action="store_true", help="Print in transactions of addresses")
    parser.add_argument("-o", "--outcoming", action="store_true", help="Print out transactions of addresses")
    parser.add_argument("-f", "--format", action="store", type=str,
                        help='Custom format for transaction string {d} — Transaction Date {a} — Transaction Address {'
                             's} — BTC Value. Example: "Transaction {s} completed {d} to address {a}"')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        from blockchain.exceptions import APIException
        from blockchain_info import Explorer
        args = parse_arg()

        exp = Explorer(args.addresses if len(args.addresses) > 0 else None)
        if len(args.addresses) == 0:
            exp.print_data(balance=True, secret=True, headers=False)
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
            exp.print_data(**kwargs)
    except ImportError as e:
        print "Some Modules not Installed! ({0})".format(e.message)
    except APIException as e:
        print "API Exception ({0})".format(e.message)
    except URLError as e:
        print "No Internet Connection!"
    except Exception as e:
        print "Exception! {0}".format(e.message)
    finally:
        print
        print "Stopping"
        sys.exit()
