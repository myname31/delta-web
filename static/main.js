document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('btn-run');
  const input = document.getElementById('input-url');
  const result = document.getElementById('result');

  btn.addEventListener('click', async ()=>{
    const url = input.value.trim();
    if(!url){ alert('Masukkan URL'); return; }
    result.classList.remove('hidden');
    result.textContent = "Memproses...";

    try {
      const r = await fetch('/api/delta', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({url})
      });
      const data = await r.json();
      result.textContent = JSON.stringify(data, null, 2);
    } catch (e){
      result.textContent = "Error: " + e.toString();
    }
  });
});
