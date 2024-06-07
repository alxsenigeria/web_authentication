const createUser = async function (userData) {
  const response = await fetch("http://127.0.0.1:5000/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  console.log(data);
};

const logUser = async function (userData) {
  const response = await fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  localStorage.setItem("userToken", data.access_token);
};

const getUser = async function (token) {
  const response = await fetch("http://127.0.0.1:5000/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  return data;
};

document.querySelector(".form-1")?.addEventListener("submit", function (e) {
  e.preventDefault();
  const email = document.querySelector(".email").value;
  const firstName = document.querySelector(".first-name").value;
  const lastName = document.querySelector(".last-name").value;
  const password = document.querySelector(".password").value;

  const userData = {
    first_name: firstName,
    last_name: lastName,
    email: email,
    password: password,
  };

  createUser(userData);
  window.location.pathname = "/login.html";
});

document
  .querySelector(".form-2")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();
    const email = document.querySelector(".email").value;
    const password = document.querySelector(".password").value;

    const userData = {
      email: email,
      password: password,
    };

    await logUser(userData);
    window.location.pathname = "/welcome.html";
  });

window.addEventListener("DOMContentLoaded", function () {
  if (this.window.location.pathname === "/welcome.html") {
    const token = this.localStorage.getItem("userToken");
    getUser(token);
  }
});
