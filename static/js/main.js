function setFilter(value) {
  document.getElementById("filter-input").value = value;
}

let isSameFilterOn = false;

function toggleSameRecFilter() {
  if (!isLoggedIn || isLoggedIn == "false") {
    window.location.href = "/login"; // 로그인 페이지로 이동
    return;
  }

  isSameFilterOn = !isSameFilterOn;

  const filterBtn = document.getElementById("same-rec-filters");
  if (isSameFilterOn) {
    filterBtn.classList.add("bg-blue-200", "border-blue-400");
    filterBtn.classList.remove("border-gray-300");
  } else {
    filterBtn.classList.add("border-gray-300");
    filterBtn.classList.remove("bg-blue-200", "border-blue-400");
  }

  setFilter(isSameFilterOn ? "same-recommend" : "all");
}
