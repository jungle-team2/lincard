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

  fetch("/api/user/my", {
    method: "put",
    body: JSON.stringify({ data, introduction, name }),
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
