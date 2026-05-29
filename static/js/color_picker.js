/**
 * Dar Safeera Admin — Color Picker Widget JS
 * Manages swatch toggle and syncs selected color names to a hidden <input>.
 */

function dsColorPickerInit(containerId, hiddenId, allColors) {
  const container = document.getElementById(containerId);
  const hidden = document.getElementById(hiddenId);
  if (!container || !hidden) return;

  // Build a lookup: name → swatch button
  const swatches = container.querySelectorAll('.ds-swatch');

  function getSelected() {
    const selected = [];
    swatches.forEach(sw => {
      if (sw.classList.contains('ds-swatch--selected')) {
        selected.push(sw.dataset.name);
      }
    });
    // Also pick up any dynamic custom swatches
    container.querySelectorAll('.ds-swatch--custom.ds-swatch--selected').forEach(sw => {
      if (!selected.includes(sw.dataset.name)) selected.push(sw.dataset.name);
    });
    return selected;
  }

  function syncHidden() {
    hidden.value = getSelected().join(', ');
    const count = container.querySelector('.ds-color-picker__count');
    if (count) count.textContent = getSelected().length;
  }

  // Attach click handlers to static swatches
  swatches.forEach(sw => {
    sw.addEventListener('click', function () {
      const isSelected = this.classList.contains('ds-swatch--selected');
      this.classList.toggle('ds-swatch--selected', !isSelected);
      this.setAttribute('aria-pressed', !isSelected);
      syncHidden();
    });
  });

  // Initial count sync
  syncHidden();
}

function dsAddCustomColor(containerId, colorInputId) {
  const container = document.getElementById(containerId);
  const colorInput = document.getElementById(colorInputId);
  const hidden = document.getElementById(container.dataset.field);
  if (!container || !colorInput || !hidden) return;

  const hex = colorInput.value;
  const name = hex; // use hex as the name for custom colors

  // Check if already added
  const existing = container.querySelector(`.ds-swatch[data-name="${name}"]`);
  if (existing) {
    existing.click();
    return;
  }

  // Create new swatch
  const swatchGrid = container.querySelector('.ds-color-picker__swatches');
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'ds-swatch ds-swatch--custom ds-swatch--selected';
  btn.style.background = hex;
  btn.title = hex;
  btn.dataset.name = name;
  btn.dataset.hex = hex;
  btn.setAttribute('aria-pressed', 'true');
  btn.innerHTML = '<span class="ds-swatch__check">✓</span>';

  btn.addEventListener('click', function () {
    const isSelected = this.classList.contains('ds-swatch--selected');
    this.classList.toggle('ds-swatch--selected', !isSelected);
    this.setAttribute('aria-pressed', !isSelected);
    syncHiddenForContainer(container, hidden);
  });

  swatchGrid.appendChild(btn);
  syncHiddenForContainer(container, hidden);
}

function syncHiddenForContainer(container, hidden) {
  const selected = [];
  container.querySelectorAll('.ds-swatch--selected').forEach(sw => {
    selected.push(sw.dataset.name);
  });
  hidden.value = selected.join(', ');
  const count = container.querySelector('.ds-color-picker__count');
  if (count) count.textContent = selected.length;
}
