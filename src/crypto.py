import discord
import json
import requests
from discord.ext import commands

class crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def getCryptoPrice(self, ctx, coin:str = None):
        if(coin == None):
            await ctx.reply("*Check your arguments!*\n```/getCryptoPrice COIN_NAME```")
        else:
            coinData = requests.get(url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd')
            coinDataJSON = coinData.json()
            
            for i in range(len(coinDataJSON)):
                if(coinDataJSON[i][id] == "coin"):
                    await ctx.reply(f"*Current Price Of : {coin} = {coinDataJSON[i]['current_price']}*")
                    return
            
            await ctx.reply(f"*Can't seem to find that coin ({coin}) :/*")
            
            
    
            
      
            
def setup(bot):
    bot.add_cog(crypto(bot))