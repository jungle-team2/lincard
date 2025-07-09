function onSave() {
  const cardEdits = document.querySelectorAll("#card-edit");

  const data = [];
  for (const edit of cardEdits) {
    const key = edit.querySelector("#key").value;
    const value = edit.querySelector("#value").value;

    if (key) data.push([key, value]);
  }

  const introduction = document.querySelector("#intruduction").value;

  fetch("/api/user/my", {
    method: "put",
    body: JSON.stringify({ data, introduction }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(() => alert("저장 완료"))
    .catch(() => alert("저장 실패"));
}
