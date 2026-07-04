/**
 * ASVS 4.2.4 — CRLF Header Injection Lab
 * Interactive Educational UI — Shared JavaScript
 *
 * Works for both the Secure (port 5000) and Vulnerable (port 5001) apps.
 * Detects which mode it's in from the <body class="mode-secure|mode-vulnerable">.
 */

'use strict';

// ─────────────────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Escape HTML special characters so values can be safely inserted via innerHTML.
 */
function esc(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/**
 * Return a human-readable label for a character code.
 * Highlights control characters.
 */
function charLabel(char) {
  const code = char.charCodeAt(0);
  const hex = '0x' + code.toString(16).toUpperCase().padStart(2, '0');
  if (code === 0x0d) return { label: '\\r (CR)', ctrl: true, hex };
  if (code === 0x0a) return { label: '\\n (LF)', ctrl: true, hex };
  if (code < 0x20)   return { label: `CTL ${hex}`, ctrl: true, hex };
  return { label: char, ctrl: false, hex };
}

// ─────────────────────────────────────────────────────────────────────────────
// Byte Visualizer
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Renders a byte-by-byte visualization of a string into the #byte-visualizer div.
 * Control characters are shown in red with their escape sequence.
 */
function updateByteVisualizer(value) {
  const container = document.getElementById('byte-visualizer');
  if (!container) return;

  if (!value) {
    container.innerHTML = '<span style="color:var(--text-muted);font-size:0.75rem;">(empty)</span>';
    return;
  }

  const chips = [];
  for (const char of value) {
    const { label, ctrl } = charLabel(char);
    const cls = 'byte-chip' + (ctrl ? ' ctrl-char' : '');
    chips.push(`<span class="${cls}" title="${charLabel(char).hex}">${esc(label)}</span>`);
  }

  // Limit display to 40 chars to avoid overflow
  if (value.length > 40) {
    container.innerHTML = chips.slice(0, 40).join('') +
      `<span class="byte-chip" style="color:var(--text-muted)">… +${value.length - 40} more</span>`;
  } else {
    container.innerHTML = chips.join('');
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Result Panel Renderer
// ─────────────────────────────────────────────────────────────────────────────

function showResult(data, httpStatus) {
  const placeholder = document.getElementById('result-placeholder');
  const panel       = document.getElementById('result-panel');
  if (!placeholder || !panel) return;

  placeholder.classList.add('hidden');
  panel.classList.remove('hidden');

  // ── Verdict Banner ──────────────────────────────────────────────────────
  const banner  = document.getElementById('verdict-banner');
  const verdict = data.verdict || (httpStatus < 300 ? 'ACCEPTED' : 'REJECTED');

  if (verdict === 'REJECTED') {
    banner.className = 'verdict-banner rejected';
    banner.innerHTML = '❌ REJECTED — Request blocked due to CRLF sequences in header';
  } else if (verdict === 'ACCEPTED_WITHOUT_VALIDATION') {
    banner.className = 'verdict-banner accepted-no-validation';
    banner.innerHTML = '⚠️ ACCEPTED WITHOUT VALIDATION — CRLF not checked (ASVS FAIL)';
  } else if (verdict === 'ACCEPTED') {
    if (data.asvs_pass === false) {
      banner.className = 'verdict-banner accepted-no-validation';
      banner.innerHTML = '⚠️ ACCEPTED (No validation performed) — ASVS 4.2.4 FAIL';
    } else {
      banner.className = 'verdict-banner accepted';
      banner.innerHTML = '✅ ACCEPTED — Header passed CRLF validation';
    }
  } else {
    banner.className = 'verdict-banner accepted-no-validation';
    banner.innerHTML = `⚠️ ${esc(verdict)}`;
  }

  // ── ASVS Status ─────────────────────────────────────────────────────────
  const asvsStatus = document.getElementById('asvs-status');
  if (asvsStatus) {
    if (data.asvs_pass === true) {
      asvsStatus.className = 'result-value asvs-pass';
      asvsStatus.textContent = '✅ PASS';
    } else {
      asvsStatus.className = 'result-value asvs-fail';
      asvsStatus.textContent = '❌ FAIL';
    }
  }

  // ── Header Name / Value ──────────────────────────────────────────────────
  const nameEl = document.getElementById('res-header-name');
  if (nameEl) nameEl.textContent = data.header_name || '—';

  const valueEl = document.getElementById('res-header-value');
  if (valueEl) valueEl.textContent = data.header_value_repr || data.header_value || '—';

  // ── Violations ───────────────────────────────────────────────────────────
  const violRow = document.getElementById('violations-row');
  const violList = document.getElementById('violations-list');
  if (violRow && violList) {
    if (data.violations && data.violations.length > 0) {
      violRow.classList.remove('hidden');
      violList.innerHTML = data.violations
        .map(v => `<div class="violation-item">${esc(v)}</div>`)
        .join('');
    } else {
      violRow.classList.add('hidden');
    }
  }

  // ── Attack Type (vulnerable only) ────────────────────────────────────────
  const attackTypeRow  = document.getElementById('attack-type-row');
  const attackTypeText = document.getElementById('attack-type-text');
  if (attackTypeRow && attackTypeText) {
    if (data.attack_type_demonstrated) {
      attackTypeRow.classList.remove('hidden');
      attackTypeText.textContent = data.attack_type_demonstrated;
    } else {
      attackTypeRow.classList.add('hidden');
    }
  }

  // ── Missing Control (vulnerable only) ────────────────────────────────────
  const missingRow  = document.getElementById('missing-control-row');
  const missingText = document.getElementById('missing-control-text');
  if (missingRow && missingText) {
    if (data.missing_control) {
      missingRow.classList.remove('hidden');
      missingText.textContent = data.missing_control;
    } else {
      missingRow.classList.add('hidden');
    }
  }

  // ── Explanation ──────────────────────────────────────────────────────────
  const explText = document.getElementById('explanation-text');
  if (explText) explText.textContent = data.explanation || '';

  // ── Attacks Prevented (secure only) ─────────────────────────────────────
  const preventedSection = document.getElementById('attack-prevented-section');
  const attackList       = document.getElementById('attack-list');
  if (preventedSection && attackList) {
    if (data.attack_prevented && data.attack_prevented.length > 0) {
      preventedSection.classList.remove('hidden');
      attackList.innerHTML = data.attack_prevented
        .map(a => `<li>${esc(a)}</li>`)
        .join('');
    } else {
      preventedSection.classList.add('hidden');
    }
  }

  // ── HTTP/1.1 Injection Simulation ────────────────────────────────────────
  const httpSimSection = document.getElementById('http-sim-section');
  const httpSimPre     = document.getElementById('http-sim-pre');
  if (httpSimSection && httpSimPre) {
    if (data.simulated_http1_injection) {
      httpSimSection.classList.remove('hidden');
      // Highlight \r and \n in the simulation
      const highlighted = highlightCrlf(data.simulated_http1_injection);
      httpSimPre.innerHTML = highlighted;
    } else {
      httpSimSection.classList.add('hidden');
    }
  }

  // ── Log Injection Preview (vulnerable only) ──────────────────────────────
  const logSection = document.getElementById('log-inject-section');
  const logPre     = document.getElementById('log-inject-pre');
  if (logSection && logPre) {
    if (data.log_injection_note) {
      logSection.classList.remove('hidden');
      logPre.textContent = buildLogSample(data.header_value_repr || '');
    } else {
      logSection.classList.add('hidden');
    }
  }

  // ── Secure Comparison (vulnerable only) ──────────────────────────────────
  const secureCompText = document.getElementById('secure-comparison-text');
  if (secureCompText) {
    if (data.what_secure_does) {
      secureCompText.textContent = data.what_secure_does;
    } else if (data.asvs_pass === true) {
      secureCompText.textContent =
        'Both implementations accept this clean header. No difference in behaviour.';
    }
  }

  // ── RFC Section (secure only) ────────────────────────────────────────────
  const rfcSection = document.getElementById('rfc-section');
  const rfcList    = document.getElementById('rfc-list');
  if (rfcSection && rfcList) {
    if (data.relevant_rfcs && data.relevant_rfcs.length > 0) {
      rfcSection.classList.remove('hidden');
      rfcList.innerHTML = data.relevant_rfcs
        .map(r => `<li>${esc(r)}</li>`)
        .join('');
    } else if (rfcSection) {
      rfcSection.classList.add('hidden');
    }
  }
}

/**
 * Highlights \r and \n in a string for display in code blocks.
 */
function highlightCrlf(str) {
  return esc(str)
    .replace(/\\r\\n/g, '<span style="background:rgba(239,68,68,0.25);color:#fca5a5;border-radius:3px;padding:1px 3px">\\r\\n</span>')
    .replace(/\\r/g,   '<span style="background:rgba(249,115,22,0.25);color:#fdba74;border-radius:3px;padding:1px 3px">\\r</span>')
    .replace(/\\n/g,   '<span style="background:rgba(234,179,8,0.25);color:#fef08a;border-radius:3px;padding:1px 3px">\\n</span>');
}

/**
 * Build a fake log sample showing what log injection would produce.
 */
function buildLogSample(valueRepr) {
  const ts = new Date().toISOString();
  return [
    `${ts} [VULNERABLE] INFO Processing header: value=${valueRepr}`,
    `  ↑ If the value above contains \\n, the log entry splits here ↓`,
    `${ts} [VULNERABLE] INFO [INJECTED LINE] ADMIN LOGIN SUCCESSFUL`,
    `  ← This second line was injected by the attacker via \\n in the header value`
  ].join('\n');
}

// ─────────────────────────────────────────────────────────────────────────────
// Form Handler
// ─────────────────────────────────────────────────────────────────────────────

function initForm() {
  const form        = document.getElementById('header-test-form');
  const submitBtn   = document.getElementById('submit-btn');
  const nameInput   = document.getElementById('header-name');
  const valueInput  = document.getElementById('header-value');

  if (!form) return;

  // Update byte visualizer on input
  if (valueInput) {
    valueInput.addEventListener('input', () => {
      updateByteVisualizer(valueInput.value);
    });
    updateByteVisualizer(valueInput.value);
  }

  // Preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const name  = btn.dataset.name  || '';
      const value = btn.dataset.value || '';

      if (nameInput)  nameInput.value  = name;
      if (valueInput) {
        valueInput.value = value;
        updateByteVisualizer(value);
      }
    });
  });

  // Form submit
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const headerName  = nameInput  ? nameInput.value.trim()  : '';
    const headerValue = valueInput ? valueInput.value         : '';

    if (!headerName) {
      nameInput.focus();
      nameInput.style.borderColor = 'var(--vuln-primary)';
      setTimeout(() => { nameInput.style.borderColor = ''; }, 2000);
      return;
    }

    // Loading state
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add('loading');
    }

    try {
      const resp = await fetch('/api/validate-header', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          header_name:  headerName,
          header_value: headerValue,
        }),
      });

      let data = {};
      try { data = await resp.json(); } catch (_) {}

      showResult(data, resp.status);

    } catch (err) {
      showResult({
        verdict: 'ERROR',
        asvs_pass: false,
        explanation: `Network error: ${err.message}. Is the Docker container running?`,
        header_name: headerName,
        header_value_repr: repr(headerValue),
      }, 0);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
      }
    }
  });
}

/**
 * Minimal Python-style repr for display.
 */
function repr(str) {
  return "'" + str
    .replace(/\\/g, '\\\\')
    .replace(/'/g, "\\'")
    .replace(/\r/g, '\\r')
    .replace(/\n/g, '\\n')
    .replace(/\t/g, '\\t') + "'";
}

// ─────────────────────────────────────────────────────────────────────────────
// Initialise
// ─────────────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  initForm();

  // Smooth scroll for any anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
