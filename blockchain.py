from hashlib import sha256
import datetime
import json


class Blockchain:
    def __init__(self):
        self.chain = list()
        initial_block = self._create_block(
            data="genesis block",
            nounce=1,
            previous_hash="0",
            index=1,
            mined_hash="",
        )
        self.chain.append(initial_block)
        self.difficulty = 4

    def _to_digest(
        self,
        new_nounce: int,
        index: int,
        data: str,
    ):
        to_digest = str(index) + str(new_nounce) + data
        return to_digest.encode()

    def _proof_of_work(self, index: int, data: str):
        new_nounce = 1
        check_nounce = False
        zeros = "0" * self.difficulty
        print(f"zeros: {zeros}")
        while not check_nounce:
            to_digest = self._to_digest(new_nounce, index, data)
            hash_operation = sha256(to_digest).hexdigest()
            if hash_operation[: self.difficulty] == zeros:
                print("checked nounce true")
                print(f"hash:{hash_operation}")
                check_nounce = True
            else:
                new_nounce += 1

        return new_nounce

    def _hash(self, block: dict):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()

    def _create_block(
        self,
        data: str,
        nounce: int,
        previous_hash: str,
        index: int,
        mined_hash: str,
    ):
        block = {
            "index": index,
            "timestamp": str(datetime.datetime.now()),
            "data": data,
            "nounce": nounce,
            "mined_hash": mined_hash,
            "previous_hash": previous_hash,
        }
        return block

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def mine_block(self, data: str) -> dict:
        previous_block = self.get_previous_block()
        index = len(self.chain) + 1
        nounce = self._proof_of_work(
            index=index,
            data=data,
        )
        previous_hash = self._hash(
            block=previous_block,
        )
        current_hash = sha256(
            self._to_digest(
                data=data,
                index=index,
                new_nounce=nounce,
            )
        ).hexdigest()
        block = self._create_block(
            data=data,
            nounce=nounce,
            previous_hash=previous_hash,
            index=index,
            mined_hash=current_hash,
        )
        self.chain.append(block)
        return block

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block["previous_hash"] != self._hash(previous_block):
                return False

            index, data, nounce = block["index"], block["data"], block["nounce"]
            hash_operation = sha256(
                self._to_digest(
                    new_nounce=nounce,
                    index=index,
                    data=data,
                )
            ).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True
