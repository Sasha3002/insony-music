
// UTILITY FUNCTIONS
function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}

// PASSWORD TOGGLE
function togglePassword(btn, selector) {
  let input = null;
  if (selector) {
    input = document.querySelector(selector);
  } else if (btn && btn.closest) {
    input = btn.closest('.input-group')?.querySelector('input[type="password"], input[type="text"]');
  }
  if (!input) return;

  const makeVisible = input.type === 'password';
  input.type = makeVisible ? 'text' : 'password';

  const icon = btn.querySelector('i');
  if (icon) {
    icon.classList.toggle('bi-eye', !makeVisible);
    icon.classList.toggle('bi-eye-slash', makeVisible);
  }

  btn.setAttribute('aria-pressed', makeVisible ? 'true' : 'false');
  btn.setAttribute('title', makeVisible ? 'Ukryj hasło' : 'Pokaż hasło');
}

// QUICK REPORT SYSTEM
let currentContentType = '';
let currentContentId = '';

function showQuickReport(contentType, contentId) {
  if (!contentType || !contentId || contentId === 'undefined') {
    alert('Błąd: nieprawidłowe dane treści');
    return;
  }
  
  currentContentType = contentType;
  currentContentId = contentId;
  
  document.getElementById('detailedReportLink').href = `/users/report/${contentType}/${contentId}/`;
  
  document.querySelectorAll('input[name="quickReason"]').forEach(input => {
    input.checked = false;
  });
  
  new bootstrap.Modal(document.getElementById('quickReportModal')).show();
}

async function submitQuickReport() {
  const reason = document.querySelector('input[name="quickReason"]:checked');
  
  if (!reason) {
    alert('Wybierz powód zgłoszenia');
    return;
  }
  
  if (!currentContentType || !currentContentId || currentContentId === 'undefined') {
    alert('Błąd: brak danych do zgłoszenia');
    return;
  }
  
  try {
    const formData = new FormData();
    formData.append('content_type', currentContentType);
    formData.append('content_id', String(currentContentId)); 
    formData.append('reason', reason.value);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    const response = await fetch('/users/report-content/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (data.ok) {
      alert(data.message);
      bootstrap.Modal.getInstance(document.getElementById('quickReportModal')).hide();
    } else {
      alert(data.message || 'Wystąpił błąd');
    }
  } catch (e) {
    console.error('Report error:', e);
    alert('Wystąpił błąd podczas zgłaszania: ' + e.message);
  }
}


// ACTIVE NAV LINK HIGHLIGHTING
document.addEventListener('DOMContentLoaded', function() {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});