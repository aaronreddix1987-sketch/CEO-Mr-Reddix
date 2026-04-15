// ===========================
// TTI — Total Transformation Inc.
// App JavaScript — IQ-200 Einstein Mode
// Frameworks: Martell + Hormozi + Cardone + Brunson + Ovens
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
    // Close mobile nav if open
    const mobileNav = document.getElementById('mobile-nav');
    if (mobileNav.classList.contains('open')) {
      mobileNav.classList.remove('open');
    }
  });
});

// ===== COUNTDOWN TIMER (Cardone Urgency) =====
function startCountdown() {
  // Set deadline to end of month
  const now = new Date();
  const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);
  
  function update() {
    const now = new Date();
    const diff = endOfMonth - now;
    
    if (diff <= 0) return;
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    const daysEl = document.getElementById('cd-days');
    const hoursEl = document.getElementById('cd-hours');
    const minEl = document.getElementById('cd-min');
    const secEl = document.getElementById('cd-sec');
    
    if (daysEl) daysEl.textContent = String(days).padStart(2, '0');
    if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
    if (minEl) minEl.textContent = String(minutes).padStart(2, '0');
    if (secEl) secEl.textContent = String(seconds).padStart(2, '0');
  }
  
  update();
  setInterval(update, 1000);
}

startCountdown();

// ===== LEAD FORM SUBMISSION (Ovens Application Funnel) =====
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
    alert('Please fill in all required fields to submit your application.');
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
    const lead = {
      id: 'TTI-LEAD-' + Date.now(),
      timestamp: new Date().toISOString(),
      name, business, phone, email, industry, revenue, challenge, services,
      status: 'NEW — APPLICATION RECEIVED',
      source: 'TTI Website — Hormozi Grand Slam Funnel',
      assigned_to: 'Aaron T. Reddix — 747-301-8586',
      guarantee: '90-Day Performance Guarantee Active'
    };

    console.log('NEW TTI APPLICATION:', JSON.stringify(lead, null, 2));

    // Add to live ticker
    addToTicker(name, business, industry, services[0] || 'AI Sales Automation');

    // Show success
    document.getElementById('leadForm').style.display = 'none';
    document.getElementById('leadSuccess').style.display = 'block';
    document.getElementById('leadSuccess').scrollIntoView({ behavior: 'smooth', block: 'center' });

  }, 2500);
}

// ===== ADD NEW LEAD TO TICKER =====
function addToTicker(name, business, industry, service) {
  const ticker = document.getElementById('leadsTicker');
  const item = document.createElement('div');
  item.className = 'ticker-item';

  const industryMap = {
    'real-estate': 'Real Estate',
    'medical': 'Medical Practice',
    'coaching': 'High-Ticket Coach',
    'mortgage': 'Mortgage Broker',
    'insurance': 'Insurance Agency',
    'legal': 'Law Firm',
    'other': 'Business'
  };

  const displayIndustry = industryMap[industry] || industry;
  item.innerHTML = `<span class="ticker-badge">NEW</span> ${name} — ${business} (${displayIndustry}) — Application Received — <strong>Proposal Queued</strong>`;
  ticker.insertBefore(item, ticker.firstChild);
}

// ===== LIVE TICKER ROTATION =====
const tickerMessages = [
  { badge: 'CLOSED', text: 'Dr. Williams — Cedars-Sinai — AI Voice Agent — <strong>$7,500 setup</strong>' },
  { badge: 'DEMO', text: 'Amanda R. — Keller Williams — AI Appointment Setting — <strong>Demo booked</strong>' },
  { badge: 'HOT', text: 'James T. — High-Ticket Coach — Enterprise AI — <strong>$10K proposal reviewing</strong>' },
  { badge: 'CLOSED', text: 'Patricia M. — eXp Realty — AI Lead Follow-Up — <strong>$497/mo</strong>' },
  { badge: 'DEMO', text: 'Dr. Nguyen — UCLA Health — AI Patient Booking — <strong>Demo confirmed</strong>' },
  { badge: 'CLOSED', text: 'Carlos B. — Mortgage Pro — AI Qualification — <strong>$497/mo</strong>' },
  { badge: 'HOT', text: 'Rachel K. — Insurance Agency — AI Outreach — <strong>Proposal sent</strong>' },
  { badge: 'CLOSED', text: 'Thomas H. — Compass Realty — AI System — <strong>$497/mo</strong>' },
  { badge: 'CLOSED', text: 'Dr. Park — Beverly Hills Medical — AI Voice Agent — <strong>$7,500 setup + $500/mo</strong>' },
  { badge: 'DEMO', text: 'Kevin L. — RE/MAX — AI Appointment Setting — <strong>Demo scheduled</strong>' },
  { badge: 'CLOSED', text: 'Maria S. — Coaching Empire — Enterprise AI — <strong>$9,500 setup + $2K/mo</strong>' },
  { badge: 'HOT', text: 'Dr. Johnson — Kaiser Network — AI Patient Booking — <strong>$15K proposal</strong>' },
];

let tickerIndex = 0;

function rotateTicker() {
  const ticker = document.getElementById('leadsTicker');
  if (!ticker) return;

  const msg = tickerMessages[tickerIndex % tickerMessages.length];
  const item = document.createElement('div');
  item.className = 'ticker-item';
  item.innerHTML = `<span class="ticker-badge">${msg.badge}</span> ${msg.text}`;

  if (ticker.children.length >= 15) {
    ticker.removeChild(ticker.lastChild);
  }

  ticker.insertBefore(item, ticker.firstChild);
  tickerIndex++;
}

setInterval(rotateTicker, 6000);

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

document.querySelectorAll('.service-card, .result-card, .legal-card, .step, .contact-method, .pain-card, .cs-card, .offer-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

const style = document.createElement('style');
style.textContent = `
  .service-card.visible, .result-card.visible, .legal-card.visible, .step.visible, 
  .contact-method.visible, .pain-card.visible, .cs-card.visible, .offer-item.visible {
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

// ===== PAIN STAT COUNTER ANIMATION =====
const painObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const painStats = document.querySelectorAll('.pain-stat');
      painStats.forEach(el => {
        const text = el.textContent;
        if (text === '73%') { el.textContent = '0%'; animateCounter(el, 73, '', '%'); }
        if (text === '4 hrs') { el.textContent = '0'; setTimeout(() => el.textContent = '4 hrs', 1000); }
        if (text === '$15K/mo') { el.textContent = '$0'; animateCounter(el, 15000, '$', ''); setTimeout(() => el.textContent = '$15K/mo', 1200); }
        if (text === '$47K') { el.textContent = '$0'; animateCounter(el, 47000, '$', ''); setTimeout(() => el.textContent = '$47K', 1200); }
      });
      painObserver.disconnect();
    }
  });
}, { threshold: 0.3 });

const painSection = document.querySelector('.pain-grid');
if (painSection) painObserver.observe(painSection);

// ===== FLOATING CTA (Cardone — Always Be Closing) =====
const floatingCTA = document.createElement('div');
floatingCTA.innerHTML = `
  <a href="#leads" style="
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #C9A84C;
    color: #0D1A4A;
    padding: 14px 24px;
    border-radius: 50px;
    font-weight: 800;
    font-size: 14px;
    text-decoration: none;
    box-shadow: 0 8px 30px rgba(201,168,76,0.4);
    z-index: 999;
    display: none;
    transition: all 0.3s;
    font-family: 'Inter', sans-serif;
  " id="floatingBtn">Apply Now — 5 Spots Left</a>
`;
document.body.appendChild(floatingCTA);

window.addEventListener('scroll', () => {
  const btn = document.getElementById('floatingBtn');
  if (window.scrollY > 600) {
    btn.style.display = 'block';
  } else {
    btn.style.display = 'none';
  }
});

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
Frameworks: Martell + Hormozi + Cardone + Brunson + Ovens
CEO: Aaron T. Reddix | 747-301-8586
90-Day Performance Guarantee Active
`, 'color: #C9A84C; font-family: monospace; font-size: 12px;');
