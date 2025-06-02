# publisher.py
import asyncio
import nats

test=2
cnl = ["argent.16933478.10500.2025-01-08","argent.16933478.505.2025-06-08","argent.16933478.460.2025-06-02","argent.78666310.10.2025-06-02","argent.78666310.11.2025-06-01"]

async def cb(msg):
    valid.append(msg.data.decode())
    print(f"Message reçu: {msg.data.decode()}")

async def publish(n):
    # Connexion au serveur NATS
    global valid
    valid=[]
    nc = await nats.connect("nats://127.0.0.1:4222")

    print(f"En attente pour {cnl[n]}...")
    msg = await nc.publish(cnl[n],cnl[n].encode())
    
    sub = await nc.subscribe(cnl[n], cb=cb)
    
    try:
        while len(valid)<3:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du subscriber.")
        await nc.close()
        return

    await nc.close()
    print(valid)

if __name__ == "__main__":
    asyncio.run(publish(test))
    
