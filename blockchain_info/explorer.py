# coding=utf-8
import os

import datetime

import binascii
from blockchain import blockexplorer

from address_utils import generate_keys


class OutTransactionIsEmptyException(Exception):
    def __init__(self, message, transaction):
        Exception.__init__(self, message)
        self.transaction = transaction


class Explorer:
    _INCOMING_STATUS = 1
    _OUTCOMING_STATUS = -1
    _no_addresses_count = 10
    _sorted = False
    addresses = []
    addresses_data = {}
    in_transactions = []
    out_transactions = []
    trx_offset = 0
    limit = 50

    def __init__(self, addresses=None):
        self.transaction_format = "Transaction {s} completed {d} to address {a}"
        if addresses is None:
            keys = dict()
            for i in range(self._no_addresses_count):
                keys_data = generate_keys()
                keys[keys_data[2]] = keys_data
            self.addresses = tuple(keys.keys())
            addresses_data = blockexplorer.get_multi_address(self.addresses, limit=self.limit)
            for address in addresses_data.addresses:
                if address.address in keys:
                    address.secret_key = keys[address.address][0]
                    address.public_key = keys[address.address][1]
            self.addresses_data = addresses_data
        else:
            self.addresses = tuple(addresses)
            self.addresses_data = blockexplorer.get_multi_address(self.addresses, limit=self.limit)
        self.trx_limit = self.addresses_data.n_tx

    @staticmethod
    def get_balance(address):
        return blockexplorer.get_balance(address)[address].final_balance

    @staticmethod
    def _satoshi_to_btc(satoshi):
        return satoshi / 100000000.0

    @staticmethod
    def _format_price(satoshi):
        return "{0:.8f} BTC".format(Explorer._satoshi_to_btc(float(satoshi)))

    def _get_balance_data(self, address, secret=False):
        btc = self._format_price(address.final_balance)
        if secret:
            secret_key = binascii.hexlify(address.secret_key).decode('ascii').upper()
            return "Balance of {0} Secret Key({1}) is {2}".format(address.address, secret_key, btc)
        return "Balance of {0} is {1}".format(address.address, btc)

    def _get_transactions_data(self, transactions):
        data = []
        for transaction in transactions:
            date_string = datetime.datetime.utcfromtimestamp(transaction.time).strftime('%Y.%m.%d')
            data.append(self.transaction_format.format(s=self._format_price(transaction.value), d=date_string,
                                                       a=transaction.address))
        return os.linesep.join(data)

    def _sort_transactions(self, transactions):
        data = []
        out_transactions = []
        in_transactions = []
        for transaction in transactions:
            try:
                incoming = True
                out_value = 0
                for tx_input in transaction.inputs:
                    if hasattr(tx_input, "address") and tx_input.address in self.addresses:
                        incoming = False
                        out_value += tx_input.value
                if not incoming:
                    transaction.value = -out_value
                    transaction.address = ", ".join(tx_output.address for tx_output in transaction.outputs)
                    out_transactions.append(transaction)
                if incoming:
                    if len(transaction.outputs) == 0:  # TODO: Понять почему output бывает пустым массивом
                        raise OutTransactionIsEmptyException("Out Transactions is Empty!", transaction)
                    else:
                        transaction.value = transaction.outputs[0].value
                        transaction.address = transaction.outputs[0].address
                    in_transactions.append(transaction)
            except OutTransactionIsEmptyException as e:
                data.append("{0} Hash: ({1})".format(e.message, e.transaction.hash))
        return os.linesep.join(data), in_transactions, out_transactions

    def print_data(self, balance=False, incoming=False, outcoming=False, secret=False, headers=True,
                   transaction_format=None):
        if transaction_format:
            self.transaction_format = transaction_format
        data = []
        if balance:
            if headers:
                data.append("{0}Balance:{0}".format(os.linesep))
            for address in self.addresses_data.addresses:
                data.append(self._get_balance_data(address, secret=secret))
            print os.linesep.join(data)
        if incoming or outcoming:
            while self.trx_offset < self.trx_limit:
                if self.trx_offset > 0:
                    transactions = blockexplorer.get_multi_address(self.addresses, limit=self.limit,
                                                                   offset=self.trx_offset).transactions
                else:
                    transactions = self.addresses_data.transactions
                errors, in_transactions, out_transaction = self._sort_transactions(transactions)
                if len(errors) > 0:
                    data.append("{0}Transactions Errors:{0}".format(os.linesep))
                    data.append(errors)
                if incoming and len(in_transactions) > 0:
                    if headers:
                        data.append("{0}Incoming Transactions:{0}".format(os.linesep))
                    data.append(self._get_transactions_data(in_transactions))
                if outcoming and len(out_transaction) > 0:
                    if headers:
                        data.append("{0}Outcoming Transactions:{0}".format(os.linesep))
                    data.append(self._get_transactions_data(out_transaction))
                print os.linesep.join(data)
                self.trx_offset += self.limit
