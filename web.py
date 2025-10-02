from fastapi import FastAPI, Request
import os, json, time

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "KBRIDGE_9f8a1c2b0e4a4a7f")

app = FastAPI()

# 간단 로깅용(선택)
def log(msg): print(f"[webhook] {msg}", flush=True)

@app.post("/kbank-webhook")
async def kbank_webhook(req: Request):
    try:
        token = (req.headers.get("Authorization") or "").replace("Bearer","").strip()
        if token != WEBHOOK_SECRET:
            return {"ok": False, "error": "unauthorized"}

        payload = await req.json()
        gid = int(payload.get("guildId"))
        amount = int(str(payload.get("amount")).replace(",", ""))
        depositor = str(payload.get("depositor")).strip()

        # TODO: 여기서 실제 충전처리 호출
        # 1) Render에 봇도 함께 올렸다면 handle_deposit 직접 호출
        # 2) 아니면, 집/서버에 돌아가는 봇으로 전달(내부 프록시/미니 웹훅/큐)
        # 지금은 응답만 OK로
        log(f"gid={gid}, amount={amount}, depositor={depositor}")
        return {"ok": True, "result": "queued"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
