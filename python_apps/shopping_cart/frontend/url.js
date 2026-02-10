window.shoppingCartAPIBaseURL = "https://p9i0yg66jc.execute-api.us-east-2.amazonaws.com/prod";
document.addEventListener("DOMContentLoaded", () => {
  const apiDocEl = document.getElementById("apiDoc");
  if (apiDocEl) {
    apiDocEl.innerHTML = "API: https://p9i0yg66jc.execute-api.us-east-2.amazonaws.com/prod";
  }
});
