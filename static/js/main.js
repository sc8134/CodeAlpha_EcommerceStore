document.addEventListener('DOMContentLoaded', function() {

  // AJAX add to cart (only on product listing cards, not detail page)
  var cartForms = document.querySelectorAll('.add-to-cart-form');

  cartForms.forEach(function(form) {
    form.addEventListener('submit', async function(e) {
      // if it's inside a product card use ajax, otherwise let it submit normally
      if (!form.closest('.product-card')) return;

      e.preventDefault();

      var btn = form.querySelector('button[type="submit"]');
      var originalText = btn.innerHTML;

      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Adding...';

      try {
        var fd = new FormData(form);
        var res = await fetch(form.action, {
          method: 'POST',
          body: fd,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (res.ok) {
          var data = await res.json();
          updateCartBadge(data.cart_count);

          btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Added!';
          btn.classList.remove('btn-dark');
          btn.classList.add('btn-success');

          setTimeout(function() {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-dark');
            btn.disabled = false;
          }, 1600);

        } else {
          throw new Error('server error');
        }

      } catch(err) {
        // fallback to regular form submit if fetch fails
        btn.innerHTML = originalText;
        btn.disabled = false;
        form.submit();
      }
    });
  });


  // update the cart icon badge number
  function updateCartBadge(count) {
    var badge = document.getElementById('cart-badge');

    if (count > 0) {
      if (!badge) {
        badge = document.createElement('span');
        badge.id = 'cart-badge';
        badge.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning text-dark';

        var cartLink = document.querySelector('.nav-link .bi-cart3');
        if (cartLink) {
          cartLink.parentElement.appendChild(badge);
        }
      }
      badge.textContent = count;
      badge.classList.add('badge-pop');
      badge.addEventListener('animationend', function() {
        badge.classList.remove('badge-pop');
      }, { once: true });

    } else {
      if (badge) badge.remove();
    }
  }


  // auto close alert messages after a few seconds
  var alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach(function(el) {
    setTimeout(function() {
      var instance = bootstrap.Alert.getOrCreateInstance(el);
      if (instance) instance.close();
    }, 4000);
  });


  // smooth scroll when clicking "Shop Now" hero button
  var heroCta = document.querySelector('a[href="#products"]');
  if (heroCta) {
    heroCta.addEventListener('click', function(e) {
      e.preventDefault();
      var target = document.getElementById('products');
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  }

});
