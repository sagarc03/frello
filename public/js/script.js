function create_notification(message, className) {
  var notDiv = document.createElement("div");
  notDiv.classList.add("notification");
  notDiv.classList.add(className || "is-info");
  notDiv.textContent = message;
  document.getElementById("notification").appendChild(notDiv);
  setTimeout(() => notDiv.remove(), 10000);
}

document.body.addEventListener("htmx:responseError", (event) => {
  console.log(event);
  create_notification(
    event?.detail?.xhr?.responseText || "Error processing request",
    "is-danger"
  );
  console.log(event);
});

document.body.addEventListener("htmx:sendError", (_) =>
  create_notification("could not connect to the server", "is-danger")
);
