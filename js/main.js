// =============================================
// GENIOAI.COM - Main JavaScript
// =============================================

// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 20);
});

// Mobile menu toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (!navbar.contains(e.target)) navLinks.classList.remove('open');
  });
}

// Newsletter form
const newsletterForm = document.getElementById('newsletterForm');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = newsletterForm.querySelector('button');
    btn.textContent = '¡Suscrito! ✓';
    btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    setTimeout(() => {
      btn.textContent = 'Suscribirse';
      btn.style.background = '';
      newsletterForm.reset();
    }, 3000);
  });
}

// Contact form
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = contactForm.querySelector('button');
    btn.textContent = 'Mensaje enviado ✓';
    btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    setTimeout(() => {
      btn.textContent = 'Enviar Mensaje';
      btn.style.background = '';
      contactForm.reset();
    }, 3000);
  });
}

// Animate on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.article-card, .category-card, .featured-card, .tool-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// Reading progress bar (for article pages)
const progressBar = document.getElementById('readingProgress');
if (progressBar) {
  window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    progressBar.style.width = (winScroll / height * 100) + '%';
  });
}

// Copy code blocks
document.querySelectorAll('pre').forEach(pre => {
  const btn = document.createElement('button');
  btn.textContent = 'Copiar';
  btn.style.cssText = 'position:absolute;top:8px;right:8px;padding:4px 10px;background:rgba(124,58,237,0.3);border:none;border-radius:6px;color:white;font-size:0.75rem;cursor:pointer;font-family:inherit;';
  pre.style.position = 'relative';
  pre.appendChild(btn);
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(pre.textContent.replace('Copiar',''));
    btn.textContent = '¡Copiado!';
    setTimeout(() => btn.textContent = 'Copiar', 2000);
  });
});
