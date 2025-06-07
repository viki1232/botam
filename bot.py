import discord
import os
import discord
from discord.ext import commands
import requests
import logging
import random
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

description = '''Un bot que consulta el clima.'''


intents = discord.Intents.default()
intents.members = True
intents.message_content = True


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

genai.configure(api_key="")
model = genai.GenerativeModel('gemini-2.0-flash')


CLIMATE_KEYWORDS = ["clima", "cambio climático", "medio ambiente", "calentamiento", "emisiones", "contaminación", "efecto invernadero"]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!gemini"):
        prompt = message.content[len("!gemini"):].strip()

        if not any(keyword in prompt.lower() for keyword in CLIMATE_KEYWORDS):
            await message.channel.send("🌍 Este bot solo responde preguntas relacionadas con el *cambio climático*.")
            return

        try:
            # Instrucción adicional para mantener el tema centrado
            system_prompt = (
                "Responde únicamente preguntas relacionadas con el cambio climático, medio ambiente y temas ecológicos. "
                "Si la pregunta no está relacionada, responde educadamente que no puedes responder."
            )
            # Se combina el prompt del sistema con el del usuario
            full_prompt = f"{system_prompt}\n\nPregunta del usuario: {prompt}"
            response = model.generate_content(full_prompt)
            text = response.text
            await message.channel.send(text)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("⚠️ Ocurrió un error al procesar tu solicitud.")

client.run()