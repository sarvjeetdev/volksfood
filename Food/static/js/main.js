const button = document.querySelector(".navbar__ham");
const menu = document.querySelector(".navbar__links");
const overlay = document.querySelector("#overlay");

button.addEventListener("click", () => {
  console.log("btn clicked!");
  button.classList.toggle("open");
  menu.classList.toggle("navbar__open");
  overlay.classList.toggle("show");
});

overlay.addEventListener("click", () => {
  console.log("btn clicked!");
  overlay.classList.toggle("show");
  button.classList.toggle("open");
  menu.classList.toggle("navbar__open");
});

const btns = document.querySelectorAll("[data-target]");
const close_modals = document.querySelectorAll(".close-modal");
const overlay2 = document.getElementById("overlay2");

btns.forEach((btn) => {
  btn.addEventListener("click", () => {
    console.log("btn clicked!");
    document.querySelector(btn.dataset.target).classList.add("active");
    overlay2.classList.add("active");
    console.log("end");
  });
});

close_modals.forEach((btn) => {
  btn.addEventListener("click", () => {
    console.log("btn clicked!");
    const modal = btn.closest(".modal2");
    modal.classList.remove("active");
    overlay2.classList.remove("active");
  });
});

window.onclick = (event) => {
  if (event.target == overlay2) {
    console.log("btn clicked!");
    const modals = document.querySelectorAll(".modal2");
    modals.forEach((modal) => modal.classList.remove("active"));
    overlay2.classList.remove("active");
  }
};
