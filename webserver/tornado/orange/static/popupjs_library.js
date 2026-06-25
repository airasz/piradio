class PopupJSLibrary {
  constructor() {
    this.backdrop = null;
    this.container = null;
    this.toastContainer = null;
    this.initCompleted = false;
  }

  /**
   * Initializes the library, injects CSS animations, styles, and core DOM structures.
   */
  init() {
    if (this.initCompleted) return;

    // 1. Inject required CSS configurations
    const styleEl = document.createElement("style");
    styleEl.id = "popupjs-styles";
    styleEl.innerHTML = `

                    /* Backdrop Overlay */
                    #pjs-modal-backdrop {
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background-color: rgba(2, 6, 23, 0.55);
                        backdrop-filter: blur(4px);
                        -webkit-backdrop-filter: blur(4px);
                        z-index: 9999;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 1rem;
                        opacity: 0;
                        visibility: hidden;
                        transition: opacity 0.25s ease, visibility 0.25s ease;
                    }
                    #pjs-modal-backdrop.active {
                        opacity: 1;
                        visibility: visible;
                    }

                    /* Modal Content Frame */
                    .pjs-modal-container {
                        background-color: #0f172a; /* slate-900 */
                        border: 1px solid #334155; /* slate-700 */
                        width: 100%;
                        max-width: 32rem;
                        border-radius: 1.25rem;
                        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                        padding: 1.5rem;
                        transform: scale(0.95);
                        transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
                    }
                    #pjs-modal-backdrop.active .pjs-modal-container {
                        transform: scale(1);
                    }

                    /* Scoped Modal Utilities */
                    .pjs-flex { display: flex; }
                    .pjs-align-start { align-items: flex-start; }
                    .pjs-space-x-4 > * + * { margin-left: 1rem; }
                    .pjs-flex-shrink-0 { flex-shrink: 0; }
                    .pjs-flex-1 { flex: 1; }
                    .pjs-text-white { color: #ffffff; }
                    .pjs-text-sm { font-size: 0.875rem; }
                    .pjs-text-slate-400 { color: #94a3b8; }
                    .pjs-mt-1 { margin-top: 0.25rem; }
                    .pjs-mt-6 { margin-top: 1.5rem; }
                    .pjs-justify-end { justify-content: flex-end; }

                    /* Scoped Library Buttons */
                    .pjs-btn-group {
                        display: flex;
                        gap: 0.75rem;
                        justify-content: flex-end;
                    }
                    .pjs-btn {
                        padding: 0.5rem 1rem;
                        font-size: 0.875rem;
                        font-weight: 500;
                        border-radius: 0.5rem;
                        cursor: pointer;
                        transition: background-color 0.15s ease;
                    }
                    .pjs-btn-cancel {
                        background-color: #334155;
                        color: #e2e8f0;
                        border: 1px solid #475569;
                    }
                    .pjs-btn-cancel:hover {
                        background-color: #475569;
                    }
                    .pjs-btn-ok {
                        background-color: #d97706; /* amber-600 */
                        color: white;
                        border: none;
                    }
                    .pjs-btn-ok:hover {
                        background-color: #b45309;
                    }
                    .pjs-btn-primary {
                        background-color: #4f46e5;
                        color: white;
                        border: none;
                        width: 100%;
                        padding: 0.625rem 1rem;
                    }
                    .pjs-btn-primary:hover {
                        background-color: #4338ca;
                    }

                    /* Scoped Icons */
                    .pjs-icon-box {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 2.5rem;
                        width: 2.5rem;
                        border-radius: 0.5rem;
                    }
                    .pjs-icon-alert {
                        background-color: rgba(245, 158, 11, 0.1);
                        color: #fbbf24;
                        border: 1px solid rgba(245, 158, 11, 0.25);
                    }
                    .pjs-icon-info {
                        background-color: rgba(59, 130, 246, 0.1);
                        color: #60a5fa;
                        border: 1px solid rgba(59, 130, 246, 0.25);
                        margin: 0 auto 1rem;
                        border-radius: 50%;
                    }

                    /* Custom dynamic playlists layout system */
                    .pjs-playlist-wrapper {
                        /* display: grid; */
                        grid-template-columns: repeat(2, minmax(0, 1fr));
                        gap: 0.75rem;
                        width: 100%;
                        margin-top: 1rem;
                        margin-bottom: 1rem;

                        flex: 1 1 0;
                        min-height: 0;
                        /* required for flex children to shrink below content size */
                        /*   max-height: none; */
                        /* override .buttonstation fixed cap */
                        overflow-y: auto;
                        max-height: 400px;
                    }
                    @media (min-width: 640px) {
                        .pjs-playlist-wrapper {
                            grid-template-columns: repeat(3, minmax(0, 1fr));
                        }
                    }
                    .pjs-playlist-wrapper .button1 {
/*                         background-color: rgba(2, 6, 23, 0.6); */
/*                         border: 1px solid rgba(71, 85, 105, 0.4); */
/*                         border-radius: 0.75rem; */
                        /*padding: 0.75rem 1rem;*/

                        font-weight: 500;
                        font-size: 0.875rem;
                        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                        text-align: left;
                        // display: flex;
                        align-items: center;
                        justify-content: space-between;
                        cursor: pointer;
                        /* width: 100%;
                        backdrop-filter: none !important;*/
                    }
                    .pjs-playlist-wrapper .button1:hover {
                        background-color: rgba(19, 142, 41, 0.45);
                        border-color: rgba(99, 102, 241, 0.6);

                        transform: translateY(-2px);
                        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
                    }
                    .pjs-playlist-wrapper .button1.bplay {
                        background-color: rgba(16, 185, 129, 0.1);
                        border-color: rgba(16, 185, 129, 0.5);
                        color: #34d399;
                        font-weight: 600;
                        box-shadow: 0 0 12px rgba(16, 185, 129, 0.1);

                        backdrop-filter: none !important;
                    }
                    .pjs-playlist-wrapper .button1.bplay::after {
                        content: '';
                        display: inline-block;
                        width: 8px;
                        height: 8px;
                        background-color: #108981;
                        border-radius: 50%;
                        margin-left: 0.5rem;
                        box-shadow: 0 0 8px #10b981;
                        animation: pjsPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
                    }
                    .pjs-playlist-wrapper .button1 a {
                        text-decoration: none;
                        color: inherit;
                        display: inline-block;
                        width: 100%;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        pointer-events: none;

                    }
                    @keyframes pjsPulse {
                        0%, 100% { opacity: 1; transform: scale(1); }
                        50% { opacity: .4; transform: scale(1.2); }
                    }

                    /* Toast Notification System */
                    #pjs-toast-container {
                        position: fixed;
                        top: 1.5rem;
                        right: 1.5rem;
                        z-index: 10000;
                        display: flex;
                        flex-direction: column;
                        gap: 0.75rem;
                        pointer-events: none;
                        max-width: 24rem;
                        width: 100%;
                    }
                    .pjs-toast {
                        pointer-events: auto;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        gap: 0.75rem;
                        padding: 1rem;
                        border-radius: 0.75rem;
                        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
                        background-color: rgba(15, 23, 42, 0.95);
                        border: 1px solid #334155;
                        transform: translateY(1rem);
                        opacity: 0;
                        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
                    }
                    .pjs-toast.active {
                        transform: translateY(0);
                        opacity: 1;
                    }
                    .pjs-toast-success {
                        border-color: rgba(16, 185, 129, 0.3);
                    }
                    .pjs-toast-error {
                        border-color: rgba(244, 63, 94, 0.3);
                    }
                    .pjs-toast-close {
                        background: none;
                        border: none;
                        color: #64748b;
                        cursor: pointer;
                        display: flex;
                        padding: 0.125rem;
                    }
                    .pjs-toast-close:hover {
                        color: #cbd5e1;
                    }
					.hidden{
						visibility: hidden;
					}
					.popup_card{
						background:  rgba(244, 244, 244, 0.3);
						padding:6px;
					}
					.popup_card input[type="text"]{
                      width:80%;
                    }
                    #prompt-input{
                    width:80%;
                    }


                `;
    document.head.appendChild(styleEl);

    // 2. Generate and inject Modal Backdrop markup
    this.backdrop = document.createElement("div");
    this.backdrop.id = "pjs-modal-backdrop";

    this.container = document.createElement("div");
    // this.container.className = "pjs-modal-container";
    this.container.className = "popup_card";
    this.backdrop.appendChild(this.container);
    document.body.appendChild(this.backdrop);

    // Close on backdrop click
    this.backdrop.addEventListener("click", (e) => {
      if (e.target === this.backdrop) {
        this.close();
      }
    });

    // 3. Generate and inject Toast Container
    this.toastContainer = document.createElement("div");
    this.toastContainer.id = "pjs-toast-container";
    document.body.appendChild(this.toastContainer);

    this.initCompleted = true;
  }

  /**
   * Helper to open any raw HTML template in the modal layout.
   */
  open(htmlContent) {
    this.init();
    this.container.innerHTML = htmlContent;
    this.backdrop.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  /**
   * Closes the active modal cleanly.
   */
  close() {
    if (!this.initCompleted) return;
    this.backdrop.classList.remove("active");
    document.body.style.overflow = "";
    setTimeout(() => {
      if (!this.backdrop.classList.contains("active")) {
        this.container.innerHTML = "";
      }
    }, 250);
  }

  /**
   * Triggers a promise-based confirmation popup.
   */
  confirm(title, message, confirmBtnText = "Confirm") {
    return new Promise((resolve) => {
      const template = `
                        <div>
                            <div class="pjs-flex pjs-align-start pjs-space-x-4">
                                <div class="pjs-flex-shrink-0 pjs-icon-box pjs-icon-alert">
                                    <svg style="width:1.25rem; height:1.25rem" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                </div>
                                <div class="pjs-flex-1">
                                    <h3 class="pjs-text-white" style="font-weight: 600; font-size: 1.125rem;">${title}</h3>
                                    <p class="pjs-text-slate-400 pjs-text-sm pjs-mt-1">${message}</p>
                                </div>
                            </div>
                            <div class="pjs-mt-6 pjs-btn-group">
                                <button id="pjs-confirm-cancel" class="pjs-btn pjs-btn-cancel">
                                    Cancel
                                </button>
                                <button id="pjs-confirm-ok" class="pjs-btn pjs-btn-ok">
                                    ${confirmBtnText}
                                </button>
                            </div>
                        </div>
                    `;
      this.open(template);

      document
        .getElementById("pjs-confirm-cancel")
        .addEventListener("click", () => {
          this.close();
          resolve(false);
        });

      document
        .getElementById("pjs-confirm-ok")
        .addEventListener("click", () => {
          this.close();
          resolve(true);
        });
    });
  }

  /**
   * Displays non-blocking, beautiful toast notifications.
   */
  toast(message, type = "success") {
    this.init();
    const id = "pjs-toast-" + Math.random().toString(36).substr(2, 9);

    let iconColor = "#10b981"; // emerald
    let iconSvg = `<svg style="width:1.25rem; height:1.25rem" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
    let specificClass = "pjs-toast-success";

    if (type === "error") {
      iconColor = "#f43f5e"; // rose
      iconSvg = `<svg style="width:1.25rem; height:1.25rem" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
      specificClass = "pjs-toast-error";
    }

    const toastHTML = `
                    <div id="${id}" class="pjs-toast ${specificClass}">
                        <div class="pjs-flex" style="align-items: center; gap: 0.75rem;">
                            <div style="color: ${iconColor}; display: flex;">${iconSvg}</div>
                            <div class="pjs-text-sm" style="font-weight: 500; color: #e2e8f0;">${message}</div>
                        </div>
                        <button onclick="PopupJS.dismissToast('${id}')" class="pjs-toast-close">
                            <svg style="width:1rem; height:1rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                        </button>
                    </div>
                `;

    this.toastContainer.insertAdjacentHTML("beforeend", toastHTML);

    // Trigger entrance animation on next layout frame
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) el.classList.add("active");
    }, 50);

    // Auto dismiss after 4 seconds
    setTimeout(() => {
      this.dismissToast(id);
    }, 4000);
  }

  dismissToast(id) {
    const element = document.getElementById(id);
    if (element) {
      element.classList.remove("active");
      setTimeout(() => element.remove(), 300);
    }
  }

  /**
   * Opens a modal container containing custom dynamic HTML (e.g. MPC Playlist).
   */
  openCustomHTML(title, rawHtml) {
    const template = `
                    <div>
                        <!-- Header -->
                        <div class="pjs-flex" style="align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(51, 65, 85, 0.6); padding-bottom: 1rem; margin-bottom: 1rem;">
                            <div class="pjs-flex" style="align-items: center; gap: 0.75rem;">
                                <div style="width: 2rem; height: 2rem; border-radius: 0.5rem; background-color: rgba(99, 102, 241, 0.1); color: #818cf8; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(99, 102, 241, 0.2);">
                                    <svg style="width:1.25rem; height:1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                                </div>
                                <div>
                                    <h3 class="pjs-text-white" style="font-weight: 700; font-size: 1.125rem; line-height: 1.2;">${title}</h3>
                                    <p class="pjs-text-white" style="font-size: 0.75rem; font-weight: 500; margin-top: 0.125rem;">Select an option below.</p>
                                </div>
                            </div>
                            <button onclick="PopupJS.close()" style="background:none; border:none; color:#94a3b8; cursor:pointer; padding:0.25rem; display:flex; border-radius:0.375rem;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#94a3b8'">
                                <svg style="width:1.5rem; height:1.5rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                            </button>
                        </div>

                        <!-- Custom HTML container with scoped playlist design patterns -->
                        <div class="pjs-playlist-wrapper">
                            ${rawHtml}
                        </div>

                        <!-- Footer close -->
                        <div class="pjs-mt-6 pjs-flex pjs-justify-end" style="border-top: 1px solid rgba(51, 65, 85, 0.6); padding-top: 1rem;">
                            <button onclick="PopupJS.close()" class="pjs-btn pjs-btn-cancel">
                                Cancel
                            </button>
                        </div>
                    </div>
                `;
    this.open(template);
  }
  /* ------------------------------------------- */
  /* 2. CUSTOM INPUT PROMPT WITH VALIDATION      */
  /* ------------------------------------------- */
  customPrompt(callback, title, label, placeholder) {
    return new Promise((resolve) => {
      const template = `
				<div>
          <div class="pjs-flex" style="align-items: center; gap: 0.75rem;">
              <div style="width: 2rem; height: 2rem; border-radius: 0.5rem; background-color: rgba(99, 102, 241, 0.1); color: #818cf8; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(99, 102, 241, 0.2);">
                  <svg style="width:1.25rem; height:1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
              </div>
              <div>
                  <h3 class="pjs-text-white" style="font-weight: 700; font-size: 1.125rem; line-height: 1.2;">${title}</h3>
                  <p class="pjs-text-white" style="font-size: 0.75rem; font-weight: 500; margin-top: 0.125rem;">${label}</p>
              </div>
          </div>
					<input type="text" id="prompt-input" placeholder="${placeholder}"
						   class="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none rounded-xl px-4 py-2.5 text-sm text-white mb-1 transition"/>
					<p id="prompt-error" class="text-xs text-rose-400 hidden mt-1">Input cannot be left empty.</p>

					<div class="mt-6 flex justify-end space-x-3">
						<button id="prompt-cancel" class="button1 -4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 text-sm font-medium rounded-xl transition">
							Cancel
						</button>
						<button id="prompt-submit" class="button1 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-xl transition">
							Submit
						</button>
					</div>
				</div>
			`;
      this.open(template);

      // Focus on input when prompt loads
      const inputEl = document.getElementById("prompt-input");
      setTimeout(() => inputEl.focus(), 100);

      // Add enter key handler
      inputEl.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
          document.getElementById("prompt-submit").click();
        }
      });

      document.getElementById("prompt-cancel").addEventListener("click", () => {
        this.close();
        resolve(null);
      });

      document.getElementById("prompt-submit").addEventListener("click", () => {
        const value = inputEl.value.trim();
        if (!value) {
          document.getElementById("prompt-error").classList.remove("hidden");
          inputEl.classList.add("border-rose-500");
          return;
        }
        this.close();
        resolve(value);
        callback(value);
      });
    });
  }

  async triggerPrompt() {
    appendLog("Custom Prompt triggered, awaiting valid input resolution...");
    const username = await customPrompt(
      "Update Developer Alias",
      "Alias Identifier",
      "e.g., CodeNinja99",
    );

    if (username !== null) {
      appendLog(`Resolved input value: "${username}"`, "success");
      triggerToast("success", `Developer alias saved as "${username}"`);
    } else {
      appendLog("Prompt dismissed. Returned value: null", "warn");
    }
  }
}

// Initialize the library in the window context
window.PopupJS = new PopupJSLibrary();
