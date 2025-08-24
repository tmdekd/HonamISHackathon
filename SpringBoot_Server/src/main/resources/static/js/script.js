async function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (message === '') return;

  const messagesDiv = document.getElementById('messages');
  // 합계 계산

  // 사용자 메시지 추가
  const userDiv = document.createElement('div');
  userDiv.classList.add('message', 'user');
  const userBubble = document.createElement('div');
  userBubble.classList.add('bubble', 'user');
  userBubble.textContent = message;
  userDiv.appendChild(userBubble);

  const userTime = document.createElement('div');
  userTime.classList.add('time');
  userTime.textContent = getTime();
  userDiv.appendChild(userTime);

  messagesDiv.appendChild(userDiv);
  input.value = '';
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  // GPT 스타일 타이핑 표시
  const botDiv = document.createElement('div');
  botDiv.classList.add('message', 'bot');
  const typingBubble = document.createElement('div');
  typingBubble.classList.add('bubble', 'bot');
  typingBubble.innerHTML = '<span class="typing"></span>';
  botDiv.appendChild(typingBubble);
  messagesDiv.appendChild(botDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  try {
    // FastAPI /chatbot 호출
    const response = await fetch('http://localhost:8000/api/chatbot/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();
    const botMessage = data.reply || "응답이 없습니다.";

    // 타이핑 후 실제 메시지 표시
    setTimeout(() => {
      typingBubble.textContent = botMessage;

      const botTime = document.createElement('div');
      botTime.classList.add('time');
      botTime.textContent = getTime();
      botDiv.appendChild(botTime);

      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }, 800); // 타이핑 딜레이
  } catch (error) {
    typingBubble.textContent = "서버와 연결 실패 😢";
    console.error(error);
  }
}

function getTime() {
  const now = new Date();
  return now.getHours().toString().padStart(2,'0') + ":" + now.getMinutes().toString().padStart(2,'0');
}
