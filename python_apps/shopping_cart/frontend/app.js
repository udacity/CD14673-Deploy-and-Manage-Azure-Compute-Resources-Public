const API_BASE_URL = window.shoppingCartAPIBaseURL;

const productsEl = document.getElementById("products");
const cartEl = document.getElementById("cart");
const cartTotalEl = document.getElementById("cart-total");

const formatPrice = (value) => `$${value.toFixed(2)}`;

const request = async (path, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Request failed");
  }

  return response.json();
};

const renderProducts = (products) => {
  productsEl.innerHTML = "";
  products.forEach((product) => {
    const wrapper = document.createElement("div");
    wrapper.className = "product";

    const info = document.createElement("div");
    info.innerHTML = `<strong>${product.name}</strong><div class="muted">${formatPrice(
      product.price
    )}</div>`;

    const action = document.createElement("button");
    action.textContent = "Add to cart";
    action.addEventListener("click", () => addToCart(product));

    wrapper.appendChild(info);
    wrapper.appendChild(action);
    productsEl.appendChild(wrapper);
  });
};

const renderCart = (items) => {
  cartEl.innerHTML = "";

  if (!items.length) {
    cartEl.innerHTML = '<div class="muted">Your cart is empty.</div>';
    cartTotalEl.textContent = "";
    return;
  }

  let total = 0;
  items.forEach((item) => {
    total += item.price * item.quantity;
    const wrapper = document.createElement("div");
    wrapper.className = "cart-item";

    const info = document.createElement("div");
    info.innerHTML = `<strong>${item.name}</strong><div class="muted">Qty: ${item.quantity} · ${formatPrice(
      item.price
    )}</div>`;

    const action = document.createElement("button");
    action.className = "secondary";
    action.textContent = "Remove";
    action.addEventListener("click", () => deleteFromCart(item.itemId));

    wrapper.appendChild(info);
    wrapper.appendChild(action);
    cartEl.appendChild(wrapper);
  });

  cartTotalEl.textContent = `Total: ${formatPrice(total)}`;
};

const loadProducts = async () => {
  const data = await request("/products");
  renderProducts(data.items || []);
};

const loadCart = async () => {
  const data = await request("/cart");
  renderCart(data.items || []);
};

const addToCart = async (product) => {
  await request("/cart", {
    method: "POST",
    body: JSON.stringify({
      itemId: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
    }),
  });
  await loadCart();
};

const deleteFromCart = async (itemId) => {
  await request(`/cart/${itemId}`, { method: "DELETE" });
  await loadCart();
};

const init = async () => {
  try {
    await loadProducts();
    await loadCart();
  } catch (error) {
    cartEl.innerHTML = `<div class="muted">${error.message}</div>`;
  }
};

init();
