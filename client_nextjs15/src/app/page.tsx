'use client'

import { useState } from "react"
import { createSession, whoami, deleteSession, addMessage, listMessages } from "@/app/lib/api"

export default function Home() {
  const [username, setUsername] = useState("")
  const [response, setResponse] = useState("")
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<string[]>([])

  return (
    <main className="p-4 space-y-4">
      <div>
        <input
          placeholder="Enter username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={async () => setResponse(await createSession(username))}>
          Create Session
        </button>
      </div>

      <div>
        <button onClick={async () => setResponse(JSON.stringify(await whoami()))}>
          Who Am I
        </button>
        <button onClick={async () => setResponse(await deleteSession())} className="ml-2">
          Delete Session
        </button>
      </div>

      <div>
        <input
          placeholder="Enter message"
          value={message}
          onChange={e => setMessage(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={async () => setResponse(await addMessage(message))}>
          Add Message
        </button>
        <button
          onClick={async () => {
            const msgs = await listMessages()
            setMessages(msgs)
            setResponse(JSON.stringify(msgs))
          }}
          className="ml-2"
        >
          List Messages
        </button>
      </div>

      <div className="mt-4">
        <p><strong>Response:</strong> {response}</p>
        <ul className="list-disc list-inside">
          {Array.isArray(messages) && messages.length > 0 ? (
            messages.map((msg, idx) => (
              <li key={idx}>{msg}</li>
            ))
          ) : (
            <li>No messages</li>
          )}
        </ul>
      </div>
    </main>
  )
}
