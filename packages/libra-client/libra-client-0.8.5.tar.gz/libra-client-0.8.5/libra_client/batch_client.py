import libra
from libra_client import Client
from libra.transaction import Transaction
from libra.account_address import Address
from libra.account_config import AccountConfig
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
from libra.contract_event import ContractEvent
from canoser import Uint64
import pdb

class BatchClient(Client):

    def parseTransactionWithProof(self, proof):
        tx = Transaction.deserialize(proof.transaction.transaction).value
        tx.version = proof.version
        return tx

    def parseTransactionListWithProof(self, tlp):
        start_version = tlp.first_transaction_version.value
        txs = [Transaction.deserialize(x.transaction).value for x in tlp.transactions]
        for tx in txs:
            tx.version = start_version
            start_version += 1
        return txs


    @staticmethod
    def get_range_asc(sequence_number, start_version, limit):
        end_version = start_version+limit
        if end_version > sequence_number:
            end_version = sequence_number
        return range(start_version, end_version)

    @staticmethod
    def get_range_desc(sequence_number, limit):
        end_version = sequence_number
        start_version = sequence_number - limit
        if start_version < 0:
            start_version = 0
        return range(start_version, end_version)

    def _get_acc_txns_by_range(self, address, rg):
        address = Address.normalize_to_bytes(address)
        request = UpdateToLatestLedgerRequest()
        for idx in rg:
            item = request.requested_items.add()
            itemreq = item.get_account_transaction_by_sequence_number_request
            itemreq.account = address
            itemreq.sequence_number = idx
            itemreq.fetch_events = False
        resp = self.get_with_proof(request)
        tp = [x.get_account_transaction_by_sequence_number_response.transaction_with_proof
            for x in resp.response_items]
        return [self.parseTransactionWithProof(x) for x in tp]

    def get_send_txs_by_address(self, address, start_version, limit):
        seq = self.get_sequence_number(address)
        rg = MyClient.get_range_asc(seq, start_version, limit)
        return self._get_acc_txns_by_range(address, rg)

    def get_send_latest_txs_by_address(self, address, limit):
        seq = self.get_sequence_number(address)
        rg = MyClient.get_range_desc(seq, limit)
        return self._get_acc_txns_by_range(address, rg)

    def batch_get_txs(self, ids):
        request = UpdateToLatestLedgerRequest()
        for idx in ids:
            item = request.requested_items.add()
            item.get_transactions_request.start_version = idx
            item.get_transactions_request.limit = 1
            item.get_transactions_request.fetch_events = False
        resp = self.get_with_proof(request)
        tlps = [x.get_transactions_response.txn_list_with_proof for x in resp.response_items]
        return [self.parseTransactionListWithProof(tlp)[0] for tlp in tlps]

    def _get_events(self, address, limit, start_event_seq_num, ascending):
        if limit <= 0 or limit >= Uint64.max_value:
            raise ValueError(f"limit:{limit} is invalid.")
        address = Address.normalize_to_bytes(address)
        request = UpdateToLatestLedgerRequest()
        spath = libra.AccountConfig.account_sent_event_path()
        rpath = libra.AccountConfig.account_received_event_path()
        for path in [spath, rpath]:
            item = request.requested_items.add()
            eapr = item.get_events_by_event_access_path_request
            eapr.access_path.address = address
            eapr.access_path.path = path
            eapr.start_event_seq_num = start_event_seq_num
            eapr.ascending = ascending
            eapr.limit = limit
        resp = self.get_with_proof(request)
        epss = [x.get_events_by_event_access_path_response.events_with_proof
            for x in resp.response_items]
        sent, received =  [[ContractEvent.from_proto_event_with_proof(ep)
             for ep in eps] for eps in epss]
        return {"sent": sent, "received": received}

    def get_latest_events_both(self, address, limit=1):
        start_event_seq_num = 2**64-1
        ascending = False
        return self._get_events(address, limit, start_event_seq_num, ascending)

    def get_events_both(self, address, start_event_seq_num, limit=1):
        ascending = True
        return self._get_events(address, limit, start_event_seq_num, ascending)