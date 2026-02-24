document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities", { cache: 'no-store' });
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Clear and reset activity select (keep the placeholder option)
      while (activitySelect.firstChild) {
        activitySelect.removeChild(activitySelect.firstChild);
      }
      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = '-- Select an activity --';
      activitySelect.appendChild(placeholder);

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        const participants = details.participants || [];
        const participantsHtml = participants.length > 0
          ? `<ul class="participants-list">${participants.map(p => `<li class="participant-item"><span class="participant-email">${p}</span><button class="participant-delete" data-activity="${encodeURIComponent(name)}" data-email="${encodeURIComponent(p)}" aria-label="Remove ${p}">&times;</button></li>`).join('')}</ul>`
          : `<p class="no-participants">No participants yet</p>`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-section">
            <h5>Participants</h5>
            ${participantsHtml}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Attach delete handlers for participant remove buttons
        activityCard.querySelectorAll('.participant-delete').forEach(btn => {
          btn.addEventListener('click', async (e) => {
            const encodedEmail = btn.dataset.email;
            const encodedActivity = btn.dataset.activity;
            const email = decodeURIComponent(encodedEmail);
            const activityName = decodeURIComponent(encodedActivity);

            if (!confirm(`Remove ${email} from ${activityName}?`)) return;

            try {
              const resp = await fetch(`/activities/${encodeURIComponent(activityName)}/participants?email=${encodeURIComponent(email)}`, { method: 'DELETE' });
              const data = await resp.json();
              if (resp.ok) {
                messageDiv.textContent = data.message;
                messageDiv.className = 'message success';
                messageDiv.classList.remove('hidden');
                await fetchActivities();
                setTimeout(() => messageDiv.classList.add('hidden'), 3000);
              } else {
                messageDiv.textContent = data.detail || 'Failed to remove participant';
                messageDiv.className = 'message error';
                messageDiv.classList.remove('hidden');
              }
            } catch (err) {
              messageDiv.textContent = 'Failed to remove participant';
              messageDiv.className = 'message error';
              messageDiv.classList.remove('hidden');
              console.error('Error removing participant:', err);
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "message success";
        signupForm.reset();
        // Refresh activities list to show the new participant
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "message error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "message error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
