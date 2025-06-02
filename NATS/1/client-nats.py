# publisher.py
import asyncio
import nats
import time

async def publish():
    # Connexion au serveur NATS
    nc = await nats.connect("nats://127.0.0.1:4222")

    # Publication du message "bonjour" sur le sujet "salut"
    k=0
    while True:
        await nc.publish("compteur", str(k).encode())
        print(f"Message {k} envoyé sur le sujet 'compteur'.")
        await asyncio.sleep(10)
        k+=2

    await nc.close()

if __name__ == "__main__":
    asyncio.run(publish())
