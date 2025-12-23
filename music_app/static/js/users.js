// UTILITY FUNCTIONS
function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}

// ACCOUNT DELETE PAGE
function initAccountDelete() {
  const form = document.getElementById('deleteForm');
  const passwordInput = document.getElementById('password-input');
  const confirmInput = document.getElementById('confirm-input');
  const deleteBtn = document.getElementById('deleteBtn');

  if (!form) return;

  function checkForm() {
    const password = passwordInput.value;
    const confirmText = confirmInput.value;
    
    // Enable button only if both fields are filled
    if (password && confirmText === 'USUŃ KONTO') {
      deleteBtn.disabled = false;
    } else {
      deleteBtn.disabled = true;
    }
  }

  passwordInput.addEventListener('input', checkForm);
  confirmInput.addEventListener('input', checkForm);

  form.addEventListener('submit', function(e) {
    const confirmText = confirmInput.value;
    
    if (confirmText !== 'USUŃ KONTO') {
      e.preventDefault();
      alert('Musisz wpisać dokładnie: USUŃ KONTO');
      return;
    }

    if (!confirm('Czy NA PEWNO chcesz usunąć swoje konto? Tej operacji nie można cofnąć!')) {
      e.preventDefault();
      return;
    }
  });
}

// BLOCKED USERS PAGE


function initBlockedUsers() {
  window.unblockUser = async function(username, btn) {
    if (!confirm(`Czy na pewno chcesz odblokować użytkownika ${username}?`)) {
      return;
    }
    
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Odblokowywanie...';
    
    try {
      const resp = await fetch(`/users/u/${username}/unblock/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      const data = await resp.json();
      
      if (data.ok) {
        const userItem = btn.closest('.blocked-user-item');
        userItem.style.opacity = '0';
        userItem.style.transform = 'translateX(-30px)';
        
        setTimeout(() => {
          userItem.remove();
          
          const list = document.getElementById('blockedUsersList');
          if (list && list.children.length === 0) {
            window.location.reload();
          }
        }, 300);
        
        alert(data.message);
      } else {
        alert(data.message || 'Wystąpił błąd');
        btn.disabled = false;
        btn.innerHTML = originalHTML;
      }
    } catch (e) {
      console.error(e);
      alert('Wystąpił błąd podczas odblokowywania');
      btn.disabled = false;
      btn.innerHTML = originalHTML;
    }
  };
}

// PROFILE PAGE
function initProfile() {
  // Animate XP bar on load
  const fill = document.getElementById('xpFill');
  const tip = document.getElementById('xpTip');
  
  if (!fill || !tip) return;

  // Get target % from data attribute
  const target = parseFloat(fill.dataset.target || '0');
  const clamp = v => Math.max(0, Math.min(100, v));

  // Animate on load
  requestAnimationFrame(() => {
    fill.style.setProperty('--xp-pct', clamp(target) + '%');
    tip.textContent = Math.round(clamp(target)) + '%';
    tip.style.left = clamp(target) + '%';
  });

  // Mouse hover to show tooltip position
  fill.parentElement.addEventListener('mousemove', (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const pct = clamp(((e.clientX - rect.left) / rect.width) * 100);
    tip.style.left = pct + '%';
  });
}

// PROFILE EDIT PAGE
function initProfileEdit() {
  // Get all genres and artists from data attributes
  const genresData = document.getElementById('genresData');
  const artistsData = document.getElementById('artistsData');
  
  if (!genresData || !artistsData) return;

  const allGenres = JSON.parse(genresData.textContent);
  const allArtists = JSON.parse(artistsData.textContent);

  // Generic autocomplete class
  class Autocomplete {
    constructor(inputId, dropdownId, tagsId, hiddenId, allItems, icon) {
      this.input = document.getElementById(inputId);
      this.dropdown = document.getElementById(dropdownId);
      this.tagsContainer = document.getElementById(tagsId);
      this.hiddenInput = document.getElementById(hiddenId);
      this.allItems = allItems;
      this.icon = icon;
      this.selectedItems = [];
      
      this.init();
    }

    init() {
      // Load initial selected items
      const initialValue = this.hiddenInput.value;
      if (initialValue) {
        this.selectedItems = initialValue.split(',').map(i => i.trim()).filter(i => i);
        this.renderTags();
      }

      // Input events
      this.input.addEventListener('input', () => this.handleInput());
      this.input.addEventListener('focus', () => this.handleInput());
      
      // Click outside to close
      document.addEventListener('click', (e) => {
        if (!this.input.contains(e.target) && !this.dropdown.contains(e.target)) {
          this.dropdown.classList.remove('show');
        }
      });
    }

    handleInput() {
      const query = this.input.value.trim().toLowerCase();
      
      if (query.length === 0) {
        this.dropdown.classList.remove('show');
        return;
      }

      // Filter items
      const filtered = this.allItems.filter(item => 
        item.toLowerCase().includes(query) && !this.selectedItems.includes(item)
      );

      this.renderDropdown(filtered);
    }

    renderDropdown(items) {
      if (items.length === 0) {
        this.dropdown.innerHTML = '<div class="autocomplete-empty">Nie znaleziono wyników</div>';
        this.dropdown.classList.add('show');
        return;
      }

      this.dropdown.innerHTML = items.slice(0, 10).map(item => `
        <div class="autocomplete-item" data-value="${item}">
          <i class="bi ${this.icon}"></i>
          ${item}
        </div>
      `).join('');

      // Add click handlers
      this.dropdown.querySelectorAll('.autocomplete-item').forEach(el => {
        el.addEventListener('click', () => {
          this.addItem(el.dataset.value);
        });
      });

      this.dropdown.classList.add('show');
    }

    addItem(item) {
      if (!this.selectedItems.includes(item)) {
        this.selectedItems.push(item);
        this.updateHidden();
        this.renderTags();
      }
      
      this.input.value = '';
      this.dropdown.classList.remove('show');
      this.input.focus();
    }

    removeItem(item) {
      this.selectedItems = this.selectedItems.filter(i => i !== item);
      this.updateHidden();
      this.renderTags();
    }

    updateHidden() {
      this.hiddenInput.value = this.selectedItems.join(', ');
    }

    renderTags() {
      if (this.selectedItems.length === 0) {
        this.tagsContainer.innerHTML = '<span class="text-muted small">Nie wybrano żadnych pozycji</span>';
        return;
      }

      this.tagsContainer.innerHTML = this.selectedItems.map(item => `
        <span class="selected-tag">
          <i class="bi ${this.icon}"></i>
          ${item}
          <span class="tag-remove" data-value="${item}">×</span>
        </span>
      `).join('');

      // Add remove handlers
      this.tagsContainer.querySelectorAll('.tag-remove').forEach(el => {
        el.addEventListener('click', () => {
          this.removeItem(el.dataset.value);
        });
      });
    }
  }

  // Initialize autocompletes
  new Autocomplete(
    'genres-search',
    'genres-dropdown',
    'genres-tags',
    'genres-hidden',
    allGenres,
    'bi-music-note'
  );

  new Autocomplete(
    'artists-search',
    'artists-dropdown',
    'artists-tags',
    'artists-hidden',
    allArtists,
    'bi-person'
  );

  // Bio character counter
  const bioInput = document.getElementById('bio-input');
  const bioCount = document.getElementById('bio-count');
  
  if (bioInput && bioCount) {
    const updateBioCount = () => {
      bioCount.textContent = bioInput.value.length;
    };
    updateBioCount();
    bioInput.addEventListener('input', updateBioCount);
  }

  // Form validation on submit
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', (e) => {
      const email = form.querySelector('[name="email"]');
      if (!email.value.trim()) {
        e.preventDefault();
        alert('Email jest wymagany');
        email.focus();
      }
    });
  }

  // Profile picture preview
  const pictureUpload = document.getElementById('picture-upload');
  const avatarPreview = document.getElementById('avatar-preview');
  const removeButton = document.getElementById('remove-picture');
  
  if (pictureUpload && avatarPreview) {
    pictureUpload.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          avatarPreview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (removeButton) {
    removeButton.addEventListener('click', function() {
      if (confirm('Czy na pewno chcesz usunąć zdjęcie profilowe?')) {
        // Create hidden input to signal removal
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'remove_picture';
        input.value = 'true';
        document.querySelector('form').appendChild(input);
        document.querySelector('form').submit();
      }
    });
  }
}

// PUBLIC PROFILE PAGE
function initPublicProfile() {
  window.toggleFollow = async function() {
    const btn = document.getElementById('followBtn');
    const text = document.getElementById('followText');
    const icon = btn.querySelector('i');
    const username = btn.dataset.username;
    
    btn.disabled = true;
    
    try {
      const resp = await fetch(`/users/u/${username}/follow/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      const data = await resp.json();
      
      if (data.ok) {
        if (data.is_following) {
          btn.className = 'btn btn-success';
          icon.className = 'bi bi-check-circle';
          text.textContent = 'Obserwujesz';
        } else {
          btn.className = 'btn btn-primary';
          icon.className = 'bi bi-plus-circle';
          text.textContent = 'Obserwuj';
        }
        const followersCount = document.getElementById('followersCount');
        if (followersCount) {
          followersCount.textContent = data.followers_count;
        }
      }
      
      btn.disabled = false;
    } catch (e) {
      console.error(e);
      btn.disabled = false;
    }
  };

  window.toggleBlock = async function() {
    const btn = document.querySelector('[onclick*="toggleBlock"]');
    const username = btn.dataset.username;
    
    if (!confirm('Czy na pewno chcesz zablokować tego użytkownika?')) {
      return;
    }
    
    try {
      const resp = await fetch(`/users/u/${username}/block/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      const data = await resp.json();
      
      if (data.ok) {
        alert(data.message);
        if (data.is_blocked) {
          window.location.href = '/users/search/';
        }
      }
    } catch (e) {
      console.error(e);
    }
  };
}

// USER SEARCH PAGE
function initUserSearch() {
  window.toggleFollow = async function(username, btn) {
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    
    try {
      const resp = await fetch(`/users/u/${username}/follow/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      const data = await resp.json();
      
      if (data.ok) {
        if (data.is_following) {
          btn.classList.add('following');
          btn.innerHTML = '<i class="bi bi-check-circle"></i> Obserwujesz';
        } else {
          btn.classList.remove('following');
          btn.innerHTML = '<i class="bi bi-plus-circle"></i> Obserwuj';
        }
      } else {
        alert(data.message || 'Wystąpił błąd');
      }
      
      btn.disabled = false;
    } catch (e) {
      console.error(e);
      btn.disabled = false;
      btn.innerHTML = originalHTML;
    }
  };

  window.toggleBlock = async function(username, btn) {
    if (!confirm('Czy na pewno chcesz zablokować tego użytkownika?')) {
      return;
    }
    
    btn.disabled = true;
    
    try {
      const resp = await fetch(`/users/u/${username}/block/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      const data = await resp.json();
      
      if (data.ok) {
        alert(data.message);
        // Remove user card
        btn.closest('.user-card').style.opacity = '0';
        setTimeout(() => {
          btn.closest('.user-card').remove();
        }, 300);
      } else {
        alert(data.message || 'Wystąpił błąd');
        btn.disabled = false;
      }
    } catch (e) {
      console.error(e);
      alert('Wystąpił błąd');
      btn.disabled = false;
    }
  };
}

// INITIALIZE ON PAGE LOAD
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('accountDeletePage')) {
    initAccountDelete();
  } else if (document.getElementById('blockedUsersPage')) {
    initBlockedUsers();
  } else if (document.getElementById('profilePage')) {
    initProfile();
  } else if (document.getElementById('profileEditPage')) {
    initProfileEdit();
  } else if (document.getElementById('publicProfilePage')) {
    initPublicProfile();
  } else if (document.getElementById('userSearchPage')) {
    initUserSearch();
  }
});