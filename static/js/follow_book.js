// 타입스크립트 문법 무시
// @ts-nocheck
/* global jQuery */

$(document).ready(function () {
  $(document).on("click", ".show-recommends-btn", function (e) {
    e.preventDefault();
    const userId = $(this).data("user-id");
    result = requestRecommends(userId);
    if (!result) {
      return;
    }

    userId = result["userId"];
    recommneds = result["recommneds"];
    // 비우기 구현 필요 ex. $(this).empty();
    for (const rec in recommneds) {
      const [title, url, description] = rec;
      // 이제 넘겨주기
    }
  });

  $(document).on("click", ".show-profile-btn", function (e) {
    e.preventDefault();
    const userId = $(this).data("user-id");
    result = requestProfile(userId);
    const introduction = result["introduction"];
    const data = result["data"];
    // 비우기 구현 필요
  });

  function requestRecommends(userId) {
    $.ajax({
      url: `/api/users/${userId}/recommends`,
      method: "GET",
      success: function (data) {
        return data;
      },
      error: function (error) {
        alert(`추천 목록 조회 실패: ${error}`);
      },
    });
  }
});
