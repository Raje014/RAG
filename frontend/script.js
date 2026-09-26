const chatMessages =
    document.getElementById("chatMessages");

const questionInput =
    document.getElementById("questionInput");

const sendButton =
    document.getElementById("sendButton");

const typing =
    document.getElementById("typing");


async function sendMessage() {

    const question =
        questionInput.value.trim();

    if (!question) {
        return;
    }


    // Display user message

    addMessage(
        question,
        "user"
    );


    questionInput.value = "";

    questionInput.style.height = "auto";


    // Disable button

    sendButton.disabled = true;

    typing.classList.remove("hidden");


    try {

        const response =
            await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            });


        const data =
            await response.json();


        typing.classList.add("hidden");


        if (!response.ok) {

            addMessage(
                data.error ||
                "Something went wrong.",
                "assistant"
            );

            return;
        }


        addMessage(
            data.answer,
            "assistant",
            data.sources
        );


    } catch (error) {

        console.error(error);

        typing.classList.add("hidden");

        addMessage(
            "Unable to connect to the server. Please make sure the Flask backend is running.",
            "assistant"
        );

    } finally {

        sendButton.disabled = false;

        questionInput.focus();

    }

}


function addMessage(
    text,
    sender,
    sources = []
) {

    const message =
        document.createElement("div");

    message.className =
        `message ${sender}`;


    const avatar =
        document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent =
        sender === "user"
            ? "YOU"
            : "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const bubble =
        document.createElement("div");

    bubble.className = "bubble";


    // Convert new lines

    const formattedText =
        escapeHtml(text)
            .replace(/\n/g, "<br>");


    bubble.innerHTML =
        `<p>${formattedText}</p>`;


    // Show sources only when available

    if (
        sender === "assistant" &&
        sources &&
        sources.length > 0
    ) {

        const sourceBox =
            document.createElement("div");

        sourceBox.className =
            "sources";


        sourceBox.innerHTML =
            `<small>Retrieved from document</small>`;


        bubble.appendChild(
            sourceBox
        );

    }


    content.appendChild(bubble);


    message.appendChild(avatar);

    message.appendChild(content);


    chatMessages.appendChild(message);


    // Scroll down

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


function handleKey(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


function clearChat() {

    chatMessages.innerHTML = `

        <div class="message assistant">

            <div class="avatar">
                AI
            </div>

            <div class="message-content">

                <div class="bubble">

                    <p>
                        Hello! 👋
                    </p>

                    <p>
                        I'm your document AI assistant.
                        Ask me anything about the
                        uploaded documents.
                    </p>

                </div>

            </div>

        </div>

    `;

}