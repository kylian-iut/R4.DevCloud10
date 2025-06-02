import asyncio
import nats

async def cb(msg):
    print(f"Message reçu: {msg.data.decode()}")

async def subscribe():
    # Connexion au serveur NATS
    nc = await nats.connect("nats://127.0.0.1:4222")

    # Souscription au sujet "bonjour.strasbourg.matin"
    try:
         msg = await nc.request('bonjour.strasbourg.matin',b'ok')
         print(f"reponse recue {msg.data}")
    except nats.errors.NoRespondersError:
         sub = await nc.subscribe("bonjour.strasbourg.matin", cb=cb)

    print("En attente d'un message sur le sujet 'bonjour.strasbourg.matin'...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du subscriber.")
        await nc.close()

if __name__ == "__main__":
        asyncio.run(subscribe())
