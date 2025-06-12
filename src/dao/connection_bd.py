import re
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pathlib import Path
from os.path import join


base_path = Path(__file__).resolve().parents[1]

def connection_bd():
    try:
        # Conexão com o MongoDB Atlas
        client = MongoClient("mongodb+srv://charlesvilela12:#ProjetoPLN7@cluster0.ieoh4ho.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        client.admin.command("ping")
        db = client['TransformMind']
        collection = db['texts']
        print("✅ Conexão bem-sucedida com o MongoDB Atlas!")
        return collection
    except ConnectionFailure as e:
        print("❌ Erro ao conectar ao MongoDB Atlas:", e)


