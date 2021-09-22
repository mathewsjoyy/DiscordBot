import discord
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
            
            print(coinDataJSON['bitcoin'])
            
            await ctx.reply(f"Done {coin}")
    
            
      
            
def setup(bot):
    bot.add_cog(crypto(bot))