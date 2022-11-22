# trading-bot
 
This bot is an EVM compatible trading bot, meant to be multi chain, only tested on BSC and BSC testnet with the pancakeswap router.
It can trade tokens, and subscribe to the router in order to detect a new pair and trade based on that.
It uses selenium to get the contract ABIS from the network block explorer.
To use (remove the word 'example' from config_testnet_example, and fill the blanks.)