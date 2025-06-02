import asyncio
import nats

async def cb(msg):
    cnl=msg.data.decode()
    try:
        mnt=cnl.split('.',4)[2]
    except IndexError:
        return
    print(mnt,end=':')
    if int(mnt) > 10000:
        await nc.publish(cnl,b'{"montant":false}')
        print("false")
    else:
        await nc.publish(cnl,b'{"montant":true}')
        print("true")

async def subscribe():
    # Connexion au serveur NATS
    global nc
    nc = await nats.connect("nats://127.0.0.1:4222")

    sub = await nc.subscribe("argent.>", cb=cb)

    print("Traitement des montants...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du subscriber.")
        await nc.close()

if __name__ == "__main__":
        asyncio.run(subscribe())
