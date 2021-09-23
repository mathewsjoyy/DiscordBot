import discord
import json
import requests
from discord.ext import commands

class crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['Price', 'price', 'crypto'])
    async def getCryptoPrice(self, ctx, coin:str = None):
        if(coin == None):
            await ctx.reply("*Check your arguments!*\n```/getCryptoPrice COIN_NAME```")
        else:
            coin = coin.lower()
            
            try:
                coinData = requests.get(url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd')
            except Exception:
                await ctx.reply("*The Crypto coin API is down, try again later!*")
                return
            
            coinDataJSON = coinData.json()
            
            for i in range(len(coinDataJSON)): # Search trough the json data for the coin
                print(coinDataJSON[i]['id'])
                if(coinDataJSON[i]['id'] == coin):
                    await ctx.reply(f"""
*Current Price Of : {coin} =* **{coinDataJSON[i]['current_price']} USD**
**{coinDataJSON[i]['high_24h']}** *(24 hour HIGH)*
**{coinDataJSON[i]['low_24h']}** *(24 hour LOW)*""")
                    return
            
            await ctx.reply(f"*Can't seem to find that coin (**{coin}**) :/*")
            
    
    @commands.command(aliases=['supported','supportedCoins'])
    async def support(self, ctx):
        try:
            coinData = requests.get(url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd')
        except Exception:
            print("*The Crypto coin API is down, try again later!*")
            return
            
        coinDataJSON = coinData.json()
        
        for i in range(len(coinDataJSON)): # Search trough the json data for the coin
            await ctx.reply(f"*{coinDataJSON[i]['id']}* ", end=" ")
        
        
def setup(bot):
    bot.add_cog(crypto(bot))