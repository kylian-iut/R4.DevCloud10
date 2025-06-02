import asyncio
import nats
import datetime

async def cb(msg):
    cnl=str(msg.data.decode())
    try:
        dt=cnl.split('.',4)[3]
    except IndexError:
        return
    print(dt,end=':')
    if datetime.date.fromisoformat(dt) > datetime.date.today()-datetime.timedelta(10):
        await nc.publish(cnl,b'{"date":true}')
        print("true")
    else:
        await nc.publish(cnl,b'{"date":false}') 
        print("false")

async def subscribe():
    # Connexion au serveur NATS
    global nc
    nc = await nats.connect("nats://127.0.0.1:4222")

    sub = await nc.subscribe("argent.>", cb=cb)

    print("Traitement des dates...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du subscriber.")
        await nc.close()

if __name__ == "__main__":
        asyncio.run(subscribe())
