from web3 import Web3
import json
import time
from BuyTokens import buyTokens
import config_testnet as config
from scanner import Scanner
import asyncio



scan = Scanner()

bsc = config.RPC
web3 = Web3(Web3.HTTPProvider(bsc))
factory = web3.eth.contract(address=config.PANCAKE_FACTORY_ADDRESS, abi=scan.getAbi(config.PANCAKE_FACTORY_ADDRESS))
router = web3.eth.contract(address=config.PANCAKE_ROUTER_ADDRESS, abi=scan.getAbi(config.PANCAKE_ROUTER_ADDRESS))


def handle_event(event):
    data = json.loads(Web3.toJSON(event))
    args = data["args"]
    token0 = args["token0"]
    token1 = args["token1"]
    print(f'pair token 0: {scan.getTokenTracker(token0)} token 1: {scan.getTokenTracker(token1)}')
    # print(Web3.toJSON(event))

async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


def main():
    # 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56 busd
    # add1 = Web3.toChecksumAddress("0x373E768f79c820aA441540d254dCA6d045c6d25b")
    # add2 = Web3.toChecksumAddress("0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56")
    print(web3.isConnected())
    wbnb_add = Web3.toChecksumAddress(config.WBNB_ADDRESS)
    busd_add = Web3.toChecksumAddress(config.BUSD_ADDRESS)
    wbnb = web3.eth.contract(address=wbnb_add, abi=scan.getAbi(config.WBNB_ADDRESS))
    busd = web3.eth.contract(address=busd_add, abi=scan.getAbi(config.BUSD_ADDRESS))
    TradingTokenDecimal = wbnb.functions.decimals().call()
    symbol = wbnb.functions.symbol().call()
    # a = factory.functions.getPair(wbnb_add,busd_add).call()
    # pair = web3.eth.contract(address=a, abi=scan.getAbi(a))
    # reserves = pair.functions.getReserves().call()
    # price = reserves[1]/reserves[0]
    # print(scan.getAbi("0x373E768f79c820aA441540d254dCA6d045c6d25b"))

    params = {
        'symbol': symbol,
        'web3': web3,
        'walletAddress': Web3.toChecksumAddress(config.WALLET_ADDRESS),
        'contractBuyToken': busd,
        'contractPancake': router,
        'pancakeRouterAddress': web3.toChecksumAddress(config.PANCAKE_ROUTER_ADDRESS),
        'TokenToBuyAddress': busd_add,
        'WBNB_Address': wbnb_add,
        'TradingTokenDecimal': TradingTokenDecimal
    }
    buyTokens(params)
    print(web3.isConnected())
    # event_filter = factory.events.PairCreated.createFilter(fromBlock='latest')
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(
    #         asyncio.gather(
    #             log_loop(event_filter,0.2)
    #         )
    #     )
    # finally:
    #     loop.close()


if __name__ == "__main__":
    main()