const messagesContainer = document.getElementById("messages")
const chatForm = document.getElementById("chatForm")
const userInput = document.getElementById("userInput")
const model = document.getElementById("modelsSelection")

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

function getBotResponse(userMessage) {
  const responses = [
    "Query processed. Awaiting further input.",
    "Acknowledged. Operating within defined parameters.",
    "Response generated. Constraints maintained.",
    "Information retrieved. Boundaries respected.",
    "Processing complete. System stable.",
    "Request understood. Limitations observed.",
  ]

  return responses[Math.floor(Math.random() * responses.length)]
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault()

  const message = userInput.value.trim()
  if (!message) return

  addMessage(message, true)
  userInput.value = ""

  setTimeout(() => {
    const botResponse = getBotResponse(message)
    addMessage(botResponse, false)
  }, 500)
})

userInput.focus()
