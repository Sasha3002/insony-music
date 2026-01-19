// EVENT CREATE PAGE
function initEventCreate() {
  const dateInput = document.getElementById('event_date');
  const endDateInput = document.getElementById('end_date');
  
  if (!dateInput) return;

  // Set minimum date to today
  const now = new Date();
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
  dateInput.min = now.toISOString().slice(0, 16);

  // Set end date minimum to start date
  dateInput.addEventListener('change', function() {
    const startDate = dateInput.value;
    if (startDate) {
      endDateInput.min = startDate;
    }
  });
}

// EVENT DETAIL PAGE
function initEventDetail() {
  const starRating = document.querySelector('.star-rating');
  if (!starRating) return;

  const stars = document.querySelectorAll('.star-label');
  const radios = document.querySelectorAll('input[name="rating"]');

  stars.forEach((star, index) => {
    star.addEventListener('mouseenter', function() {
      highlightStars(index + 1);
    });
  });

  // Reset on mouse leave
  starRating.addEventListener('mouseleave', function() {
    const checkedRadio = document.querySelector('input[name="rating"]:checked');
    if (checkedRadio) {
      const rating = parseInt(checkedRadio.value);
      highlightStars(rating);
    } else {
      highlightStars(0);
    }
  });

  radios.forEach(radio => {
    radio.addEventListener('change', function() {
      highlightStars(parseInt(this.value));
    });
  });

  const checkedRadio = document.querySelector('input[name="rating"]:checked');
  if (checkedRadio) {
    highlightStars(parseInt(checkedRadio.value));
  }

  function highlightStars(rating) {
    stars.forEach((star, index) => {
      if (index < rating) {
        star.style.color = '#fbbf24';
      } else {
        star.style.color = '#6b7280';
      }
    });
  }
}

// POLL CREATE PAGE
function initPollCreate() {
  const pollTypeSelect = document.getElementById('poll_type');
  
  if (!pollTypeSelect) return;

  const dateFields = document.getElementById('dateFields');
  const timeFields = document.getElementById('timeFields');
  const locationFields = document.getElementById('locationFields');
  const otherFields = document.getElementById('otherFields');

  pollTypeSelect.addEventListener('change', function() {
    dateFields.classList.remove('active');
    timeFields.classList.remove('active');
    locationFields.classList.remove('active');
    otherFields.classList.remove('active');

    // Show relevant fields
    switch(this.value) {
      case 'date':
        dateFields.classList.add('active');
        break;
      case 'time':
        timeFields.classList.add('active');
        break;
      case 'location':
        locationFields.classList.add('active');
        break;
      case 'other':
        otherFields.classList.add('active');
        break;
    }
  });

  // Set minimum date/time to now
  const now = new Date();
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
  const minDateTime = now.toISOString().slice(0, 16);
  
  const closesAtInput = document.getElementById('closes_at');
  const proposedDateInput = document.getElementById('proposed_date');
  const proposedTimeInput = document.getElementById('proposed_time');
  const proposedEndDateInput = document.getElementById('proposed_end_date');
  const proposedEndTimeInput = document.getElementById('proposed_end_time');
  
  if (closesAtInput) closesAtInput.min = minDateTime;
  if (proposedDateInput) proposedDateInput.min = minDateTime;
  if (proposedTimeInput) proposedTimeInput.min = minDateTime;
  if (proposedEndDateInput) proposedEndDateInput.min = minDateTime;
  if (proposedEndTimeInput) proposedEndTimeInput.min = minDateTime;
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

window.updateFileName = updateFileName;

// INITIALIZE ON PAGE LOAD
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('eventCreatePage')) {
    initEventCreate();
  } else if (document.getElementById('eventDetailPage')) {
    initEventDetail();
  } else if (document.getElementById('pollCreatePage')) {
    initPollCreate();
  }
});