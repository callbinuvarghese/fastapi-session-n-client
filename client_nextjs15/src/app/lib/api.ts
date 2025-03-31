export async function createSession(username: string) {
    const res = await fetch("http://localhost:8000/create_session/" + username, {
      method: "POST",
      credentials: "include",
    });
    return res.text();
  }
  
  export async function whoami() {
    const res = await fetch("http://localhost:8000/whoami", {
      credentials: "include",
    });
    return res.json();
  }
  
  export async function deleteSession() {
    const res = await fetch("http://localhost:8000/delete_session", {
      method: "POST",
      credentials: "include",
    });
    return res.text();
  }
  
  export async function addMessage(message: string) {
    const res = await fetch("http://localhost:8000/add_message", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
    return res.text();
  }
  
  export async function listMessages() {
    const res = await fetch("http://localhost:8000/get_messages", {
      credentials: "include",
    });
    const data = await res.json();
    const messages = Array.isArray(data) ? data : []; 
    return messages
  }
  