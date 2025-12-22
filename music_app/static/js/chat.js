// UTILITY FUNCTIONS

function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}

function scrollToBottom(container) {
  container.scrollTop = container.scrollHeight;
}

// CHAT LIST FUNCTIONS

function initChatList() {
  function updateUnreadCounts() {
    const unreadCountsUrl = document.getElementById('unreadCountsUrl')?.value;
    if (!unreadCountsUrl) return;

    fetch(unreadCountsUrl)
      .then(response => response.json())
      .then(data => {
        if (data.ok) {
          data.conversations.forEach(conv => {
            const card = document.querySelector(`a[href*="conversation/${conv.conversation_id}/"]`);
            if (!card) return;
            
            const metaDiv = card.querySelector('.conversation-meta');
            const previewDiv = card.querySelector('.conversation-preview');
            const timeDiv = card.querySelector('.conversation-time');
            const oldBadge = metaDiv.querySelector('.unread-badge');
            
            if (oldBadge) oldBadge.remove();
            
            if (conv.unread_count > 0) {
              const badge = document.createElement('div');
              badge.className = 'unread-badge';
              badge.textContent = conv.unread_count;
              metaDiv.insertBefore(badge, metaDiv.firstChild);
              card.classList.add('has-unread');
            } else {
              card.classList.remove('has-unread');
            }
            
            if (conv.last_message) {
              const prefix = conv.last_message.is_own ? 'Ty: ' : '';
              const truncated = conv.last_message.content.substring(0, 47);
              const display = truncated.length < conv.last_message.content.length 
                ? truncated + '...' 
                : truncated;
              previewDiv.textContent = prefix + display;
              
              if (timeDiv) {
                timeDiv.textContent = conv.last_message.time;
              }
            }
          });
        }
      })
      .catch(error => console.error('Polling error:', error));
  }

  setInterval(updateUnreadCounts, 5000);
}
// GROUP CHAT FUNCTIONS

function initGroupChat() {
  const messagesContainer = document.getElementById('messagesContainer');
  const messageForm = document.getElementById('messageForm');
  const messageInput = document.getElementById('messageInput');
  const sendBtn = document.getElementById('sendBtn');
  const groupId = document.getElementById('groupId')?.value;
  const sendMessageUrl = document.getElementById('sendMessageUrl')?.value;
  const pollMessagesUrl = document.getElementById('pollMessagesUrl')?.value;
  const deleteMessageUrlTemplate = document.getElementById('deleteMessageUrlTemplate')?.value;
  
  if (!messagesContainer || !messageForm) return;

  scrollToBottom(messagesContainer);
  messageInput?.focus();

  let lastMessageId = parseInt(document.getElementById('lastMessageId')?.value || 0);
  let pollInterval;

  // Send message
  messageForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const content = messageInput.value.trim();
    if (!content) return;

    sendBtn.disabled = true;
    messageInput.disabled = true;

    try {
      const formData = new FormData();
      formData.append('group_id', groupId);
      formData.append('content', content);
      formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

      const response = await fetch(sendMessageUrl, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });

      const data = await response.json();
      
      if (data.ok) {
        const userAvatar = document.getElementById('userAvatar')?.value || '';
        const username = document.getElementById('username')?.value || '';
        const canDelete = document.getElementById('canDeleteOwn')?.value === 'true';
        
        const messageHTML = `
          <div class="message own" data-message-id="${data.message.id}">
            <div class="message-avatar">
              ${userAvatar 
                ? `<img src="${userAvatar}" alt="${username}">` 
                : `<div class="avatar-placeholder">${username.charAt(0).toUpperCase()}</div>`
              }
            </div>
            <div class="message-content-wrapper">
              <div class="message-content">
                ${data.message.content.replace(/\n/g, '<br>')}
                ${canDelete ? `<button class="message-delete-btn" onclick="deleteMessage(${data.message.id})" title="Usuń wiadomość">
                  <i class="bi bi-x"></i>
                </button>` : ''}
                <div class="message-time">${data.message.created_at}</div>
              </div>
            </div>
          </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messageInput.value = '';
        scrollToBottom(messagesContainer);
        lastMessageId = data.message.id;
      } else {
        alert(data.message || 'Błąd podczas wysyłania wiadomości');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Błąd podczas wysyłania wiadomości');
    } finally {
      sendBtn.disabled = false;
      messageInput.disabled = false;
      messageInput.focus();
    }
  });

  // Delete message (global function)
  window.deleteMessage = async function(messageId) {
    if (!confirm('Czy na pewno chcesz usunąć tę wiadomość?')) return;
    
    try {
      const formData = new FormData();
      formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
      
      const deleteUrl = deleteMessageUrlTemplate.replace('0', messageId);
      
      const response = await fetch(deleteUrl, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      
      const data = await response.json();
      
      if (data.ok) {
        document.querySelector(`[data-message-id="${messageId}"]`)?.remove();
      } else {
        alert(data.message || 'Błąd podczas usuwania wiadomości');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Błąd podczas usuwania wiadomości');
    }
  };

  // Poll for new messages
  function pollNewMessages() {
    fetch(`${pollMessagesUrl}?last_message_id=${lastMessageId}`)
      .then(response => response.json())
      .then(data => {
        if (data.ok && data.messages.length > 0) {
          data.messages.forEach(msg => {
            const messageHTML = `
              <div class="message" data-message-id="${msg.id}">
                <div class="message-avatar">
                  ${msg.sender_picture 
                    ? `<img src="${msg.sender_picture}" alt="${msg.sender}">` 
                    : `<div class="avatar-placeholder">${msg.sender.charAt(0).toUpperCase()}</div>`
                  }
                </div>
                <div class="message-content-wrapper">
                  <div class="message-sender-name">${msg.sender}</div>
                  <div class="message-content">
                    ${msg.content.replace(/\n/g, '<br>')}
                    <div class="message-time">${msg.created_at}</div>
                  </div>
                </div>
              </div>
            `;
            
            messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
            lastMessageId = msg.id;
          });
          
          scrollToBottom(messagesContainer);
        }
      })
      .catch(error => console.error('Polling error:', error));
  }

  pollInterval = setInterval(pollNewMessages, 3000);
  window.addEventListener('beforeunload', () => clearInterval(pollInterval));
}

// CONVERSATION DETAIL FUNCTIONS

function initConversationDetail() {
  const messagesContainer = document.getElementById('messagesContainer');
  const messageForm = document.getElementById('messageForm');
  const messageInput = document.getElementById('messageInput');
  const sendBtn = document.getElementById('sendBtn');
  const conversationId = document.getElementById('conversationId')?.value;
  const sendMessageUrl = document.getElementById('sendMessageUrl')?.value;
  const pollMessagesUrl = document.getElementById('pollMessagesUrl')?.value;
  
  if (!messagesContainer || !messageForm) return;

  scrollToBottom(messagesContainer);
  messageInput?.focus();

  let lastMessageId = parseInt(document.getElementById('lastMessageId')?.value || 0);
  let pollInterval;

  // Send message
  messageForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const content = messageInput.value.trim();
    if (!content) return;

    sendBtn.disabled = true;
    messageInput.disabled = true;

    try {
      const formData = new FormData();
      formData.append('conversation_id', conversationId);
      formData.append('content', content);
      formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

      const response = await fetch(sendMessageUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      const data = await response.json();
      
      if (data.ok) {
        const userAvatar = document.getElementById('userAvatar')?.value || '';
        const username = document.getElementById('username')?.value || '';
        
        const messageHTML = `
          <div class="message own" data-message-id="${data.message.id}">
            <div class="message-avatar">
              ${userAvatar 
                ? `<img src="${userAvatar}" alt="${username}">` 
                : `<div class="avatar-placeholder">${username.charAt(0).toUpperCase()}</div>`
              }
            </div>
            <div class="message-content">
              ${data.message.content.replace(/\n/g, '<br>')}
              <div class="message-time">${data.message.created_at}</div>
            </div>
          </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messageInput.value = '';
        scrollToBottom(messagesContainer);
      } else {
        alert(data.message || 'Błąd podczas wysyłania wiadomości');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Błąd podczas wysyłania wiadomości');
    } finally {
      sendBtn.disabled = false;
      messageInput.disabled = false;
      messageInput.focus();
    }
  });

  // Poll for new messages
  function pollNewMessages() {
    fetch(`${pollMessagesUrl}?last_message_id=${lastMessageId}`)
      .then(response => response.json())
      .then(data => {
        if (data.ok && data.messages.length > 0) {
          data.messages.forEach(msg => {
            const messageHTML = `
              <div class="message" data-message-id="${msg.id}">
                <div class="message-avatar">
                  ${msg.sender_picture 
                    ? `<img src="${msg.sender_picture}" alt="${msg.sender}">` 
                    : `<div class="avatar-placeholder">${msg.sender.charAt(0).toUpperCase()}</div>`
                  }
                </div>
                <div class="message-content">
                  ${msg.content.replace(/\n/g, '<br>')}
                  <div class="message-time">${msg.created_at}</div>
                </div>
              </div>
            `;
            
            messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
            lastMessageId = msg.id;
          });
          
          scrollToBottom(messagesContainer);
        }
      })
      .catch(error => console.error('Polling error:', error));
  }
  
  pollInterval = setInterval(pollNewMessages, 3000);
  
  window.addEventListener('beforeunload', () => {
    clearInterval(pollInterval);
  });
}

// INITIALIZATION

document.addEventListener('DOMContentLoaded', function() {
  // Check which page we're on and initialize accordingly
  if (document.getElementById('chatListPage')) {
    initChatList();
  } else if (document.getElementById('conversationDetailPage')) {
    initConversationDetail();
  } else if (document.getElementById('groupChatPage')) {
    initGroupChat();
  }
});