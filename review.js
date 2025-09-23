let allReviews = [];

// Fetch all reviews from a single JSON file
fetch('./slu.json')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    allReviews = data;
    // Optionally show first business’s reviews on load:
    // loadReviewsForBusiness('Blueprint Coffee');
  })
  .catch(error => console.error('Error loading reviews:', error));

// Function to load reviews for a specific business
function loadReviewsForBusiness(businessName) {
  const container = document.getElementById('review-container');
  const title = document.getElementById('reviews-title');
  container.innerHTML = '';
  title.textContent = `Reviews for ${businessName}`;

  const reviews = allReviews.filter(r => r.business === businessName);

  if (reviews.length === 0) {
    container.innerHTML = `<p>No reviews yet.</p>`;
    return;
  }

  reviews.forEach(r => {
    const div = document.createElement('div');
    div.classList.add('review-card');
    div.innerHTML = `
      <p><strong>${r.reviewer}</strong> (${r.date}) ★${r.rating}</p>
      <p>${r.text}</p>
    `;
    container.appendChild(div);
  });
}

// Add click listener to each business card
document.querySelectorAll('.business-card').forEach(card => {
  card.addEventListener('click', () => {
    const businessName = card.dataset.business;
    loadReviewsForBusiness(businessName);
  });
});

// Optional: highlight filter buttons on click
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('active');
    console.log(`Filter clicked: ${btn.dataset.category || btn.dataset.price || btn.dataset.rating}`);
  });
});
