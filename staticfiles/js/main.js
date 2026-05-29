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
    const updateWhatsAppLink = () => {
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
      });
    });

    // Run once on load to initialize URL
    updateWhatsAppLink();
  }

  // ─── 4. Client-side Shop Color Filters ───
  const colorFiltersContainer = document.querySelector('.js-color-filters');
  const productGrid = document.getElementById('shop-product-grid');
  const noResultsAlert = document.getElementById('no-filtered-results');
  const resetBtn = document.getElementById('reset-color-filter');

  if (colorFiltersContainer && productGrid) {
    const filterButtons = colorFiltersContainer.querySelectorAll('button');
    const cards = productGrid.querySelectorAll('.product-card');

    const filterProductsByColor = (selectedColor) => {
      let visibleCount = 0;

      cards.forEach(card => {
        const productColorsStr = card.getAttribute('data-colors') || '';
        const colorsList = productColorsStr.split(' ').filter(c => c.trim() !== '');

        if (selectedColor === 'all') {
          card.classList.remove('hidden');
          visibleCount++;
        } else {
          // Check if selectedColor is a substring of any color listed (e.g. "cream" matches "cream/beige" or "beige")
          const matches = colorsList.some(colorVal => {
            return colorVal.includes(selectedColor) || selectedColor.includes(colorVal);
          });

          if (matches) {
            card.classList.remove('hidden');
            visibleCount++;
          } else {
            card.classList.add('hidden');
          }
        }
      });

      // Manage empty state
      if (visibleCount === 0) {
        noResultsAlert.classList.remove('hidden');
        productGrid.classList.add('hidden');
      } else {
        noResultsAlert.classList.add('hidden');
        productGrid.classList.remove('hidden');
      }
    };

    filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('filter-btn--active'));
        btn.classList.add('filter-btn--active');
        const color = btn.getAttribute('data-color');
        filterProductsByColor(color);
      });
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('filter-btn--active'));
        const allBtn = colorFiltersContainer.querySelector('[data-color="all"]');
        if (allBtn) allBtn.classList.add('filter-btn--active');
        filterProductsByColor('all');
      });
    }
  }
});
