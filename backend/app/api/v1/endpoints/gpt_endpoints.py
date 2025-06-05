from fastapi import APIRouter
from fastapi import Request
from openai import AsyncOpenAI
import asyncio

import random
router = APIRouter()


@router.get("/")
async def transform_message(content: str, request: Request):
    openai_api_key = request.app.state.settings.openai_api_key
    assistant_id = request.app.state.settings.assistant_id

    client = AsyncOpenAI(api_key=openai_api_key)


    try:
        thread = await client.beta.threads.create()

        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content
        )

        run = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        while True:
            run_status = await client.beta.threads.runs.retrieve(
													              thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            elif run_status.status in {"failed", "cancelled"}:
                raise Exception(f"Run failed: {run_status.status}")
            await asyncio.sleep(0.5)

        messages = await client.beta.threads.messages.list(thread_id=thread.id)
        answer = messages.data[0].content[0].text.value.strip()

        is_abusive = answer != content
        updated_score = -5 if is_abusive else 0

        return {
            "is_abusive": is_abusive,
            "sanitized": answer,
            "updated_score": updated_score
        }

    except Exception as e:
        print(f"[Assistant Error] {e}")
        return {
            "is_abusive": False,
            "sanitized": content,
            "updated_score": 0
        }

