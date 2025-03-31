import asyncio
import httpx

BASE_URL = "http://localhost:8000"

class SessionClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url, cookies={})

    async def create_session(self, username: str):
        response = await self.client.post(f"/create_session/{username}")
        print("Session created:", response.text)
        print("Cookies:", self.client.cookies)

    async def add_message(self, message: str):
        response = await self.client.post("/add_message", json={"message": message})
        if response.status_code == 200:
            print("Message added:", response.json())
        else:
            print("Error adding message:", response.text)

    async def list_messages(self):
        response = await self.client.get("/get_messages")
        if response.status_code == 200:
            print("Messages:", response.json())
        else:
            print("Error fetching messages:", response.text)

    async def close(self):
        await self.client.aclose()


async def main():
    session_client = SessionClient(BASE_URL)
    await session_client.create_session("alice")
    await session_client.add_message("Hello from async client!")
    await session_client.add_message("Async second message.")
    await session_client.add_message("Async third message.")
    await session_client.list_messages()
    await session_client.close()

if __name__ == "__main__":
    asyncio.run(main())
