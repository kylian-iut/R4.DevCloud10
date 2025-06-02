import asyncio
import nats
async def cb(msg):
    print(f"Message reçu: {msg.data.decode()}")

async def subscribe():
    # Connexion au serveur NATS
    nc = await nats.connect("nats://127.0.0.1:4222")

    # Souscription au sujet "fr.Grand_Est.>"
    sub = await nc.subscribe("fr.Grand_Est.>", cb=cb)

    print("En attente d'un message sur le sujet 'fr.Grand_Est.>'...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du subscriber.")
        await nc.close()

if __name__ == "__main__":
        asyncio.run(subscribe())
