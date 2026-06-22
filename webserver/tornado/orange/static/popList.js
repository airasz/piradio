/**
 * PopupList.js - Portable Interactive Popup List Library
 * Features: Zero dependencies, dynamically-injected scoped styling
 */
class PopupList {
    constructor(options = {}) {
        this.config = {
            title: options.title || 'Select Option',
            items: options.items || [],
            onSelect: options.onSelect || (() => {}),
            themeColor: options.themeColor || '#4f46e5',
            closeOnSelect: options.closeOnSelect !== false,
        };

        this.popupElement = null;
        this._injectStyles();
    }

    // Self-inject component encapsulation styles
    _injectStyles() {
        if (document.getElementById('popup-list-styles')) return;

        const style = document.createElement('style');
        style.id = 'popup-list-styles';
        style.textContent = `
        .pl-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(4px);
            display: flex; justify-content: center; align-items: center;
            z-index: 99999; opacity: 0; transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            padding: 16px;
            box-sizing: border-box;
        }
        .pl-overlay * { box-sizing: border-box; }
        .pl-overlay.pl-active { opacity: 1; }

        .pl-container {
            background: #1e293b; border: 1px solid #334155; border-radius: 12px;
            width: 100%; max-width: 420px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); overflow: hidden;
            transform: scale(0.95) translateY(10px); transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .pl-overlay.pl-active .pl-container { transform: scale(1) translateY(0); }

        .pl-header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 20px; border-bottom: 1px solid #334155; background: #0f172a;
        }
        .pl-title { margin: 0; font-size: 1.05rem; font-weight: 600; color: #f8fafc; }

        .pl-close-btn {
            background: none; border: none; font-size: 1.6rem; cursor: pointer;
            color: #94a3b8; line-height: 1; transition: color 0.15s ease;
        }
        .pl-close-btn:hover { color: #f1f5f9; }

        .pl-list { list-style: none; padding: 0; margin: 0; max-height: 320px; overflow-y: auto; }

        .pl-item {
            padding: 14px 20px; cursor: pointer; transition: all 0.15s ease;
            color: #cbd5e1; border-bottom: 1px solid #334155; font-size: 0.95rem;
            display: flex; align-items: center; justify-content: space-between;
        }
        .pl-item:last-child { border-bottom: none; }
        .pl-item:hover {
            background: rgba(255, 255, 255, 0.03);
            color: var(--pl-theme-color, #4f46e5);
            padding-left: 24px;
        }
        `;
        document.head.appendChild(style);
    }

    open() {
        if (this.popupElement) this.close();

        this.popupElement = document.createElement('div');
        this.popupElement.className = 'pl-overlay';
        this.popupElement.style.setProperty('--pl-theme-color', this.config.themeColor);

        const itemsHTML = this.config.items.map((item, index) => {
            const text = typeof item === 'object' ? item.text : item;
            return `<li class="pl-item" data-index="${index}">
            <span>${text}</span>
            <span style="opacity: 0.4; font-size: 0.8rem;">&rarr;</span>
            </li>`;
        }).join('');

        this.popupElement.innerHTML = `
        <div class="pl-container">
        <div class="pl-header">
        <h3 class="pl-title">${this.config.title}</h3>
        <button class="pl-close-btn" aria-label="Close">&times;</button>
        </div>
        <ul class="pl-list">${itemsHTML}</ul>
        </div>
        `;

        this.popupElement.querySelector('.pl-close-btn').addEventListener('click', () => this.close());
        this.popupElement.addEventListener('click', (e) => { if (e.target === this.popupElement) this.close(); });
        this.popupElement.querySelector('.pl-list').addEventListener('click', (e) => {
            const itemEl = e.target.closest('.pl-item');
            if (!itemEl) return;
            const index = itemEl.getAttribute('data-index');
            this.config.onSelect(this.config.items[index], index);
            if (this.config.closeOnSelect) this.close();
        });

            document.body.appendChild(this.popupElement);
            setTimeout(() => this.popupElement.classList.add('pl-active'), 10);
    }

    close() {
        if (!this.popupElement) return;
        this.popupElement.classList.remove('pl-active');
        setTimeout(() => {
            if (this.popupElement && this.popupElement.parentNode) {
                this.popupElement.parentNode.removeChild(this.popupElement);
            }
            this.popupElement = null;
        }, 250);
    }
}

// Export support
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PopupList;
} else {
    window.PopupList = PopupList;
}
