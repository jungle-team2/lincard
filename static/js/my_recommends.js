const appendBtn = document.getElementById("recommend-add-btn");
const list = document.querySelector("#recommend-list");

list.addEventListener("input", () => {
  const alert = document
    .querySelector("#recommends-container")
    .querySelector("#validation-alert");
  alert.style.opacity = 0;
});

list.addEventListener("click", (e) => {
  if (e.target.classList.contains("rec-del-btn")) {
    const row = e.target.closest("#recommend-row");
    row.remove();
  }
});

const renderBtn = () => {
  const itemsLen = list.querySelectorAll("#recommend-row").length;

  if (itemsLen <= 7) {
    appendBtn.hidden = false;
  } else {
    appendBtn.hidden = true;
  }
};

const addRecItem = () => {
  const template = document.querySelector("#template-recommend-row");
  const row = template.content.cloneNode(true);

  list.append(row);
  renderBtn();
};

document
  .getElementById("recommend-add-btn")
  .addEventListener("click", addRecItem);

document.addEventListener("load", () => {
  renderBtn();
});

function onSave() {
  const list = document.querySelector("#recommend-list");
  const rows = list.querySelectorAll("#recommend-row");

  const newRecommends = [];

  for (const row of rows) {
    newRecommends.push({
      title: row.querySelector("#title").value,
      url: row.querySelector("#url").value,
      description: row.querySelector("#description").value,
    });
  }

  if (newRecommends.some((rec) => !rec.title || !rec.url)) {
    const alert = document
      .querySelector("#recommends-container")
      .querySelector("#validation-alert");
    alert.style.opacity = 1;
    return;
  }

  fetch("/api/user/my/recommends", {
    method: "put",
    body: JSON.stringify(newRecommends),
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
