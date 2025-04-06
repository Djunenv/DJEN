from communex.module import Module, endpoint
from communex.key import generate_keypair
from keylimiter import TokenBucketLimiter


class Miner(Module):
    @endpoint
    def mine_Waste(self, prompt: str, model: str = "foo"):
        print(f"Answering: `{prompt}` with model `{model}`")
        return {"answer":{prompt}}
