export default function VideoCard({ item }) {
  const videoId = item.id?.videoId || item.id;
  const snippet = item.snippet || {};
  const stats = item.statistics || {};

  const thumbnail =
    snippet.thumbnails?.high?.url || snippet.thumbnails?.medium?.url;

  const title = snippet.title;
  const channel = snippet.channelTitle;

  const views = stats.viewCount
    ? parseInt(stats.viewCount) > 1000000
      ? `${(parseInt(stats.viewCount) / 1000000).toFixed(1)}M views`
      : `${(parseInt(stats.viewCount) / 1000).toFixed(0)}K views`
    : "";

  // ⭐ Detect channel vs video
  const isChannel = videoId?.startsWith("UC");

  // ⭐ Correct URL based on type
  const url = isChannel
    ? `https://www.youtube.com/channel/${videoId}`
    : `https://www.youtube.com/watch?v=${videoId}`;

  return (
    <div
      style={{
        background: "rgba(255,255,255,0.03)",
        borderRadius: "12px",
        overflow: "hidden",
        border: "1px solid rgba(255,255,255,0.08)",
        transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-8px)";
        e.currentTarget.style.background = "rgba(255,255,255,0.06)";
        e.currentTarget.style.borderColor = "rgba(255,255,255,0.15)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.background = "rgba(255,255,255,0.03)";
        e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)";
      }}
      onClick={() => window.open(url, "_blank")}
    >
      <div style={{ position: "relative" }}>
        <img
          src={thumbnail}
          alt={title}
          style={{
            width: "100%",
            height: "180px",
            objectFit: "cover",
          }}
        />

        {/* ⭐ Only show badge when it's a video */}
        {!isChannel && (
          <div
            style={{
              position: "absolute",
              bottom: "8px",
              right: "8px",
              background: "rgba(0,0,0,0.9)",
              padding: "4px 8px",
              borderRadius: "4px",
              fontSize: "12px",
              fontWeight: "600",
              color: "white",
            }}
          >
            {videoId.substring(0, 8)}
          </div>
        )}
      </div>

      <div style={{ padding: "16px" }}>
        <h3
          style={{
            fontSize: "15px",
            fontWeight: "600",
            margin: "0 0 12px 0",
            color: "white",
            lineHeight: "1.4",
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
          }}
        >
          {title}
        </h3>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            fontSize: "13px",
          }}
        >
          <span
            style={{
              color: "rgba(255,255,255,0.6)",
              fontWeight: "500",
            }}
          >
            {channel}
          </span>

          {/* Only show views for videos */}
          {!isChannel && views && (
            <span
              style={{
                color: "rgba(255,255,255,0.4)",
                fontSize: "12px",
              }}
            >
              {views}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
