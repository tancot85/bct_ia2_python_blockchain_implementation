import fastapi
import blockchain

blockchain = blockchain.Blockchain()
app = fastapi.FastAPI()

print("===========APPLICATION HAS STARTED=================")


@app.post("/mine_block/")
def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )
    block = blockchain.mine_block(data=data)

    return block


@app.post("/set_difficulty")
def set_difficulty(difficulty):
    blockchain.set_difficulty(int(difficulty))
    dic = {"difficulty": blockchain.difficulty}
    return dic


@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )
    chain = blockchain.chain
    return chain


@app.get("/validate/")
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )

    return blockchain.is_chain_valid()


@app.get("/blockchain/last/")
def previous_block():
    if not blockchain.is_chain_valid():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )

    return blockchain.get_previous_block()


@app.get("/get_difficulty")
def get_difficulty():
    dic = {"difficulty": blockchain.difficulty}
    return dic
