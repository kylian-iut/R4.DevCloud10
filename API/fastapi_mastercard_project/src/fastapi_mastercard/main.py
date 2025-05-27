from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CardIdRequest(BaseModel):
    card_id: str

@app.post("/clear-pin-try-counter")
async def clear_pin_try_counter(request: CardIdRequest):
    # Ici tu récupères request.card_id
    card_id = request.card_id

    # Simule un appel au client Mastercard
    return {"message": f"Pin try counter cleared for card {card_id}"}
