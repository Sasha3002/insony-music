// GROUP CREATE PAGE
function initGroupCreate() {
  const form = document.querySelector('form');
  const submitBtn = document.querySelector('.btn-submit');
  const locationInput = document.getElementById('location');

  if (!form || !submitBtn) return;

  form.addEventListener('submit', function(e) {
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Sprawdzanie lokalizacji...';
    
    // Re-enable after 10 seconds (timeout)
    setTimeout(() => {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Utwórz grupę';
    }, 10000);
  });
}

// SHARED FILE UPLOAD FUNCTIONALITY
function updateFileName(input) {
  const fileName = document.getElementById('file-name');
  if (!fileName) return;
  
  if (input.files && input.files[0]) {
    fileName.textContent = input.files[0].name;
  } else {
    const isEdit = window.location.pathname.includes('/edit/');
    fileName.textContent = isEdit ? 'Nie wybrano nowego pliku' : 'Nie wybrano pliku';
  }
}

// Make it globally accessible for inline onchange handlers
window.updateFileName = updateFileName;

// INITIALIZE ON PAGE LOAD
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('groupCreatePage')) {
    initGroupCreate();
  }
});