# publisher.py
import asyncio
import nats

cnl = ['bonjour.strasbourg.matin','bonjour.strasbourg.midi','bonjour.colmar.matin']

async def publish():
    # Connexion au serveur NATS
    nc = await nats.connect("nats://127.0.0.1:4222")
    inbox = nc.new_inbox()

    # Publication du message "bonjour" sur le sujet "salut"
    for ville in cnl:
        for i in range(1,11,1):
            await nc.publish(ville, f"{i} Coucou {ville.split('.')[-2]}".encode(), reply=inbox)
        print(f"10 Messages envoyés à {ville}")

    await nc.close()

if __name__ == "__main__":
    asyncio.run(publish())
    
