(function(){
  const key='rm_padang_cart_v1';
  const cart=JSON.parse(localStorage.getItem(key)||'{}');
  const items={};
  document.querySelectorAll('.pcard').forEach(card=>{items[card.dataset.menuId]={id:card.dataset.menuId,name:card.querySelector('h3').textContent.trim(),price:Number(card.querySelector('.price').textContent.replace(/[^0-9]/g,''))}});
  const format=n=>'Rp'+Number(n).toLocaleString('id-ID');
  const save=()=>localStorage.setItem(key,JSON.stringify(cart));
  const total=()=>Object.entries(cart).reduce((sum,[id,qty])=>sum+(items[id]?.price||0)*qty,0);
  const count=()=>Object.values(cart).reduce((sum,qty)=>sum+qty,0);
  function render(){
    document.querySelectorAll('[data-cart-qty]').forEach(output=>output.textContent=cart[output.dataset.cartQty]||0);
    document.querySelectorAll('.cart-count').forEach(node=>node.textContent=count());
    document.querySelectorAll('.cart-total strong').forEach(node=>node.textContent=format(total()));
    document.querySelectorAll('.cart-lines').forEach(lines=>{lines.innerHTML='';Object.entries(cart).forEach(([id,qty])=>{if(!items[id]||qty<1)return;const line=document.createElement('div');line.className='cart-line';line.innerHTML=`<span>${items[id].name} × ${qty}</span><b>${format(items[id].price*qty)}</b>`;lines.appendChild(line)})});
    save();
  }
  function change(id,delta){cart[id]=Math.max(0,Math.min(99,(cart[id]||0)+delta));if(!cart[id])delete cart[id];render()}
  document.addEventListener('click',event=>{
    const inc=event.target.closest('[data-cart-inc]');if(inc){change(inc.dataset.cartInc,1);return}
    const dec=event.target.closest('[data-cart-dec]');if(dec){change(dec.dataset.cartDec,-1);return}
    const item=event.target.closest('[data-cart-item]');if(item){if(!cart[item.dataset.cartItem])change(item.dataset.cartItem,1);open();return}
    if(event.target.closest('.fab,[href$="#cart"]')&&document.querySelector('.cart-panel')){event.preventDefault();open()}
    if(event.target.closest('.cart-close'))close();
    if(event.target.closest('.cart-clear')){Object.keys(cart).forEach(id=>delete cart[id]);render()}
    if(event.target.closest('.cart-order')){
      if(!count())return;
      const lines=Object.entries(cart).filter(([id,qty])=>items[id]&&qty).map(([id,qty],index)=>`${index+1}. ${items[id].name} x ${qty}`).join('\n');
      const name=document.querySelector('.logo')?.textContent.trim()||'RM Padang Bateh Kota';
      window.open(`https://wa.me/${document.body.dataset.waNumber}?text=${encodeURIComponent(`${name}\n\nOrder:\n${lines}\n\nTotal:\n${format(total())}\n\nMakan di tempat / bungkus / diantar?`)}`,'_blank','noopener');
    }
  });
  function open(){document.querySelectorAll('.cart-panel').forEach(panel=>panel.hidden=false);render()}
  function close(){document.querySelectorAll('.cart-panel').forEach(panel=>panel.hidden=true)}
  render();
})();
