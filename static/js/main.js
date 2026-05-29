document.addEventListener('DOMContentLoaded', () => {
  // ─── 1. Mobile Menu Toggle ───
  const hamburger = document.getElementById('nav-hamburger');
  const navLinks = document.getElementById('nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', !isExpanded);
      hamburger.classList.toggle('nav__hamburger--active');
      navLinks.classList.toggle('nav__links--active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.classList.remove('nav__hamburger--active');
        navLinks.classList.remove('nav__links--active');
      }
    });
  }

  // Global placeholder for updating checkout link
  let updateWhatsAppLink = null;

  // ─── 2. Product Detail Gallery Thumbnails Switcher ───
  const mainImage = document.getElementById('main-product-image');
  const thumbsContainer = document.getElementById('product-thumbnails');

  if (mainImage && thumbsContainer) {
    const thumbs = thumbsContainer.querySelectorAll('.product-gallery__thumb');
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        // Remove active class from all
        thumbs.forEach(t => t.classList.remove('product-gallery__thumb--active'));
        // Add active class to clicked
        thumb.classList.add('product-gallery__thumb--active');
        // Update main image source
        const newSrc = thumb.getAttribute('data-full-src');
        if (newSrc) {
          mainImage.src = newSrc;
        }

        // ── Auto-select matching color pill in form ──
        const imgColor = thumb.getAttribute('data-color');
        if (imgColor) {
          const colorPills = document.querySelectorAll('.js-color-pills .pill-btn');
          let matched = false;
          colorPills.forEach(pill => {
            if (pill.getAttribute('data-value').trim().toLowerCase() === imgColor.trim().toLowerCase()) {
              colorPills.forEach(p => p.classList.remove('pill-btn--active'));
              pill.classList.add('pill-btn--active');
              matched = true;
            }
          });
          if (matched && updateWhatsAppLink) {
            updateWhatsAppLink();
          }
        }
      });
    });
  }

  // ─── 3. Dynamic WhatsApp Checkout URL Generator ───
  const orderBtn = document.getElementById('product-whatsapp-order-btn');
  const nameHeading = document.getElementById('product-name-heading');

  if (orderBtn && nameHeading) {
    const productName = nameHeading.getAttribute('data-product-name');
    
    // Get active state helper
    const getActiveValue = (containerSelector) => {
      const activeBtn = document.querySelector(`${containerSelector} .pill-btn--active`);
      return activeBtn ? activeBtn.getAttribute('data-value') : '';
    };

    // Update WhatsApp link target
    updateWhatsAppLink = () => {
      const size = getActiveValue('.js-size-pills');
      const color = getActiveValue('.js-color-pills');
      
      let message = `Salam. I would like to inquire about purchasing the *${productName}*`;
      if (size) message += `, Size: *${size}*`;
      if (color) message += `, Color: *${color}*`;
      message += `. Please confirm availability and delivery to my location.`;
      
      // Get the number configured, fallback to brand defaults
      const waNumber = document.getElementById('nav-whatsapp-btn') 
        ? document.getElementById('nav-whatsapp-btn').getAttribute('href').split('/').pop().split('?')[0] 
        : '2347068886422';

      const encodedMsg = encodeURIComponent(message);
      orderBtn.setAttribute('href', `https://wa.me/${waNumber}?text=${encodedMsg}`);
    };

    // Setup size option selectors
    const sizePills = document.querySelectorAll('.js-size-pills .pill-btn');
    sizePills.forEach(pill => {
      pill.addEventListener('click', () => {
        sizePills.forEach(p => p.classList.remove('pill-btn--active'));
        pill.classList.add('pill-btn--active');
        updateWhatsAppLink();
      });
    });

    // Setup color option selectors
    const colorPills = document.querySelectorAll('.js-color-pills .pill-btn');
    colorPills.forEach(pill => {
      pill.addEventListener('click', () => {
        colorPills.forEach(p => p.classList.remove('pill-btn--active'));
        pill.classList.add('pill-btn--active');
        updateWhatsAppLink();

        // ── Auto-swap image based on color selection ──
        const selectedColor = pill.getAttribute('data-value').trim().toLowerCase();
        if (thumbsContainer) {
          const matchThumb = Array.from(thumbsContainer.querySelectorAll('.product-gallery__thumb'))
            .find(t => t.getAttribute('data-color') === selectedColor);
          if (matchThumb) {
            // Remove active thumbnail class on all, add to matched
            thumbsContainer.querySelectorAll('.product-gallery__thumb').forEach(t => {
              t.classList.remove('product-gallery__thumb--active');
            });
            matchThumb.classList.add('product-gallery__thumb--active');
            // Swap main image
            const newSrc = matchThumb.getAttribute('data-full-src');
            if (newSrc) {
              mainImage.src = newSrc;
            }
          }
        }
      });
    });

    // Run once on load to initialize URL
    updateWhatsAppLink();
  }

  // ─── 4. Client-side Shop Price Filters & Sorting ───
  const priceFiltersContainer = document.querySelector('.js-price-filters');
  const productGrid = document.getElementById('shop-product-grid');
  const noResultsAlert = document.getElementById('no-filtered-results');
  const resetBtn = document.getElementById('reset-price-filter');
  const sortSelect = document.getElementById('price-sort');

  if (productGrid) {
    const cards = Array.from(productGrid.querySelectorAll('.product-card'));
    let activePriceFilter = 'all';

    const filterAndSortProducts = () => {
      // 1. Filter
      let visibleCount = 0;
      cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price') || '0');
        let show = false;

        if (activePriceFilter === 'all') {
          show = true;
        } else if (activePriceFilter === 'under-50') {
          show = price < 50000;
        } else if (activePriceFilter === '50-100') {
          show = price >= 50000 && price <= 100000;
        } else if (activePriceFilter === 'over-100') {
          show = price > 100000;
        }

        if (show) {
          card.classList.remove('hidden');
          visibleCount++;
        } else {
          card.classList.add('hidden');
        }
      });

      // Manage empty state
      if (visibleCount === 0) {
        if (noResultsAlert) noResultsAlert.classList.remove('hidden');
        productGrid.classList.add('hidden');
      } else {
        if (noResultsAlert) noResultsAlert.classList.add('hidden');
        productGrid.classList.remove('hidden');
      }

      // 2. Sort
      const sortBy = sortSelect ? sortSelect.value : 'default';
      
      cards.sort((a, b) => {
        if (sortBy === 'price-asc') {
          return parseFloat(a.getAttribute('data-price') || '0') - parseFloat(b.getAttribute('data-price') || '0');
        } else if (sortBy === 'price-desc') {
          return parseFloat(b.getAttribute('data-price') || '0') - parseFloat(a.getAttribute('data-price') || '0');
        } else {
          // Default: Sort by created date descending
          return parseInt(b.getAttribute('data-date') || '0') - parseInt(a.getAttribute('data-date') || '0');
        }
      });

      // Re-append sorted cards to grid to update DOM layout
      cards.forEach(card => productGrid.appendChild(card));
    };

    // Attach price filter event handlers
    if (priceFiltersContainer) {
      const filterButtons = priceFiltersContainer.querySelectorAll('button');
      filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          filterButtons.forEach(b => b.classList.remove('filter-btn--active'));
          btn.classList.add('filter-btn--active');
          activePriceFilter = btn.getAttribute('data-price');
          filterAndSortProducts();
        });
      });
    }

    // Attach sort event handler
    if (sortSelect) {
      sortSelect.addEventListener('change', filterAndSortProducts);
    }

    // Attach reset filter button handler
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (priceFiltersContainer) {
          const filterButtons = priceFiltersContainer.querySelectorAll('button');
          filterButtons.forEach(b => b.classList.remove('filter-btn--active'));
          const allBtn = priceFiltersContainer.querySelector('[data-price="all"]');
          if (allBtn) allBtn.classList.add('filter-btn--active');
        }
        activePriceFilter = 'all';
        filterAndSortProducts();
      });
    }
  }
});
