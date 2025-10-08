const messagesContainer = document.getElementById("messages")
const chatForm = document.getElementById("chatForm")
const userInput = document.getElementById("userInput")
const model = document.getElementById("modelsSelection")
let conversationHistory = [];

function addMessage(text, isUser = false) {
  const messageDiv = document.createElement("div")
  messageDiv.className = `message flex items-start gap-2 ${isUser ? "justify-end" : ""}`

  const bubble = document.createElement("div")
  bubble.className = `rounded p-3 max-w-[80%] font-mono text-xs shadow-lg ${
    isUser
      ? "bg-zinc-800 border border-zinc-700 text-gray-300 shadow-zinc-900/20"
      : "bg-zinc-900 border border-red-900/30 text-gray-300 shadow-red-900/10"
  }`

  if (!isUser) {
    const label = document.createElement("div")
    label.className = "text-[10px] text-red-600 mb-1"
    label.textContent = "SYSTEM"
    bubble.appendChild(label)
  }

  const text_element = document.createElement("p")
  text_element.textContent = text

  bubble.appendChild(text_element)
  messageDiv.appendChild(bubble)
  messagesContainer.appendChild(messageDiv)

  messagesContainer.scrollTop = messagesContainer.scrollHeight
}

function getBotResponse(fullChat) {
    return fetch("http://localhost:5000/response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: fullChat, model: model.value })
    })
    .then(response => response.json())
    .then(data => data.reply)
    .catch(() => "THERE WAS AN ERROR. PLEASE TRY AGAIN.");
}

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault()

    const message = userInput.value.trim()
    if (!message) return

    addMessage(message, true)
    conversationHistory.push({ role: "user", content: message })
    userInput.value = ""

    const botResponse = await getBotResponse(conversationHistory)
    
    addMessage(botResponse, false)
    conversationHistory.push({ role: "assistant", content: botResponse.response })
    console.log(conversationHistory);
})

userInput.focus()
