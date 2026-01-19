// UTILITY FUNCTIONS
function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}

// PLAYLIST CREATE PAGE
function initPlaylistCreate() {
  const coverUpload = document.getElementById('cover-upload');
  const coverPreview = document.getElementById('cover-preview');
  const nameInput = document.getElementById('name-input');
  const nameCount = document.getElementById('name-count');
  const descInput = document.getElementById('description-input');
  const descCount = document.getElementById('description-count');
  const form = document.querySelector('form');

  // Cover preview
  if (coverUpload && coverPreview) {
    coverUpload.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          coverPreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Name character counter
  if (nameInput && nameCount) {
    const updateNameCount = () => {
      nameCount.textContent = nameInput.value.length;
    };
    nameInput.addEventListener('input', updateNameCount);
  }

  // Description character counter
  if (descInput && descCount) {
    const updateDescCount = () => {
      descCount.textContent = descInput.value.length;
    };
    descInput.addEventListener('input', updateDescCount);
  }

  // Form validation
  if (form) {
    form.addEventListener('submit', (e) => {
      const name = nameInput.value.trim();
      if (!name) {
        e.preventDefault();
        alert('Nazwa playlisty jest wymagana');
        nameInput.focus();
      }
    });
  }
}

// PLAYLIST EDIT PAGE
function initPlaylistEdit() {
  const coverUpload = document.getElementById('cover-upload');
  const coverPreview = document.getElementById('cover-preview');
  const removeCoverBtn = document.getElementById('remove-cover-btn');
  const removeCoverInput = document.getElementById('remove-cover-input');
  const nameInput = document.getElementById('name-input');
  const nameCount = document.getElementById('name-count');
  const descInput = document.getElementById('description-input');
  const descCount = document.getElementById('description-count');

  // Cover preview
  if (coverUpload && coverPreview) {
    coverUpload.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          coverPreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Remove cover button
  if (removeCoverBtn && removeCoverInput) {
    removeCoverBtn.addEventListener('click', function() {
      if (confirm('Czy na pewno chcesz usunąć okładkę?')) {
        removeCoverInput.value = 'true';
        coverPreview.innerHTML = '<i class="bi bi-music-note-list"></i>';
        removeCoverBtn.style.display = 'none';
      }
    });
  }

  // Name character counter
  if (nameInput && nameCount) {
    const updateNameCount = () => {
      nameCount.textContent = nameInput.value.length;
    };
    updateNameCount(); 
    nameInput.addEventListener('input', updateNameCount);
  }

  // Description character counter
  if (descInput && descCount) {
    const updateDescCount = () => {
      descCount.textContent = descInput.value.length;
    };
    updateDescCount(); 
    descInput.addEventListener('input', updateDescCount);
  }
}

// PLAYLIST DETAIL PAGE
function initPlaylistDetail() {
  window.removeFromPlaylist = async function(playlistId, trackId) {
    if (!confirm('Czy na pewno chcesz usunąć ten utwór z playlisty?')) {
      return;
    }

    try {
      const resp = await fetch(`/playlists/${playlistId}/remove/${trackId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      const data = await resp.json();
      
      if (data.ok) {
        window.location.reload();
      } else {
        alert(data.message || 'Wystąpił błąd');
      }
    } catch (e) {
      console.error('Error:', e);
      alert('Wystąpił błąd podczas usuwania utworu');
    }
  };
}

// TRACK DETAIL PAGE
function initTrackDetail() {
  const csrftoken = getCookie('csrftoken');
  initReviewSliders();
  initCharacterCounters();
  initReviewLikes(csrftoken);
  initFavoriteToggle(csrftoken);
  animateCriteriaBars();
  initPlaylistActions(csrftoken);
}

function initReviewSliders() {
  const sliders = document.querySelectorAll('#crit-form .form-range');
  const totalEl = document.getElementById('total-current');

  function recomputeTotal() {
    let sum = 0;
    sliders.forEach(sl => sum += Number(sl.value) || 0);
    const total100 = Math.round((sum / 60) * 100);
    if (totalEl) totalEl.textContent = total100;
  }

  sliders.forEach(function(sl) {
    const key = sl.dataset.target;
    const val = document.getElementById(key + '-val');

    const update = () => {
      const v = Number(sl.value) || 0;
      if (val) val.textContent = v;
      recomputeTotal();
    };

    update();
    sl.addEventListener('input', update);
  });

  recomputeTotal();
}

function initCharacterCounters() {
  // Title counter
  const titleInput = document.querySelector('.insony-title-input');
  const titleCount = document.getElementById('title-count');
  if (titleInput && titleCount) {
    const upd = () => titleCount.textContent = (titleInput.value || '').length;
    upd();
    titleInput.addEventListener('input', upd);
  }

  // Text counter
  const textArea = document.querySelector('#crit-form textarea');
  const textCount = document.getElementById('text-count');
  if (textArea && textCount) {
    const upd = () => textCount.textContent = (textArea.value || '').length;
    upd();
    textArea.addEventListener('input', upd);
  }
}

function initReviewLikes(csrftoken) {
  document.querySelectorAll('.js-like').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const reviewId = btn.dataset.reviewId;
      if (!reviewId) return;

      const isAuthenticated = btn.dataset.authenticated === 'true';
      if (!isAuthenticated) {
        window.location.href = btn.dataset.loginUrl;
        return;
      }

      try {
        const resp = await fetch(`/reviews/${reviewId}/like/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        if (resp.status === 401 || resp.status === 403) {
          window.location.href = btn.dataset.loginUrl;
          return;
        }

        const data = await resp.json();
        if (!data || !data.ok) return;

        const countEl = document.getElementById(`like-count-${reviewId}`);
        const icon = btn.querySelector('i');

        if (data.liked) {
          btn.classList.add('is-liked');
          btn.setAttribute('aria-pressed', 'true');
          if (icon) {
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill');
          }
        } else {
          btn.classList.remove('is-liked');
          btn.setAttribute('aria-pressed', 'false');
          if (icon) {
            icon.classList.remove('bi-heart-fill');
            icon.classList.add('bi-heart');
          }
        }
        if (countEl) countEl.textContent = data.count;

      } catch (e) {
        console.error('Like error:', e);
      }
    });
  });
}

function initFavoriteToggle(csrftoken) {
  const favBtn = document.querySelector('.js-fav');
  if (!favBtn) return;

  favBtn.addEventListener('click', async () => {
    const trackId = favBtn.dataset.trackId;
    const loginUrl = favBtn.dataset.loginUrl;

    try {
      const resp = await fetch(`/favorite/${trackId}/toggle/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (resp.status === 401 || resp.status === 403) {
        window.location.href = loginUrl;
        return;
      }

      const data = await resp.json();
      if (!data.ok) return;

      const pressed = data.favorited === true;
      favBtn.setAttribute('aria-pressed', pressed ? 'true' : 'false');

      const icon = favBtn.querySelector('i');
      const text = pressed ? 'Ulubiony' : 'Dodaj do ulubionych';
      
      if (icon) {
        if (pressed) {
          icon.classList.remove('bi-heart');
          icon.classList.add('bi-heart-fill');
        } else {
          icon.classList.remove('bi-heart-fill');
          icon.classList.add('bi-heart');
        }
      }
      
      favBtn.innerHTML = `<i class="bi bi-heart${pressed ? '-fill' : ''}"></i> ${text}`;

      favBtn.classList.add('btn-success');
      setTimeout(() => favBtn.classList.remove('btn-success'), 300);

    } catch (e) {
      console.error(e);
    }
  });
}

function animateCriteriaBars() {
  const fills = document.querySelectorAll('.criterion-fill');
  fills.forEach(fill => {
    const targetWidth = fill.style.width;
    fill.style.width = '0%';
    setTimeout(() => {
      fill.style.width = targetWidth;
    }, 100);
  });
}

function initPlaylistActions(csrftoken) {
  const addButtons = document.querySelectorAll('.add-to-playlist');
  const removeButtons = document.querySelectorAll('.remove-from-playlist');
  const messageDiv = document.getElementById('playlistMessage');
  
  // Add to playlist
  addButtons.forEach(btn => {
    btn.addEventListener('click', async function(e) {
      e.stopPropagation();
      if (this.disabled) return;
      
      const playlistId = this.dataset.playlistId;
      const trackId = this.dataset.trackId;
      this.disabled = true;
      
      try {
        const resp = await fetch(`/playlists/${playlistId}/add/${trackId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          }
        });
        
        const data = await resp.json();
        
        if (data.ok) {
          showPlaylistMessage('success', data.message || 'Utwór dodany!');
          
          // Update count
          const playlistItem = this.closest('.playlist-list-item');
          const countSpan = playlistItem.querySelector('.track-count');
          if (countSpan) {
            const match = countSpan.textContent.match(/\d+/);
            if (match) {
              const newCount = parseInt(match[0]) + 1;
              countSpan.textContent = `${newCount} utwor${newCount === 1 ? '' : newCount < 5 ? 'y' : 'ów'}`;
            }
          }
          
          // Change icon
          this.querySelector('i').className = 'bi bi-check-circle-fill';
        } else {
          showPlaylistMessage('warning', data.message || 'Nie udało się dodać');
        }
        
        this.disabled = false;
      } catch (error) {
        showPlaylistMessage('error', 'Wystąpił błąd');
        this.disabled = false;
      }
    });
  });
  
  // Remove from playlist
  removeButtons.forEach(btn => {
    btn.addEventListener('click', async function(e) {
      e.stopPropagation();
      if (this.disabled) return;
      
      const playlistId = this.dataset.playlistId;
      const trackId = this.dataset.trackId;
      this.disabled = true;
      
      try {
        const resp = await fetch(`/playlists/${playlistId}/remove/${trackId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          }
        });
        
        const data = await resp.json();
        
        if (data.ok) {
          showPlaylistMessage('success', 'Utwór usunięty!');
          
          // Update count
          const playlistItem = this.closest('.playlist-list-item');
          const countSpan = playlistItem.querySelector('.track-count');
          if (countSpan) {
            const match = countSpan.textContent.match(/\d+/);
            if (match) {
              const newCount = Math.max(0, parseInt(match[0]) - 1);
              countSpan.textContent = `${newCount} utwor${newCount === 1 ? '' : newCount < 5 ? 'y' : 'ów'}`;
            }
          }
        } else {
          showPlaylistMessage('warning', data.message || 'Nie udało się usunąć');
        }
        
        this.disabled = false;
      } catch (error) {
        showPlaylistMessage('error', 'Wystąpił błąd');
        this.disabled = false;
      }
    });
  });
  
  function showPlaylistMessage(type, message) {
    if (!messageDiv) return;
    messageDiv.className = `playlist-message ${type}`;
    messageDiv.textContent = message;
    messageDiv.classList.remove('d-none');
    
    setTimeout(() => {
      messageDiv.classList.add('d-none');
    }, 3000);
  }
}

// TRACK LIST PAGE
function initTrackList() {
  // Clear search button
  const clearBtn = document.querySelector('.insony-search .clear-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      const form = clearBtn.closest('form');
      const input = form.querySelector('.search-input');
      input.value = '';
      form.submit();
    });
  }

  // Animate rating bars on load
  const fills = document.querySelectorAll('.rating-fill');
  fills.forEach(fill => {
    const targetWidth = fill.style.width;
    fill.style.width = '0%';
    setTimeout(() => {
      fill.style.width = targetWidth;
    }, 100);
  });

  window.toggleFavorite = function(button, trackId) {
    fetch(`/favorite/${trackId}/toggle/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.ok) {
        const icon = button.querySelector('i');
        if (data.favorited) {
          button.classList.add('favorited');
          icon.classList.remove('bi-heart');
          icon.classList.add('bi-heart-fill');
        } else {
          button.classList.remove('favorited');
          icon.classList.remove('bi-heart-fill');
          icon.classList.add('bi-heart');
        }
      }
    })
    .catch(error => console.error('Error:', error));
  };
}

// INITIALIZE ON PAGE LOAD
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('playlistCreatePage')) {
    initPlaylistCreate();
  } else if (document.getElementById('playlistEditPage')) {
    initPlaylistEdit();
  } else if (document.getElementById('playlistDetailPage')) {
    initPlaylistDetail();
  } else if (document.getElementById('trackDetailPage')) {
    initTrackDetail();
  } else if (document.getElementById('trackListPage')) {
    initTrackList();
  }
});