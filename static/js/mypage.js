function onSaveMyCard() {
  const cardEdits = document.querySelectorAll("#card-edit");

  const data = [];
  for (const edit of cardEdits) {
    const key = edit.querySelector("#key").value;
    const value = edit.querySelector("#value").value;

    if (key) data.push([key, value]);
  }

  const name = document.querySelector("#name").value;
  const introduction = document.querySelector("#intruduction").value;
  const avatarId =
    document.querySelector("#profile-avatar").dataset["avatarId"];

  fetch("/api/user/my", {
    method: "put",
    body: JSON.stringify({ data, introduction, name, avatarId }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (res.status !== 200) alert("저장 실패");
      else alert("저장 완료");
    })
    .catch(() => alert("저장 실패"));
}

function openAvatarModal() {
  const modal = document.querySelector("#modal");
  modal.classList.remove("hidden");
}

document.addEventListener("click", (e) => {
  const selectable = e.target.closest("#selectable-avatar");

  if (selectable) {
    id = selectable.dataset["id"];
    selectAvatar(id);
  }
});

function selectAvatar(avatarId) {
  const avatar = document.querySelector("#profile-avatar");
  const img = avatar.querySelector("img");

  avatar.dataset["avatarId"] = avatarId;
  img.src = `/static/avatars/${avatarId}.png`;

  closeAvatarModal();
}

function closeAvatarModal() {
  const modal = document.querySelector("#modal");
  modal.classList.add("hidden");
}
