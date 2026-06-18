document.addEventListener("DOMContentLoaded", () => {
    const accountsList = document.querySelectorAll(".account-item");
    const titleElement = document.getElementById("scheduler-title");
    const postsContainer = document.getElementById("posts-container");

    // Simulated Dynamic Dataset Schema Layout Mapping
    const accountDatabase = {
        facebook: {
            title: "All Scheduled Posts for Somya Mehra (Facebook)",
            badgeColor: "bg-facebook",
            icon: "fab fa-facebook-f",
            posts: [
                { title: "Beautiful sunset view 🌅", tags: "#nature #sunset #photography", date: "12 Jun 2026", time: "09:00 AM", img: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=80&auto=format&fit=crop" },
                { title: "Start your day with coffee ...", tags: "#coffee #morning #motivation", date: "12 Jun 2026", time: "01:00 PM", img: "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=80&auto=format&fit=crop" },
                { title: "Productivity tips you should...", tags: "#productivity #tips #success", date: "13 Jun 2026", time: "10:30 AM", img: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=80&auto=format&fit=crop" }
            ]
        },
        instagram: {
            title: "All Scheduled Posts for Somya Mehra (Instagram)",
            badgeColor: "bg-instagram",
            icon: "fab fa-instagram",
            posts: [
                { title: "OOTD Summer Outfits Collection 👗", tags: "#fashion #style #summer", date: "18 Jun 2026", time: "04:00 PM", img: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=80&auto=format&fit=crop" }
            ]
        },
        twitter: {
            title: "All Scheduled Posts (Twitter)",
            posts: [],
            badgeColor: "bg-twitter",
            icon: "fab fa-x-twitter"
        },
        linkedin: {
            title: "All Scheduled Posts (LinkedIn)",
            posts: [],
            badgeColor: "bg-linkedin",
            icon: "fab fa-linkedin-in"
        }
    };

    // Click handler for Account List tabs selection switcher
    accountsList.forEach(item => {
        item.addEventListener("click", (e) => {
            // Allow native redirect behaviors if user clicks the actual connect link anchor tag button
            if (e.target.classList.contains('btn-connect')) {
                return;
            }

            // Guard clause: block background container tab selection clicks if channel profile status is unconnected
            if (!item.classList.contains('active') && item.querySelector('.btn-connect')) {
                return;
            }

            // Switch layout active selection visually
            accountsList.forEach(i => i.classList.remove("active"));
            item.classList.add("active");

            const accountKey = item.getAttribute("data-account");
            const platformData = accountDatabase[accountKey];

            if (platformData) {
                titleElement.innerText = platformData.title;
                renderPosts(platformData);
            }
        });
    });

    // Render Function inside posts feed section
    function renderPosts(platform) {
        if (platform.posts.length === 0) {
            postsContainer.innerHTML = `
                <div class="empty-state">
                    <i class="far fa-folder-open"></i>
                    No scheduled posts found for this channel.
                </div>`;
            return;
        }

        postsContainer.innerHTML = platform.posts.map(post => `
            <div class="post-row">
                <div class="post-media-preview">
                    <img src="${post.img}" alt="Preview">
                    <div class="platform-overlay-badge ${platform.badgeColor}"><i class="${platform.icon}"></i></div>
                </div>
                <div>
                    <h5 class="post-title">${post.title}</h5>
                    <p class="post-tags">${post.tags}</p>
                </div>
                <div class="post-datetime">
                    <div>${post.date}</div>
                    <div class="time-muted">${post.time}</div>
                </div>
                <div class="post-actions">
                    <span class="badge-scheduled">Scheduled</span>
                    <button class="btn-more"><i class="fas fa-ellipsis-v"></i></button>
                </div>
            </div>
        `).join('');
    }
});