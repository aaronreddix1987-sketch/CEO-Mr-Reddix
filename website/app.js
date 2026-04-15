// ===========================
// TTI — Total Transformation Inc.
// App JavaScript — IQ-200 Einstein Mode
// ===========================

// ===== NAV SCROLL EFFECT =====
window.addEventListener('scroll', () => {
  const nav = document.getElementById('navbar');
  if (window.scrollY > 50) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
});

// ===== MOBILE NAV TOGGLE =====
function toggleNav() {
  const mobileNav = document.getElementById('mobile-nav');
  mobileNav.classList.toggle('open');
}

// ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) {
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ===== LEAD FORM SUBMISSION =====
function submitLead(e) {
  e.preventDefault();

  const name = document.getElementById('lead-name').value;
  const business = document.getElementById('lead-business').value;
  const phone = document.getElementById('lead-phone').value;
  const email = document.getElementById('lead-email').value;
  const industry = document.getElementById('lead-industry').value;
  const revenue = document.getElementById('lead-revenue').value;
  const challenge = document.getElementById('lead-challenge').value;

  const services = [];
  document.querySelectorAll('.checkbox-group input:checked').forEach(cb => {
    services.push(cb.value);
  });

  if (!name || !business || !phone || !email || !industry) {
    alert('Please fill in all required fields.');
    return;
  }

  const btn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btn-text');
  const btnLoading = document.getElementById('btn-loading');

  btn.disabled = true;
  btnText.style.display = 'none';
  btnLoading.style.display = 'inline';

  // Simulate AI processing
  setTimeout(() => {
    // Log lead to console (in production, this would POST to a backend)
    const lead = {
      id: 'TTI-LEAD-' + Date.now(),
      timestamp: new Date().toISOString(),
      name, business, phone, email, industry, revenue, challenge, services,
      status: 'NEW',
      source: 'TTI Website — AI Lead Engine',
      assigned_to: 'Aaron T. Reddix — 747-301-8586'
    };

    console.log('🚀 NEW TTI LEAD CAPTURED:', JSON.stringify(lead, null, 2));

    // Add to live ticker
    addToTicker(name, business, industry, services[0] || 'AI Sales Automation');

    // Show success
    document.getElementById('leadForm').style.display = 'none';
    document.getElementById('leadSuccess').style.display = 'block';

    // Scroll to success message
    document.getElementById('leadSuccess').scrollIntoView({ behavior: 'smooth', block: 'center' });

  }, 2000);
}

// ===== ADD NEW LEAD TO TICKER =====
function addToTicker(name, business, industry, service) {
  const ticker = document.getElementById('leadsTicker');
  const item = document.createElement('div');
  item.className = 'ticker-item';

  const industryMap = {
    'real-estate': 'Real Estate Agent',
    'medical': 'Medical Practice',
    'coaching': 'High-Ticket Coach',
    'mortgage': 'Mortgage Broker',
    'insurance': 'Insurance Agency',
    'legal': 'Law Firm',
    'other': 'Business'
  };

  const serviceMap = {
    'ai-sales': 'AI Sales Automation',
    'voice-agent': 'AI Voice Agent',
    'credit-repair': 'Business Credit',
    'real-estate': 'Real Estate Partnership'
  };

  const displayIndustry = industryMap[industry] || industry;
  const displayService = serviceMap[service] || service;

  item.innerHTML = `<span class="ticker-badge">NEW</span> ${name} — ${business} (${displayIndustry}) — ${displayService} — <strong>Proposal Queued</strong>`;

  ticker.insertBefore(item, ticker.firstChild);
}

// ===== LIVE TICKER ANIMATION =====
const tickerMessages = [
  { badge: 'CLOSED', text: 'Dr. Williams — Cedars-Sinai — AI Voice Agent — <strong>$7,500 setup</strong>' },
  { badge: 'DEMO', text: 'Amanda R. — Keller Williams — AI Appointment Setting — <strong>Demo booked</strong>' },
  { badge: 'HOT', text: 'James T. — High-Ticket Coach — Enterprise AI — <strong>$10K proposal reviewing</strong>' },
  { badge: 'CLOSED', text: 'Patricia M. — eXp Realty — AI Lead Follow-Up — <strong>$497/mo</strong>' },
  { badge: 'DEMO', text: 'Dr. Nguyen — UCLA Health — AI Patient Booking — <strong>Demo confirmed</strong>' },
  { badge: 'CLOSED', text: 'Carlos B. — Mortgage Pro — AI Qualification — <strong>$497/mo</strong>' },
  { badge: 'HOT', text: 'Rachel K. — Insurance Agency — AI Outreach — <strong>Proposal sent</strong>' },
  { badge: 'CLOSED', text: 'Thomas H. — Compass Realty — AI System — <strong>$497/mo</strong>' },
];

let tickerIndex = 0;

function rotateTicker() {
  const ticker = document.getElementById('leadsTicker');
  if (!ticker) return;

  const msg = tickerMessages[tickerIndex % tickerMessages.length];
  const item = document.createElement('div');
  item.className = 'ticker-item';
  item.innerHTML = `<span class="ticker-badge">${msg.badge}</span> ${msg.text}`;

  // Remove oldest if more than 12 items
  if (ticker.children.length >= 12) {
    ticker.removeChild(ticker.lastChild);
  }

  ticker.insertBefore(item, ticker.firstChild);
  tickerIndex++;
}

// Rotate ticker every 8 seconds
setInterval(rotateTicker, 8000);

// ===== INTERSECTION OBSERVER — ANIMATE ON SCROLL =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

// Observe cards and sections
document.querySelectorAll('.service-card, .result-card, .legal-card, .step, .contact-method').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// Add visible class styles
const style = document.createElement('style');
style.textContent = `
  .service-card.visible, .result-card.visible, .legal-card.visible, .step.visible, .contact-method.visible {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
`;
document.head.appendChild(style);

// ===== COUNTER ANIMATION =====
function animateCounter(el, target, prefix = '', suffix = '') {
  let current = 0;
  const increment = target / 60;
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = prefix + Math.floor(current).toLocaleString() + suffix;
  }, 16);
}

// Animate stats when hero is visible
const heroObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const statNums = document.querySelectorAll('.stat-num');
      statNums.forEach(el => {
        const text = el.textContent;
        if (text === '93') animateCounter(el, 93);
        if (text === '$1M+') { el.textContent = '$0'; animateCounter(el, 1007488, '$', ''); setTimeout(() => el.textContent = '$1M+', 1500); }
        if (text === '$6.76M') { el.textContent = '$0'; setTimeout(() => el.textContent = '$6.76M', 1500); }
        if (text === '1,200+') { el.textContent = '0'; animateCounter(el, 1200, '', '+'); }
      });
      heroObserver.disconnect();
    }
  });
}, { threshold: 0.3 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroObserver.observe(heroStats);

// ===== CONSOLE BRANDING =====
console.log(`
%c
████████╗████████╗██╗
╚══██╔══╝╚══██╔══╝██║
   ██║      ██║   ██║
   ██║      ██║   ██║
   ╚═╝      ╚═╝   ╚═╝

TOTAL TRANSFORMATION INC.
IQ-200 Einstein Mode | No Human System
CEO: Aaron T. Reddix | 747-301-8586
aaronreddix1987@gmail.com
`, 'color: #C9A84C; font-family: monospace; font-size: 12px;');
