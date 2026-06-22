/**
 * CustomNumberPicker - A beautiful, customizable popup number picker.
 * Fully self-contained, responsive, and easy to integrate.
 */
class CustomNumberPicker {
  constructor(options = {}) {
    // Default Configuration
    this.config = {
      title: options.title || 'Select Interval',
      subtitle: options.subtitle || 'Pick a preset or enter a custom value',
      unit: options.unit || 'minutes',
      presets: options.presets || [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
      defaultValue: options.defaultValue !== undefined ? options.defaultValue : 15,
      min: options.min !== undefined ? options.min : 1,
      max: options.max !== undefined ? options.max : 3600,
      onSubmit: options.onSubmit || null,
      onClose: options.onClose || null,
    };

    // Library State
    this.activeValue = this.config.defaultValue;
    this.tempValue = this.config.defaultValue;
    this.isCustomMode = !this.config.presets.includes(this.config.defaultValue);

    // DOM Elements references
    this.modalEl = null;
    this.presetsGridEl = null;
    this.customSectionEl = null;
    this.customInputEl = null;

    // Run initialization
    this._ensureTailwind();
    this._createDOM();
    this._bindEvents();
  }

  /**
   * Dynamically loads Tailwind CSS if it is not already present on the page.
   * This guarantees that the picker displays beautifully out of the box.
   */
  _ensureTailwind() {
    if (!window.tailwind) {
      const script = document.createElement('script');
      script.src = 'https://cdn.tailwindcss.com';
      document.head.appendChild(script);
    }
  }

  /**
   * Creates the markup structure for the popup modal and appends it to the body.
   */
  _createDOM() {
    // Unique ID identifier to prevent conflicts
    this.uniqueId = 'cnp-' + Math.random().toString(36).substr(2, 9);

    const overlay = document.createElement('div');
    overlay.id = this.uniqueId;
    // Hide by default with 'hidden', style using Tailwind
    overlay.className = 'hidden fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md transition-opacity duration-200';

    overlay.innerHTML = `
      <!-- Modal Card -->
      <div class="relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-6 transform scale-95 opacity-0 transition-all duration-300 ease-out select-none">

        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h2 class="text-lg font-bold text-slate-100">${this.config.title}</h2>
            <p class="text-xs text-slate-400 mt-0.5">${this.config.subtitle}</p>
          </div>
          <button
            type="button"
            data-action="close"
            class="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-xl transition-all duration-150"
            aria-label="Close"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Presets Grid -->
        <div class="space-y-3">
          <label class="text-xs font-semibold uppercase tracking-wider text-slate-500">Preset Values (${this.config.unit})</label>
          <div data-role="presets-grid" class="grid grid-cols-4 gap-2">
            <!-- Rendered Dynamically -->
          </div>
        </div>

        <!-- Custom Input Section -->
        <div data-role="custom-section" class="hidden space-y-3 border-t border-slate-800/80 pt-4 transition-all duration-200">
          <div class="flex justify-between items-center">
            <label class="text-xs font-semibold uppercase tracking-wider text-slate-500">Custom Value</label>
            <span class="text-[10px] text-slate-400">Min ${this.config.min} / Max ${this.config.max}</span>
          </div>
          <div class="flex items-center gap-2">
            <!-- Decrement -->
            <button
              type="button"
              data-action="decrement"
              class="p-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-bold transition-colors active:scale-95"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 pointer-events-none" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- Input Field -->
            <div class="relative flex-1">
              <input
                type="number"
                data-role="custom-input"
                placeholder="Enter ${this.config.unit}"
                min="${this.config.min}"
                max="${this.config.max}"
                class="w-full bg-slate-800 border border-slate-700 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 rounded-xl py-2.5 px-4 text-center text-lg font-bold text-slate-100 outline-none transition-all [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              >
            </div>

            <!-- Increment -->
            <button
              type="button"
              data-action="increment"
              class="p-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-bold transition-colors active:scale-95"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 pointer-events-none" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Actions Panel -->
        <div class="flex gap-3 border-t border-slate-800 pt-4">
          <button
            type="button"
            data-action="cancel"
            class="flex-1 py-3 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-xl transition-colors duration-150"
          >
            Cancel
          </button>
          <button
            type="button"
            data-action="submit"
            class="flex-1 py-3 px-4 bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] text-white font-semibold rounded-xl shadow-lg shadow-indigo-600/10 transition-all duration-150"
          >
            Apply Value
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    // Save internal DOM references
    this.modalEl = overlay;
    this.cardEl = overlay.querySelector('.bg-slate-900');
    this.presetsGridEl = overlay.querySelector('[data-role="presets-grid"]');
    this.customSectionEl = overlay.querySelector('[data-role="custom-section"]');
    this.customInputEl = overlay.querySelector('[data-role="custom-input"]');
  }

  /**
   * Registers all action handlers and input bindings
   */
  _bindEvents() {
    // Preset & close delegation
    this.modalEl.addEventListener('click', (e) => {
      const action = e.target.getAttribute('data-action');
      if (e.target === this.modalEl || action === 'close' || action === 'cancel') {
        this.close();
      } else if (action === 'increment') {
        this._adjustCustomValue(1);
      } else if (action === 'decrement') {
        this._adjustCustomValue(-1);
      } else if (action === 'submit') {
        this._submitValue();
      }
    });

    // Custom input parsing
    this.customInputEl.addEventListener('input', (e) => {
      let val = parseInt(e.target.value, 10);
      if (!isNaN(val)) {
        this.tempValue = val;
      }
    });

    // Handle ESC key to close
    this._onKeyDown = (e) => {
      if (e.key === 'Escape' && !this.modalEl.classList.contains('hidden')) {
        this.close();
      }
    };
    document.addEventListener('keydown', this._onKeyDown);
  }

  /**
   * Renders the presets items in the grid programmatically
   */
  _renderPresets() {
    this.presetsGridEl.innerHTML = '';

    // Preset Buttons
    this.config.presets.forEach(value => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = value;

      const isActive = !this.isCustomMode && this.tempValue === value;
      btn.className = `py-3 rounded-xl font-bold transition-all duration-150 border text-sm ${
        isActive
          ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/20'
          : 'bg-slate-800 hover:bg-slate-700/80 border-slate-800 text-slate-300 hover:text-white'
      }`;

      btn.addEventListener('click', () => this._selectPreset(value));
      this.presetsGridEl.appendChild(btn);
    });

    // Custom Choice Button
    const customBtn = document.createElement('button');
    customBtn.type = 'button';
    customBtn.textContent = 'Custom';
    customBtn.className = `py-3 rounded-xl font-bold transition-all duration-150 border text-sm col-span-4 mt-1 ${
      this.isCustomMode
        ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/20'
        : 'bg-slate-800 hover:bg-slate-700/80 border-slate-800 text-slate-300 hover:text-white'
    }`;
    customBtn.addEventListener('click', () => this._enableCustomMode());
    this.presetsGridEl.appendChild(customBtn);
  }

  _selectPreset(value) {
    this.isCustomMode = false;
    this.tempValue = value;
    this._toggleCustomView();
    this._renderPresets();
  }

  _enableCustomMode() {
    this.isCustomMode = true;
    if (!this.customInputEl.value) {
      this.customInputEl.value = this.tempValue;
    }
    this.tempValue = parseInt(this.customInputEl.value, 10) || this.config.defaultValue;
    this._toggleCustomView();
    this._renderPresets();
    this.customInputEl.focus();
  }

  _toggleCustomView() {
    if (this.isCustomMode) {
      this.customSectionEl.classList.remove('hidden');
    } else {
      this.customSectionEl.classList.add('hidden');
    }
  }

  _adjustCustomValue(offset) {
    let current = parseInt(this.customInputEl.value, 10) || this.config.defaultValue;
    let target = current + offset;
    if (target >= this.config.min && target <= this.config.max) {
      this.customInputEl.value = target;
      this.tempValue = target;
    }
  }

  _submitValue() {
    let finalValue = this.tempValue;

    if (this.isCustomMode) {
      const val = parseInt(this.customInputEl.value, 10);
      if (isNaN(val) || val < this.config.min || val > this.config.max) {
        // Red error indication
        this.customInputEl.classList.add('border-red-500', 'ring-2', 'ring-red-500/20');
        setTimeout(() => {
          this.customInputEl.classList.remove('border-red-500', 'ring-2', 'ring-red-500/20');
        }, 1500);
        return;
      }
      finalValue = val;
    }

    this.activeValue = finalValue;
    if (typeof this.config.onSubmit === 'function') {
      this.config.onSubmit(this.activeValue);
    }
    this.close();
  }

  /**
   * PUBLIC API: Opens the custom picker pop-up
   */
  open(overrideValue) {
    if (overrideValue !== undefined) {
      this.activeValue = overrideValue;
    }

    this.tempValue = this.activeValue;
    this.isCustomMode = !this.config.presets.includes(this.activeValue);

    if (this.isCustomMode) {
      this.customInputEl.value = this.activeValue;
    } else {
      this.customInputEl.value = '';
    }

    this._toggleCustomView();
    this._renderPresets();

    // Show with transitions
    this.modalEl.classList.remove('hidden');
    document.body.style.overflow = 'hidden';

    // Microtask delay to allow transition styles to compute
    setTimeout(() => {
      this.cardEl.classList.remove('scale-95', 'opacity-0');
      this.cardEl.classList.add('scale-100', 'opacity-100');
    }, 10);
  }

  /**
   * PUBLIC API: Closes the custom picker pop-up
   */
  close() {
    this.cardEl.classList.remove('scale-100', 'opacity-100');
    this.cardEl.classList.add('scale-95', 'opacity-0');

    setTimeout(() => {
      this.modalEl.classList.add('hidden');
      document.body.style.overflow = '';
      if (typeof this.config.onClose === 'function') {
        this.config.onClose();
      }
    }, 200);
  }

  /**
   * Destroys the instance and cleans up elements/events
   */
  destroy() {
    document.removeEventListener('keydown', this._onKeyDown);
    if (this.modalEl && this.modalEl.parentNode) {
      this.modalEl.parentNode.removeChild(this.modalEl);
    }
  }
}

// Export the class for ES environment
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CustomNumberPicker;
} else {
  window.CustomNumberPicker = CustomNumberPicker;
}
