// ============================================================
//  影片連結（由 site_writeback.py 自動回寫，也可以手動改）
//  youtube ：影片 ID 或網址      short  ：直式重點版（Shorts）ID
//  duration：片長 "6:35"          sections：各小節開始秒數（數量＝小節數），null 用 content.js 預估
//  noVoice ：無旁白版 ID          mp4    ：自架 MP4（沒有 YouTube 時才用）
// ============================================================

window.SERIES_PLAYLIST = "https://www.youtube.com/playlist?list=PLe6mAnJTwuNc"; // 系列播放清單網址（公開或不公開後才填）
window.SERIES_TRAILER = "";  // 系列前導片 ID（延續型系列）

window.VIDEO_LINKS = {
  u01: { youtube: "XqcHtghnEuw", mp4: "", duration: "12:39", sections: [0, 13, 52, 126, 275.8, 387.3, 514.3, 636.1], noVoice: "", short: "" },
  u02: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u03: { youtube: "IKvSUgoPnuU", mp4: "", duration: "14:16", sections: [0, 13, 62.9, 167.2, 317.1, 444.6, 561.3, 720.7], noVoice: "", short: "" },
  u04: { youtube: "LW5yZSFCpGM", mp4: "", duration: "13:37", sections: [0, 13, 61.7, 173.6, 317.9, 446.9, 565.1, 689.9], noVoice: "", short: "" },
  u05: { youtube: "cezfuuHQEHc", mp4: "", duration: "13:33", sections: [0, 13, 54.8, 191.3, 316, 444.3, 550.5, 666.2], noVoice: "", short: "" },
  u06: { youtube: "eZGCtY2WPGQ", mp4: "", duration: "13:47", sections: [0, 13, 60.4, 169.3, 308.2, 420.6, 545.5, 690.2], noVoice: "", short: "" },
  u07: { youtube: "rUfkA6BYB-c", mp4: "", duration: "13:52", sections: [0, 13, 57.4, 202, 336.8, 446.6, 555.8, 674.2], noVoice: "", short: "" },
  u08: { youtube: "FcguGyxjsy4", mp4: "", duration: "14:06", sections: [0, 13, 61.9, 172.9, 278.8, 387.8, 532.9, 686.3], noVoice: "", short: "" },
  u09: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u10: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u11: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u12: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u13: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" }
};
