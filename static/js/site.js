(function(){
  const body=document.body;
  const number=body.dataset.waNumber;
  const shopee=body.dataset.shopeeUrl;
  const wa=text=>`https://wa.me/${number}?text=${encodeURIComponent(text)}`;
  document.querySelectorAll('[data-wa]').forEach(a=>{a.href=wa(a.dataset.wa)});
  document.querySelectorAll('[data-shopee]').forEach(a=>{a.href=shopee});

  const lightbox=document.querySelector('[data-lightbox]');
  const lightboxVisual=lightbox?.querySelector('[data-lightbox-visual]');
  const lightboxCaption=lightbox?.querySelector('[data-lightbox-caption]');
  const closeLightbox=()=>{if(!lightbox)return;lightbox.hidden=true;lightboxVisual.replaceChildren();document.body.classList.remove('lightbox-open')};
  const openLightbox=trigger=>{
    if(!lightbox||!lightboxVisual)return;
    if(trigger.dataset.lightboxSrc){const image=document.createElement('img');image.src=trigger.dataset.lightboxSrc;image.alt=trigger.dataset.lightboxAlt||'';lightboxVisual.appendChild(image)}
    else if(trigger.dataset.lightboxInline){const content=trigger.querySelector('svg')?.cloneNode(true);if(content)lightboxVisual.appendChild(content)}
    lightboxCaption.textContent=trigger.dataset.lightboxAlt||'';lightbox.hidden=false;document.body.classList.add('lightbox-open');lightbox.querySelector('.lightbox-close')?.focus()
  };
  document.addEventListener('click',event=>{const trigger=event.target.closest('[data-lightbox-src],[data-lightbox-inline]');if(trigger){event.preventDefault();openLightbox(trigger)}if(event.target.closest('[data-lightbox-close]'))closeLightbox()});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!lightbox?.hidden)closeLightbox()});

  const nav=document.querySelector('.site-nav');
  const navToggle=document.querySelector('.nav-toggle');
  const navLinks=[...document.querySelectorAll('.nav-link')];
  const homePath=new URL(document.querySelector('.logo')?.href||'/',window.location.href).pathname;
  const setActive=key=>navLinks.forEach(link=>link.classList.toggle('is-active',link.dataset.navKey===key));
  const closeNav=()=>{if(!navToggle)return;navToggle.setAttribute('aria-expanded','false');nav?.classList.remove('nav-open')};
  if(navToggle){
    navToggle.addEventListener('click',()=>{const expanded=navToggle.getAttribute('aria-expanded')==='true';navToggle.setAttribute('aria-expanded',String(!expanded));nav?.classList.toggle('nav-open',!expanded)});
    navLinks.forEach(link=>link.addEventListener('click',()=>{setActive(link.dataset.navKey);closeNav()}));
    document.addEventListener('click',event=>{if(nav?.classList.contains('nav-open')&&!nav.contains(event.target))closeNav()});
    document.addEventListener('keydown',event=>{if(event.key==='Escape')closeNav()});
  }

  if(window.location.pathname===homePath){
    const sections=[...document.querySelectorAll('[data-nav-section],#tentang,#menu,#lokasi')];
    const hero=document.querySelector('.hero');
    if(hero)hero.dataset.navSection='hero';
    const updateSection=entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
      if(visible){
        const sectionKey={hero:'home',tentang:'about',menu:'menu',lokasi:'location'}[visible.target.dataset.navSection||visible.target.id]||'home';
        setActive(sectionKey);
      }
    };
    if('IntersectionObserver' in window){
      const observer=new IntersectionObserver(updateSection,{rootMargin:'-30% 0px -55% 0px',threshold:[0,.2,.5,1]});
      sections.forEach(section=>{section.dataset.navSection=section.dataset.navSection||section.id;observer.observe(section)});
    }else setActive(window.location.hash==='#menu'?'menu':window.location.hash==='#tentang'?'about':'home');
    if(window.location.hash==='#tentang')setActive('about');
    if(window.location.hash==='#menu')setActive('menu');
  }else{
    const path=window.location.pathname;
    const page=path.startsWith('/menu/')?navLinks.find(link=>link.dataset.navKey==='menu'):navLinks.find(link=>link.dataset.page&&path.startsWith(new URL(link.href,window.location.href).pathname));
    setActive(page?.dataset.navKey||'home');
  }

  function filterTabs(tabs, category, updateUrl){
    const grid=document.getElementById(tabs.dataset.targetGrid);
    if(!grid)return;
    tabs.querySelectorAll('.tab').forEach(item=>item.setAttribute('aria-pressed',String(item.dataset.category===category)));
    grid.querySelectorAll('.pcard').forEach(card=>{card.hidden=category!=='all'&&card.dataset.category!==category});
    if(updateUrl&&window.history.replaceState){
      const url=new URL(window.location.href);
      if(category==='all')url.searchParams.delete('kategori');
      else url.searchParams.set('kategori',category);
      window.history.replaceState({},'',url);
    }
  }

  document.querySelectorAll('[data-menu-tabs]').forEach(tabs=>{
    const initial=new URLSearchParams(window.location.search).get('kategori')||'all';
    const valid=tabs.querySelector(`[data-category="${CSS.escape(initial)}"]`);
    filterTabs(tabs,valid?initial:'all',false);
    tabs.addEventListener('click',event=>{
      const button=event.target.closest('.tab[data-category]');
      if(button)filterTabs(tabs,button.dataset.category,true);
    });
  });
})();
