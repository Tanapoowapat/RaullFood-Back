// Replace the placeholders with your API endpoint and form inputs
const endpointUrl = "http://localhost:8000/token";
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

// Listen for the form submit event
document.getElementById("login-form").addEventListener("submit", (event) => {
  event.preventDefault(); // prevent default form submission
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();

  // Send an AJAX request to the login endpoint
  fetch(endpointUrl, {
    method: "POST",
    body: new URLSearchParams({
      username: username,
      password: password,
      grant_type: "password",
    }),
    headers: {
      "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid credentials");
      }
      return response.json();
    })
    .then((data) => {
      // Handle successful login
      console.log("Access token:", data.access_token);
      //   localStorage.setItem("access_token", data.access_token); // save token to local storage
      //   window.location.href = "/docs"; // redirect to dashboard page
    })
    .catch((error) => {
      // Handle login error
      console.error("Login error:", error);
      alert("Invalid credentials");
    });
});
