import asyncio
import nats

comptes=[16933478]

async def cb(msg):
    cnl=msg.data.decode()
    try:
        cnt=cnl.split('.',4)[1]
    except IndexError:
        return
    print(cnt,end=':')
    if int(cnt) in comptes:
         await nc.publish(cnl,b'{"compte":true}')
         print("true")
    else:
        await nc.publish(cnl,b'{"compte":false}')
        print("false")
    

async def subscribe():
    # Connexion au serveur NATS
    global nc
    nc = await nats.connect("nats://127.0.0.1:4222")

    sub = await nc.subscribe("argent.>", cb=cb)

    print("Traitement des comptes...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du subscriber.")
        await nc.close()

if __name__ == "__main__":
        asyncio.run(subscribe())
