import enum
import json


class DataTransferObject:
    """
    Map marshalling objects transferred to and from a remote facade, in this case, libin3 rpc api.
    For more on design-patterns see [Martin Fowler's](https://martinfowler.com/eaaCatalog/) Catalog of Patterns of Enterprise Application Architecture.
    """

    def to_dict(self) -> dict:
        # TODO: Refactor
        aux = self.__dict__
        result = {}
        for i in aux:
            if aux[i] is None:
                continue

            arr = i.split("_")
            r = ""
            index_aux = 0
            for arr_aux in arr:
                if arr_aux == '':
                    continue
                r += arr_aux[index_aux].upper() + arr_aux[index_aux + 1:]
            key = r[0].lower() + r[1:]

            def get_val_from_object(_item) -> object:
                if isinstance(_item, enum.Enum):
                    return _item.value
                # TODO: review or fix this policy
                elif type(_item) == int:
                    return hex(int(_item))
                elif isinstance(_item, Account):
                    return str(_item)
                elif issubclass(_item.__class__, DataTransferObject):
                    return _item.to_dict()
                return _item

            if isinstance(aux[i], tuple):
                value = []
                for a in aux[i]:
                    value.append(get_val_from_object(a))
            else:
                value = get_val_from_object(aux[i])

            result[key] = value
        return result

    def serialize(self) -> str:
        return json.dumps(self.to_dict(self))


# TODO: from - String|Number: The address for the sending account. Uses the web3.eth.defaultAccount property, if not specified. Or an address or index of a local wallet in web3.eth.accounts.wallet.
# TODO: Check if setting gas limit is possible.
class Transaction(DataTransferObject):
    """
    Args:
        From (hex str): Address of the sender account.
        to (hex str): Address of the receiver account. Left undefined for a contract creation transaction.
        gas (int): Gas for the transaction miners and execution in wei. Will get multiplied by `gasPrice`. Use in3.eth.account.estimate_gas to get a calculated value. Set too low and the transaction will run out of gas.
        value (int): Value transferred in wei. The endowment for a contract creation transaction.
        data (hex str): Either a ABI byte string containing the data of the function call on a contract, or in the case of a contract-creation transaction the initialisation code.
        gasPrice (int): Price of gas in wei, defaults to in3.eth.gasPrice. Also know as `tx fee price`. Set your gas price too low and your transaction may get stuck. Set too high on your own loss.
        gasLimit (int); Maximum gas paid for this transaction. Set by the client using this rationale if left empty: gasLimit = G(transaction) + G(txdatanonzero) × dataByteLength. Minimum is 21000.
        nonce (int): Number of transactions mined from this address. Nonce is a value that will make a transaction fail in case it is different from (transaction count + 1). It exists to mitigate replay attacks. This allows to overwrite your own pending transactions by sending a new one with the same nonce. Use in3.eth.account.get_transaction_count to get the latest value.
        hash (hex str): Keccak of the transaction bytes, not part of the transaction. Also known as receipt, because this field is filled after the transaction is sent, by eth_sendTransaction
        blockHash (hex str): Block hash that this transaction was mined in. null when its pending.
        blockNumber (int): Block number that this transaction was mined in. null when its pending.
        transactionIndex (int): Integer of the transactions index position in the block. null when its pending.
        signature (hex str): ECDSA of transaction.data, calculated r, s and v concatenated. V is parity set by v = 27 + (r % 2).
    """

    def __init__(self, From: str, to: str, gas: int, gasPrice: int, hash: str, data: str, nonce: int, gasLimit: int,
                 blockNumber: int, transactionIndex: int, blockHash: str, value: int, signature: str):
        self.blockHash = blockHash
        self.blockNumber = blockNumber
        self.gasLimit = gasLimit
        self.From = From
        self.gas = gas
        self.gasPrice = gasPrice
        self.hash = hash
        self.data = data
        self.nonce = nonce
        self.to = to
        self.transactionIndex = transactionIndex
        self.value = value
        self.signature = signature


class RawTransaction(DataTransferObject):
    """
    Unsent transaction. Use to send a new transaction.
    Args:
        From (hex str): Address of the sender account.
        to (hex str): Address of the receiver account. Left undefined for a contract creation transaction.
        gas (int): Gas for the transaction miners and execution in wei. Will get multiplied by `gasPrice`. Use in3.eth.account.estimate_gas to get a calculated value. Set too low and the transaction will run out of gas.
        value (int): (optional) Value transferred in wei. The endowment for a contract creation transaction.
        data (hex str): (optional) Either a ABI byte string containing the data of the function call on a contract, or in the case of a contract-creation transaction the initialisation code.
        gasPrice (int): (optional) Price of gas in wei, defaults to in3.eth.gasPrice. Also know as `tx fee price`. Set your gas price too low and your transaction may get stuck. Set too high on your own loss.
        gasLimit (int); (optional) Maximum gas paid for this transaction. Set by the client using this rationale if left empty: gasLimit = G(transaction) + G(txdatanonzero) × dataByteLength. Minimum is 21000.
        nonce (int): (optional) Number of transactions mined from this address. Nonce is a value that will make a transaction fail in case it is different from (transaction count + 1). It exists to mitigate replay attacks. This allows to overwrite your own pending transactions by sending a new one with the same nonce. Use in3.eth.account.get_transaction_count to get the latest value.
        hash (hex str): (optional) Keccak of the transaction bytes, not part of the transaction. Also known as receipt, because this field is filled after the transaction is sent.
        signature (hex str): (optional) ECDSA of transaction, r, s and v concatenated. V is parity set by v = 27 + (r % 2).
    """

    def __init__(self, From: str, to: str, gas: int, nonce: int, value: int = None, data: str = None,
                 gasPrice: int = None, gasLimit: int = None, hash: str = None, signature: str = None):
        self.From = From
        self.gas = gas
        self.gasPrice = gasPrice
        self.gasLimit = gasLimit
        self.hash = hash
        self.data = data
        self.nonce = nonce
        self.to = to
        self.value = value
        self.signature = signature


class Block(DataTransferObject):

    def __init__(self, number: int, hash: str, parentHash: str, nonce: int, sha3Uncles: list, logsBloom: str,
                 transactionsRoot: str, stateRoot: str, miner: str, difficulty: int, totalDifficulty: int,
                 extraData: str, size: int, gasLimit: int, gasUsed: int, timestamp: int, transactions: list,
                 uncles: list):

        self.number = number
        self.hash = hash
        self.parentHash = parentHash
        self.nonce = nonce
        self.sha3Uncles = sha3Uncles
        self.logsBloom = logsBloom
        self.transactionsRoot = transactionsRoot
        self.stateRoot = stateRoot
        self.miner = miner
        self.difficulty = difficulty
        self.totalDifficulty = totalDifficulty
        self.extraData = extraData
        self.size = size
        self.gasLimit = gasLimit
        self.gasUsed = gasUsed
        self.timestamp = timestamp
        self.transactions = transactions
        self.uncles = uncles


class Filter(DataTransferObject):
    """
    Filters are event catchers running on the Ethereum Client. Incubed has a client-side implementation.
    An event will be stored in case it is within to and from blocks, or in the block of blockhash, contains a
    transaction to the designed address, and has a word listed on topics.
    """

    def __init__(self, fromBlock: int or str, toBlock: int or str, address: str, topics: list, blockhash: str):
        self.fromBlock = fromBlock
        self.toBlock = toBlock
        self.address = address
        self.topics = topics
        self.blockhash = blockhash


class Account:
    """
    Ethereum address of a wallet or smart-contract
    """

    def __init__(self, address: str, chain_id: str, secret: str = None):
        self.address = address
        self.chain_id = chain_id
        self.secret = secret

    def __str__(self):
        return self.address
