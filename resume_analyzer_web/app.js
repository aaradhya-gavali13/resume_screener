/**
 * NEXUS RESUME AI - UI & APPLICATION CONTROLLER
 */

document.addEventListener('DOMContentLoaded', () => {
  const {
    JOB_ROLES,
    SAMPLE_RESUME_TEXT,
    audio,
    analyzeResume,
    extractTextFromPDF,
    extractTextFromDOCX
  } = window.NexusAnalyzer;

  // DOM Elements
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const pasteBtn = document.getElementById('pasteResumeBtn');
  const pasteModal = document.getElementById('pasteModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const cancelModalBtn = document.getElementById('cancelModalBtn');
  const analyzePastedBtn = document.getElementById('analyzePastedBtn');
  const pastedResumeText = document.getElementById('pastedResumeText');
  const soundToggleBtn = document.getElementById('soundToggleBtn');
  const soundStatusText = document.getElementById('soundStatusText');
  const printDossierBtn = document.getElementById('printDossierBtn');
  const resetBtn = document.getElementById('resetBtn');

  // Results Section
  const resultsSection = document.getElementById('resultsSection');
  const topMatchesList = document.getElementById('topMatchesList');
  const candidateProgramsEl = document.getElementById('candidatePrograms');
  const candidateSkillsCloud = document.getElementById('candidateSkillsCloud');
  const allRolesMatrix = document.getElementById('allRolesMatrix');

  // Persistent Backend URL (silent auto-connection without UI setup popups)
  const DEFAULT_BACKEND_URL = "https://resume-screener.onrender.com";
  let activeBackendUrl = localStorage.getItem('nexus_backend_url') || DEFAULT_BACKEND_URL;

  // Telemetry Counters
  const telemetryDegree = document.getElementById('telemetryDegree');
  const telemetrySkillsCount = document.getElementById('telemetrySkillsCount');
  const telemetryTopRole = document.getElementById('telemetryTopRole');
  const telemetryReadiness = document.getElementById('telemetryReadiness');

  // Audio Toggle
  let audioEnabled = true;
  soundToggleBtn.addEventListener('click', () => {
    audioEnabled = !audioEnabled;
    audio.enabled = audioEnabled;
    soundStatusText.textContent = audioEnabled ? 'AUDIO: ON' : 'AUDIO: MUTED';
    soundToggleBtn.style.opacity = audioEnabled ? '1' : '0.5';
    if (audioEnabled) audio.scanBleep();
  });

  // Modal Handlers
  pasteBtn.addEventListener('click', () => {
    audio.clickBlip();
    pasteModal.classList.add('active');
    pastedResumeText.focus();
  });

  const closeModal = () => {
    audio.clickBlip();
    pasteModal.classList.remove('active');
  };
  closeModalBtn.addEventListener('click', closeModal);
  cancelModalBtn.addEventListener('click', closeModal);

  analyzePastedBtn.addEventListener('click', () => {
    const text = pastedResumeText.value.trim();
    if (!text) {
      alert("Please paste resume text before analyzing.");
      return;
    }
    closeModal();
    executeAnalysisPipeline(text, "Pasted_Resume_Text.txt");
  });

  // Drag & Drop
  dropzone.addEventListener('click', () => fileInput.click());

  ['dragenter', 'dragover'].forEach(event => {
    dropzone.addEventListener(event, (e) => {
      e.preventDefault();
      dropzone.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach(event => {
    dropzone.addEventListener(event, (e) => {
      e.preventDefault();
      dropzone.classList.remove('drag-over');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });

  // File Upload Processor with Cloud / Local Hybrid Execution
  async function handleFileUpload(file) {
    audio.clickBlip();
    const fileName = file.name;
    const extension = fileName.split('.').pop().toLowerCase();

    triggerScanAnimation(true);

    try {
      // 1. If Render backend is configured, attempt backend upload
      if (activeBackendUrl) {
        try {
          const formData = new FormData();
          formData.append('file', file);

          const response = await fetch(`${activeBackendUrl}/analyze`, {
            method: 'POST',
            body: formData
          });

          if (response.ok) {
            const results = await response.json();
            triggerScanAnimation(false);
            audio.successChime();
            renderDashboard(results, fileName + " (Render Cloud API)");
            return;
          }
        } catch (backendErr) {
          console.warn("Backend request failed or warming up, executing local client fallback:", backendErr);
        }
      }

      // 2. Client-side extraction fallback
      let extractedText = "";

      if (extension === "pdf") {
        const buffer = await file.arrayBuffer();
        extractedText = await extractTextFromPDF(buffer);
      } else if (extension === "docx") {
        const buffer = await file.arrayBuffer();
        extractedText = await extractTextFromDOCX(buffer);
      } else if (extension === "txt") {
        extractedText = await file.text();
      } else {
        throw new Error("Unsupported format. Please upload PDF, DOCX, or TXT.");
      }

      if (!extractedText.trim()) {
        throw new Error("No readable text found in document.");
      }

      executeAnalysisPipeline(extractedText, fileName);
    } catch (err) {
      triggerScanAnimation(false);
      alert("Analysis Error: " + err.message);
    }
  }

  // Holographic Scanner Animation Trigger
  function triggerScanAnimation(active) {
    if (active) {
      dropzone.classList.add('scanning');
      audio.scanBleep();
    } else {
      dropzone.classList.remove('scanning');
    }
  }

  // Execution Pipeline
  async function executeAnalysisPipeline(text, sourceName) {
    triggerScanAnimation(true);

    if (activeBackendUrl) {
      try {
        const response = await fetch(`${activeBackendUrl}/analyze-json`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });

        if (response.ok) {
          const results = await response.json();
          triggerScanAnimation(false);
          audio.successChime();
          renderDashboard(results, sourceName + " (Render Cloud API)");
          return;
        }
      } catch (err) {
        console.warn("Render backend call timed out/failed. Falling back to local engine.", err);
      }
    }

    setTimeout(() => {
      triggerScanAnimation(false);
      const results = analyzeResume(text);
      audio.successChime();
      renderDashboard(results, sourceName);
    }, 500);
  }

  // Render Dashboard
  function renderDashboard(results, sourceName) {
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    // 1. Telemetry Bar
    const topRole = results.topRoles[0];
    telemetryDegree.textContent = results.candidatePrograms.length > 0 
      ? results.candidatePrograms.join(", ") 
      : "Not Detected";
    telemetrySkillsCount.textContent = results.candidateSkills.length;
    telemetryTopRole.textContent = topRole ? topRole.role : "N/A";
    telemetryReadiness.textContent = topRole ? `${topRole.score}%` : "0%";

    // 2. Candidate Programs Badges
    candidateProgramsEl.innerHTML = '';
    if (results.candidatePrograms.length > 0) {
      results.candidatePrograms.forEach(prog => {
        const badge = document.createElement('span');
        badge.className = 'program-badge';
        badge.textContent = `✓ ${prog}`;
        candidateProgramsEl.appendChild(badge);
      });
    } else {
      candidateProgramsEl.innerHTML = '<span style="color: var(--text-dim); font-size: 0.85rem;">No degree identified</span>';
    }

    // 3. All Skills Cloud
    candidateSkillsCloud.innerHTML = '';
    if (results.candidateSkills.length > 0) {
      results.candidateSkills.forEach(skill => {
        const chip = document.createElement('span');
        chip.className = 'skill-chip matched';
        chip.innerHTML = `✓ ${skill}`;
        candidateSkillsCloud.appendChild(chip);
      });
    } else {
      candidateSkillsCloud.innerHTML = '<span style="color: var(--text-dim); font-size: 0.85rem;">No technical skills recognized</span>';
    }

    // 4. Top 5 Job Match Cards
    topMatchesList.innerHTML = '';
    results.topRoles.forEach((roleResult, index) => {
      const card = createJobMatchCard(roleResult, index + 1);
      topMatchesList.appendChild(card);
    });

    // 5. Full 14-Role Comparison Matrix
    renderRoleMatrix(results.allRoles);

    // Animate Progress Rings
    setTimeout(() => {
      document.querySelectorAll('.radial-bar-circle').forEach(circle => {
        const score = parseFloat(circle.getAttribute('data-score'));
        // Circumference is 2 * Math.PI * 30 ≈ 188.5
        const offset = 188.5 - (188.5 * score) / 100;
        circle.style.strokeDashoffset = offset;
      });
    }, 100);
  }

  // Create Job Match Card Element
  function createJobMatchCard(roleData, rank) {
    const card = document.createElement('div');
    card.className = `job-match-card ${rank === 1 ? 'rank-1' : ''}`;

    const strokeColor = roleData.tier.glow;

    // Matched skills chips HTML
    const matchedChipsHtml = roleData.matchedSkills.length > 0
      ? roleData.matchedSkills.map(s => `<span class="skill-chip matched">✓ ${s}</span>`).join('')
      : '<span style="color: var(--text-dim); font-size: 0.8rem;">None matched</span>';

    // Missing skills chips HTML with color diversity
    const missingChipsHtml = roleData.allMissingDetails && roleData.allMissingDetails.length > 0
      ? roleData.allMissingDetails.map(item => {
          let priorityClass = 'missing-rec';
          if (item.weight >= 12) priorityClass = 'missing-critical';
          else if (item.weight >= 8) priorityClass = 'missing-high';
          else if (item.weight >= 4) priorityClass = 'missing-medium';
          return `<span class="skill-chip ${priorityClass}">✕ ${item.skill}</span>`;
        }).join('')
      : '<span style="color: var(--emerald-neon); font-size: 0.8rem;">All required skills present!</span>';

    // Improvements HTML with color-coded priority pills (no numeric backend values)
    const improvementsHtml = roleData.improvements.length > 0
      ? `
        <div class="improvements-block">
          <div class="improvements-header">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
            STRATEGIC UPSKILLING ROADMAP
          </div>
          <ul class="improvements-list">
            ${roleData.improvements.map(imp => `
              <li class="improvement-item">
                <div class="improvement-content">
                  <span class="improvement-text">${imp.action}</span>
                  <span class="priority-pill ${imp.priorityClass}">${imp.priorityLevel}</span>
                </div>
              </li>
            `).join('')}
          </ul>
        </div>
      `
      : '';

    card.innerHTML = `
      <div class="card-top-row">
        <div class="role-title-group">
          <div class="rank-badge">#${rank}</div>
          <div>
            <h3 class="role-name">${roleData.role}</h3>
            <div class="role-category">${roleData.category} // ${roleData.description}</div>
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 16px;">
          <div class="tier-badge ${roleData.tier.class}">${roleData.tier.name}</div>
          <div class="radial-progress-wrapper">
            <svg class="radial-svg" viewBox="0 0 72 72">
              <circle class="radial-bg-circle" cx="36" cy="36" r="30"></circle>
              <circle class="radial-bar-circle" cx="36" cy="36" r="30" 
                data-score="${roleData.score}" 
                style="stroke: ${strokeColor};">
              </circle>
            </svg>
            <span class="radial-score-text">${roleData.score}%</span>
          </div>
        </div>
      </div>

      <div class="card-badges-row">
        <div class="education-pill ${roleData.educationMatch ? 'matched' : 'unmatched'}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
            <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
          </svg>
          ${roleData.educationMatch ? 'DEGREE: MATCHED' : 'DEGREE: NOT SPECIFIED AS PREREQUISITE'}
        </div>
        <div class="education-pill matched" style="background: rgba(0, 240, 255, 0.08); color: var(--cyan-neon); border-color: rgba(0, 240, 255, 0.25);">
          SKILLS ALIGNMENT: ${roleData.skillScore}%
        </div>
      </div>

      <div class="skills-block">
        <div class="skills-block-title">MATCHED SKILLS (${roleData.matchedSkills.length})</div>
        <div class="chips-cloud">${matchedChipsHtml}</div>
      </div>

      <div class="skills-block">
        <div class="skills-block-title">MISSING TARGET SKILLS (${roleData.missingSkills.length})</div>
        <div class="chips-cloud">${missingChipsHtml}</div>
      </div>

      ${improvementsHtml}
    `;

    return card;
  }

  // Render Full 14-Role Matrix
  function renderRoleMatrix(allRoles) {
    allRolesMatrix.innerHTML = '';
    allRoles.forEach(item => {
      const row = document.createElement('div');
      row.className = 'matrix-row';
      row.innerHTML = `
        <div class="matrix-role-name">${item.role}</div>
        <div class="matrix-bar-wrap">
          <div class="mini-score-bar-bg">
            <div class="mini-score-bar-fill" style="width: ${item.score}%;"></div>
          </div>
          <span class="matrix-score-val">${item.score}%</span>
        </div>
      `;
      allRolesMatrix.appendChild(row);
    });
  }

  // Print Dossier
  printDossierBtn.addEventListener('click', () => {
    audio.clickBlip();
    window.print();
  });

  // Reset Button
  resetBtn.addEventListener('click', () => {
    audio.clickBlip();
    resultsSection.style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
