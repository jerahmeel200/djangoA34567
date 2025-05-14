const API_BASE = 'http://localhost:8000/api';
let cartId = null;

async function fetchProducts() {
  const res = await fetch(`${API_BASE}/products/`);
  const products = await res.json();
  const container = document.getElementById('products');
  container.innerHTML = '';
  products.forEach(product => {
    const div = document.createElement('div');
    div.innerHTML = `
      <h3>${product.name}</h3>
      <p>${product.description}</p>
      <p><strong>$${product.price}</strong></p>
      <button onclick="addToCart(${product.id})">Add to Cart</button>
    `;
    container.appendChild(div);
  });
}

async function createCart() {
  const res = await fetch(`${API_BASE}/carts/`, { method: 'POST' });
  const data = await res.json();
  cartId = data.cart_id;
  document.getElementById('cart-id').innerText = cartId;
  fetchCart();
}

async function addToCart(productId) {
  if (!cartId) return alert('Please create a cart first!');
  await fetch(`${API_BASE}/carts/${cartId}/add_item/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  });
  fetchCart();
}

async function fetchCart() {
  if (!cartId) return;
  const res = await fetch(`${API_BASE}/carts/${cartId}/`);
  const cart = await res.json();
  const container = document.getElementById('cart');
  container.innerHTML = '';
  cart.items.forEach(item => {
    container.innerHTML += `
      <div>
        ${item.product.name} - ${item.quantity} × $${item.product.price} = $${item.get_total_price}
      </div>
    `;
  });
}

fetchProducts();
