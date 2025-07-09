// @ts-nocheck
/**
 * @typedef {import('jquery')} jQuery
 */

$(document).ready(function () {
  $(document).on("click", ".recommends-btn", function (e) {
    e.preventDefault();
    // 임의로 가져왔다고 치고 (나중에 수정 必)
    const userId = $(this).data("user-id");

    result = showRecommends(userId);
    if (!result) {
      return;
    }

    userId = result["userId"];
    const { title, url, description } = result["recommends"];

    // 1. 해당 userId profile칸을 비운다 2. 대신 recommends를 추가한다.
    const followerContainer = $("#follower-container");
    followerContainer.empty();
    // 이젠 쭈르륵 html 확인 후 append
  });

  function showRecommends(userId) {
    $.ajax({
      url: `/api/user/${userId}/recommends`,
      method: "get",
      success: function (data) {
        return data;
      },

      error: function (error) {
        alert(`error: ${error}`);
      },
    });
  }
});
