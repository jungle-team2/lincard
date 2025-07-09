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
    const [userId, introduction, data] = requestProfile(userId);
    // 비우기 구현 필요
    // 넘겨주면 html 화면 만들어주시기
  });

  function requestProfile(userId) {
    $.ajax({
      url: `/api/users/${userId}`,
      method: "GET",
      success: function (data) {
        return data;
      },
      error: function (error) {
        alert(`사용자 정보 조회 실패: ${error}`);
      },
    });
  }

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
