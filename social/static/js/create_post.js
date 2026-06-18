/* =============================================
   create_post.js — Social AI Post Creator
   ============================================= */

(function () {
    "use strict";

    /* ---- State ---- */
    const state = {
        selectedPlatform: null,
        selectedTone: "Professional",
    };

    /* ---- DOM refs ---- */
    const hiddenForm = document.getElementById("hiddenForm");
    const hAction = document.getElementById("hAction");
    const hPlatform = document.getElementById("hPlatform");
    const hPrompt = document.getElementById("hPrompt");
    const visiblePrompt = document.getElementById("visiblePrompt");
    const btnGenerate = document.querySelector(".btn-generate");
    const mockFooter = document.getElementById("mock-footer");

    /* ---- Read connected platforms from the injected JSON blob ---- */
    let connectedPlatforms = [];
    try {
        const blob = document.getElementById("conn-plats-data");
        if (blob) connectedPlatforms = JSON.parse(blob.textContent.trim());
    } catch (e) {
        connectedPlatforms = [];
    }

    /* ========================================================
       PLATFORM SELECTION
       ======================================================== */
    function initPlatformBoxes() {
        document.querySelectorAll(".plat-box").forEach(function (box) {
            const plat = box.dataset.plat;
            const connected =
                connectedPlatforms.includes(plat) ||
                (plat === "x" && connectedPlatforms.includes("twitter"));

            box.addEventListener("click", function () {
                if (!connected) {
                    openConnectModal(plat);
                    return;
                }
                selectPlatform(plat);
            });
        });

        /* Pre-select whatever the server returned */
        const serverPlatform = hPlatform.value;
        if (serverPlatform) {
            selectPlatform(serverPlatform, false);
        }
    }

    function selectPlatform(plat, updateHidden) {
        /* Deselect all */
        document.querySelectorAll(".plat-box").forEach(function (b) {
            b.classList.remove("selected");
        });

        /* Select the matching box */
        const target = document.querySelector(".plat-box[data-plat='" + plat + "']");
        if (target) target.classList.add("selected");

        state.selectedPlatform = plat;

        /* Update the hidden input */
        if (updateHidden !== false) {
            hPlatform.value = plat;
        }

        showMockup(plat);
    }

    /* ========================================================
       MOCKUP DISPLAY
       ======================================================== */
    const mockupMap = {
        instagram: "mock-instagram",
        facebook: "mock-facebook",
        linkedin: "mock-linkedin",
        x: "mock-twitter",
        twitter: "mock-twitter",
    };

    function showMockup(plat) {
        /* Hide all */
        document.getElementById("mock-default").style.display = "none";
        document.getElementById("mock-instagram").style.display = "none";
        document.getElementById("mock-facebook").style.display = "none";
        document.getElementById("mock-linkedin").style.display = "none";
        document.getElementById("mock-twitter").style.display = "none";

        const id = mockupMap[plat];
        if (id) {
            const el = document.getElementById(id);
            if (el) {
                el.style.display = (plat === "x" || plat === "twitter") ? "flex" : "block";
            }
        } else {
            document.getElementById("mock-default").style.display = "block";
        }

        /* Show footer if a platform is selected */
        if (mockFooter) {
            const hasPost = getActiveMockContent();
            mockFooter.style.display = (plat && hasPost) ? "flex" : "none";
        }
    }

    function getActiveMockContent() {
        /* Returns the text inside the currently visible mockup content element */
        const platform = state.selectedPlatform || hPlatform.value;
        if (!platform) return "";
        const id = mockupMap[platform];
        if (!id) return "";
        const wrapper = document.getElementById(id);
        if (!wrapper) return "";
        const contentEl = wrapper.querySelector(".mock-content, .mock-x-content");
        return contentEl ? contentEl.innerText.trim() : "";
    }
    function publishPost() {
        // 1. Find the hidden form
        const form = document.getElementById('hiddenForm');

        // 2. Change the action input value if your backend tracks it
        document.getElementById('hAction').value = 'publish';

        // 3. Submit the form
        form.submit();
    }
    /* ========================================================
       TONE SELECTION
       (Works with both <select> and optional .tone-pill elements)
       ======================================================== */
    function initTone() {
        /* Select element */
        const sel = document.querySelector(".cp-select");
        if (sel) {
            sel.addEventListener("change", function () {
                state.selectedTone = sel.value;
            });
        }

        /* Pill variant (if used instead of select) */
        document.querySelectorAll(".tone-pill").forEach(function (pill) {
            pill.addEventListener("click", function () {
                document.querySelectorAll(".tone-pill").forEach(function (p) {
                    p.classList.remove("active");
                });
                pill.classList.add("active");
                state.selectedTone = pill.dataset.tone || pill.textContent.trim();
            });
        });
    }

    /* ========================================================
       GENERATE POST
       ======================================================== */
    window.generatePost = function () {
        const prompt = visiblePrompt ? visiblePrompt.value.trim() : "";
        let plat = state.selectedPlatform || hPlatform.value;
        if (plat === "None") plat = "";

        if (!plat) {
            highlightStep(1, "Please select a platform first.");
            return;
        }
        if (!prompt) {
            highlightStep(2, "Please enter a topic or idea.");
            visiblePrompt && visiblePrompt.focus();
            return;
        }

        /* Append tone tag to the prompt */
        const tone = state.selectedTone || "Professional";
        const fullPrompt = prompt + " [Tone: " + tone + "]";

        hAction.value = "generate";
        hPlatform.value = plat;
        hPrompt.value = fullPrompt;

        /* Visual loading state */
        if (btnGenerate) {
            btnGenerate.disabled = true;
            btnGenerate.innerHTML =
                '<span class="cp-spinner"></span> Generating...';
        }

        hiddenForm.submit();
    };

    /* ========================================================
       PUBLISH POST
    //    ======================================================== */
    // window.publishPost = function () {
    //     hAction.value = "publish";
    //     hiddenForm.submit();
    // };

    /* ========================================================
       APPROVE / REGENERATE (exposed for inline onclick usage)
       ======================================================== */
    /* These are already handled by the inline onclick in the HTML:
       document.getElementById('hAction').value = 'regenerate';
       document.getElementById('hiddenForm').submit();
       But we expose a helper for clean calls from JS too. */
    window.triggerAction = function (actionName) {
        hAction.value = actionName;
        hiddenForm.submit();
    };

    /* ========================================================
       CONNECT MODAL
       ======================================================== */
    function openConnectModal(plat) {
        const modal = document.getElementById("connect-modal");
        const title = document.getElementById("cm-title");
        if (!modal) return;

        const labels = {
            instagram: "Instagram",
            facebook: "Facebook",
            linkedin: "LinkedIn",
            x: "X (Twitter)",
            twitter: "X (Twitter)",
        };
        if (title) {
            title.textContent = "Connect " + (labels[plat] || "Platform");
        }

        modal.style.display = "flex";
    }

    /* Close modal on backdrop click */
    document.addEventListener("click", function (e) {
        const modal = document.getElementById("connect-modal");
        if (modal && e.target === modal) {
            modal.style.display = "none";
        }
    });

    /* ========================================================
       TWITTER CHAR COUNTER
       ======================================================== */
    function initCharCounter() {
        const twitterWrapper = document.getElementById("mock-twitter");
        if (!twitterWrapper) return;

        const contentEl = twitterWrapper.querySelector(".mock-x-content");
        if (!contentEl) return;

        /* Inject counter element */
        let counter = twitterWrapper.querySelector(".char-counter");
        if (!counter) {
            counter = document.createElement("div");
            counter.className = "char-counter";
            twitterWrapper.appendChild(counter);
        }

        function updateCounter() {
            const len = contentEl.innerText.replace(/\n$/, "").length;
            const remaining = 280 - len;
            counter.textContent = remaining + " / 280";
            counter.className = "char-counter" +
                (remaining < 0 ? " over" : remaining < 40 ? " warn" : "");
        }

        /* Run once on load, then on mutations */
        updateCounter();
        new MutationObserver(updateCounter).observe(contentEl, {
            childList: true, subtree: true, characterData: true
        });
    }

    /* ========================================================
       STEP HIGHLIGHT (validation nudge)
       ======================================================== */
    function highlightStep(stepNum, message) {
        const steps = document.querySelectorAll(".cp-step");
        const step = steps[stepNum - 1];
        if (!step) return;

        step.style.borderColor = "#EF4444";
        step.style.boxShadow = "0 0 0 3px rgba(239,68,68,0.1)";

        /* Remove after 2s */
        setTimeout(function () {
            step.style.borderColor = "";
            step.style.boxShadow = "";
        }, 2000);

        /* Optional: show a small tooltip */
        if (message) {
            let tip = step.querySelector(".cp-validation-tip");
            if (!tip) {
                tip = document.createElement("p");
                tip.className = "cp-validation-tip";
                tip.style.cssText =
                    "margin:6px 0 0; font-size:12px; color:#EF4444; font-weight:500;";
                step.appendChild(tip);
            }
            tip.textContent = message;
            setTimeout(function () { tip.remove(); }, 2500);
        }
    }

    /* ========================================================
       FOOTER VISIBILITY — show when a post is present
       ======================================================== */
    function syncFooterVisibility() {
        if (!mockFooter) return;
        const plat = state.selectedPlatform || hPlatform.value;
        const hasPost = getActiveMockContent();
        mockFooter.style.display = (plat && hasPost) ? "flex" : "none";
    }

    /* ========================================================
       BOOT
       ======================================================== */
    function init() {
        initPlatformBoxes();
        initTone();
        initCharCounter();
        syncFooterVisibility();

        /* Keep prompt input in sync with hidden field */
        if (visiblePrompt) {
            visiblePrompt.addEventListener("input", function () {
                hPrompt.value = visiblePrompt.value;
            });
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
    
    window.saveDraft = function() {
        hAction.value = "draft";
        hiddenForm.submit();
    };

    window.openScheduleModal = function() {
        const modal = document.getElementById("schedule-modal");
        const scheduleDate = document.getElementById("scheduleDate");
        const scheduleTime = document.getElementById("scheduleTime");
        
        if (scheduleDate && scheduleTime) {
            const now = new Date();
            const minTime = new Date(now.getTime());
            minTime.setMinutes(minTime.getMinutes() - minTime.getTimezoneOffset());
            
            const todayStr = minTime.toISOString().slice(0, 10);
            scheduleDate.min = todayStr;
            
            if (!scheduleDate.value || !scheduleTime.value) {
                const defaultTime = new Date(now.getTime());
                defaultTime.setHours(defaultTime.getHours() + 1);
                defaultTime.setMinutes(defaultTime.getMinutes() - defaultTime.getTimezoneOffset());
                
                const isoStr = defaultTime.toISOString();
                scheduleDate.value = isoStr.slice(0, 10);
                scheduleTime.value = isoStr.slice(11, 16);
            }
            
            // Dynamically enforce time constraint based on selected date
            const updateTimeMin = () => {
                const checkNow = new Date();
                const checkNowLocal = new Date(checkNow.getTime() - checkNow.getTimezoneOffset() * 60000);
                const currentTodayStr = checkNowLocal.toISOString().slice(0, 10);
                
                if (scheduleDate.value === currentTodayStr) {
                    scheduleTime.min = checkNowLocal.toISOString().slice(11, 16);
                } else {
                    scheduleTime.min = "";
                }
            };
            
            scheduleDate.addEventListener('change', updateTimeMin);
            updateTimeMin();
        }

        if (modal) modal.style.display = "flex";
    };

    window.closeScheduleModal = function() {
        const modal = document.getElementById("schedule-modal");
        if (modal) modal.style.display = "none";
    };

    window.confirmSchedule = function() {
        const scheduleDate = document.getElementById("scheduleDate");
        const scheduleTime = document.getElementById("scheduleTime");
        
        if (!scheduleDate.value || !scheduleTime.value) {
            alert("Please select both a valid date and time.");
            return;
        }
        
        const selectedDateTimeStr = scheduleDate.value + "T" + scheduleTime.value;
        const selectedDate = new Date(selectedDateTimeStr);
        const now = new Date();
        
        if (selectedDate <= now) {
            alert("You cannot schedule a post in the past! Please select a future date and time.");
            return;
        }
        
        const hScheduleTime = document.getElementById("hScheduleTime");
        if (hScheduleTime) {
            hScheduleTime.value = selectedDateTimeStr;
        }
        hAction.value = "schedule";
        hiddenForm.submit();
    };
})();