function followUser(uid) {
  if (!isLoggedIn || isLoggedIn == "false") {
    window.location.href = "/login"; // 로그인 페이지로 이동
    return;
  }

  fetch(`/api/user/${uid}/following`, { method: "patch" })
    .then(async (res) => {
      if (!res.ok) {
        // 서버가 400, 403, 500 등 에러 응답을 준 경우
        const errorData = await res.json();
        // alert(errorData.message || "알 수 없는 에러");
        throw new Error(errorData.message || "알 수 없는 에러"); // 원하면 throw도 가능
      } else alert("팔로우 완료");
    })
    .catch((err) => alert(err));
}

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
