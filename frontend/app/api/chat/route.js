const MCP_URL = process.env.NEXT_PUBLIC_MCP_SERVER_URL;
const sessions = new Map();

/* ------------------------------------------
   SESSION MEMORY
------------------------------------------ */
function getSession(id) {
  if (!sessions.has(id)) {
    sessions.set(id, { 
      lastResults: null,
      lastQuery: null,
      videos: [],
      pageToken: null
    });
  }
  return sessions.get(id);
}

/* ------------------------------------------
   CALL MCP TOOL - FIXED WITH COOKIE FORWARDING
------------------------------------------ */
async function callMCP(tool, args, request) {
  const authHeader = request.headers.get("authorization") || "";
  const token = authHeader.startsWith("Bearer ") ? authHeader.replace("Bearer ", "") : "";

  const forwardedCookies = request.headers.get("x-forwarded-cookies") || "";
  const regularCookies = request.headers.get("cookie") || "";

  const cookies = forwardedCookies || regularCookies;

  const res = await fetch(`${MCP_URL}/call`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": token ? `Bearer ${token}` : "",
      "Cookie": cookies,
    },
    body: JSON.stringify({
      tool_name: tool,
      arguments: args,
    }),
  });

  return res.json();
}

/* ------------------------------------------
   INTENT DETECTION (unchanged)
------------------------------------------ */
function detectIntent(text) {
  const t = text.toLowerCase().trim();

  if (/^(more|some more|show more|load more|next|next page)$/i.test(t))
    return "more";

  if (/^unlike\b/.test(t) || /remove\s+like/i.test(t) || /take.*like\s*off/i.test(t))
    return "unlike";

  if (/^dislike\b/.test(t) || /thumbs\s*down/i.test(t) || /hate\s+(this|it)/i.test(t) || /give.*dislike/i.test(t))
    return "dislike";

  if (/^like\b/.test(t) || /(^|\s)like\s+[a-z0-9_-]{11}/i.test(t) || /please\s+like/i.test(t) || /pls\s+like/i.test(t) || /can (u|you).*like/i.test(t) || /give.*like/i.test(t) || /hit.*like/i.test(t) || /thumbs\s*up/i.test(t) || /\blove (this|it)\b/i.test(t) || /^[a-z0-9_-]{11}\s+like$/i.test(t))
    return "like";

  if (/^comment\b/.test(t) || /leave (a )?comment/i.test(t) || /post (a )?comment/i.test(t) || /write.*comment/i.test(t) || /add.*comment/i.test(t) || /can (u|you).*comment/i.test(t) || /^[a-z0-9_-]{11}\s+comment/i.test(t))
    return "comment";

  if (/^unsub/.test(t) || /unsubscribe/i.test(t) || /stop following/i.test(t) || /remove subscription/i.test(t))
    return "unsubscribe";

  if (/^subscribe\b/.test(t) || /please\s+subscribe/i.test(t) || /can (u|you).*subscribe/i.test(t) || /follow this channel/i.test(t) || /sub to/i.test(t) || /^[a-z0-9_-]{24}\s+subscribe$/i.test(t))
    return "subscribe";

  if (/trending|popular|viral/i.test(t))
    return "trending";
  
  if (/best .*channels?/i.test(t) || /top .*channels?/i.test(t) || /recommend .*channels?/i.test(t))
    return "top_channels";

  if (/best|top|recommend/i.test(t))
    return "recommend";

  return "search";
}

function cleanQuery(text) {
  return text
    .replace(/(videos?|show|find|search|me|about|on|please|can you)/gi, "")
    .replace(/python\s+programming/gi, "python tutorial")
    .trim();
}

function scoreVideo(v, query) {
  const title = v.snippet?.title?.toLowerCase() || "";
  const views = parseInt(v.statistics?.viewCount || 0);
  const q = query.toLowerCase();
  
  let score = 0;
  if (title.includes(q)) score += 5;
  if (q.includes("python") && !title.includes("pyth network")) {
    if (title.includes("tutorial") || title.includes("course")) score += 10;
    if (title.includes("crypto")) score -= 20;
  }
  if (views > 100000) score += 3;
  if (title.includes("#shorts")) score -= 10;
  
  return score + Math.log(views + 1) * 0.1;
}

function extractVideoId(text) {
  const match = text.match(/[a-zA-Z0-9_-]{11}/);
  return match ? match[0] : null;
}

function extractChannelId(text) {
  const match = text.match(/UC[a-zA-Z0-9_-]{22}/);
  return match ? match[0] : null;
}

/* ------------------------------------------
   MAIN POST HANDLER - FIXED TO PASS REQUEST
------------------------------------------ */
export async function POST(req) {
  try {
    const { message, session_id = "default" } = await req.json();
    const session = getSession(session_id);
    const intent = detectIntent(message);

    /* ------------------------------------------
       MORE / PAGINATION
    ------------------------------------------ */
    if (intent === "more") {
      if (!session.lastQuery) {
        return Response.json({
          reply: "❌ No previous search found. Try searching first!",
          type: "text"
        });
      }

      const result = await callMCP("search_videos", { 
        query: session.lastQuery,
        max_results: 10,
        page_token: session.pageToken
      }, req);  // 🔥 PASS REQUEST

      if (result.success && result.data?.items) {
        const items = result.data.items
          .map(v => ({ video: v, score: scoreVideo(v, session.lastQuery) }))
          .sort((a, b) => b.score - a.score)
          .map(x => x.video);

        session.pageToken = result.data.nextPageToken || null;
        session.videos.push(...items.map(v => v.id?.videoId || v.id));

        return Response.json({
          reply: `🎬 Showing more videos for "${session.lastQuery}"!`,
          data: { data: { items } },
          type: "tool_result"
        });
      }
    }

    /* ------------------------------------------
       LIKE VIDEO - FIXED
    ------------------------------------------ */
    if (intent === "like") {
      let videoId = extractVideoId(message) || session.videos[0];

      if (!videoId) {
        return Response.json({
          reply: "❌ Provide a video ID like: 'like video K5KVEU3a'",
          type: "text"
        });
      }

      const result = await callMCP("like_video", { video_id: videoId }, req);  // 🔥 PASS REQUEST
      
      if (result.success) {
        return Response.json({
          reply: `✅ Liked video ${videoId}!`,
          type: "action"
        });
      }

      return Response.json({
        reply: `❌ Failed: ${result.error || "Unknown error"}`,
        type: "error"
      });
    }

    /* ------------------------------------------
       UNLIKE
    ------------------------------------------ */
    if (intent === "unlike") {
      const videoId = extractVideoId(message) || session.videos[0];
      if (!videoId) {
        return Response.json({ reply: "❌ Specify a video ID", type: "text" });
      }

      const result = await callMCP("unlike_video", { video_id: videoId }, req);  // 🔥 PASS REQUEST

      return Response.json({
        reply: result.success 
          ? `✅ Removed like from ${videoId}!`
          : `❌ Failed to unlike`,
        type: result.success ? "action" : "error"
      });
    }

    /* ------------------------------------------
       DISLIKE VIDEO
    ------------------------------------------ */
    if (intent === "dislike") {
      const videoId = extractVideoId(message) || session.videos[0];

      if (!videoId) {
        return Response.json({
          reply: "❌ Provide a video ID like: 'dislike <video_id>'",
          type: "text",
        });
      }

      const result = await callMCP("dislike_video", { video_id: videoId }, req);  // 🔥 PASS REQUEST

      return Response.json({
        reply: result.success
          ? `👎 Disliked video ${videoId}!`
          : `❌ Failed to dislike`,
        type: result.success ? "action" : "error",
      });
    }

    /* ------------------------------------------
       COMMENT
    ------------------------------------------ */
    if (intent === "comment") {
      const videoId = extractVideoId(message) || session.videos[0];

      if (!videoId) {
        return Response.json({
          reply: "❌ I couldn't find any video ID. Try: comment on <video_id> \"your comment\"",
          type: "text"
        });
      }

      let match = message.match(/["'](.+?)["']/);
      let commentText = match ? match[1] : null;

      if (!commentText) {
        const after = message.split(/comment|reply/i)[1];
        if (after) {
          commentText = after.replace(/on\s+[a-zA-Z0-9_-]{11}/, "").trim();
        }
      }

      if (!commentText) {
        return Response.json({
          reply: "❌ Please include a comment text. Example: comment on <video_id> \"nice video\"",
          type: "text"
        });
      }

      const result = await callMCP("comment_on_video", {
        video_id: videoId,
        text: commentText
      }, req);  // 🔥 PASS REQUEST

      if (!result.success) {
        return Response.json({
          reply: `❌ Failed to comment: ${result.error || "Unknown error"}`,
          type: "error"
        });
      }

      return Response.json({
        reply: `✅ Comment posted on ${videoId}!`,
        type: "action"
      });
    }

    /* ------------------------------------------
       SUBSCRIBE
    ------------------------------------------ */
    if (intent === "subscribe") {
      let channelId = extractChannelId(message);
      const handleMatch = message.match(/@[\w\d_]+/);

      if (!channelId && handleMatch) {
        const handle = handleMatch[0];
        const search = await callMCP("search_channels", { query: handle, max_results: 1 }, req);  // 🔥 PASS REQUEST

        if (search.success && search.data?.items?.length) {
          channelId = search.data.items[0].id.channelId;
        }
      }

      if (!channelId && !handleMatch) {
        const search = await callMCP("search_channels", { query: message, max_results: 1 }, req);  // 🔥 PASS REQUEST

        if (search.success && search.data?.items?.length) {
          channelId = search.data.items[0].id.channelId;
        }
      }

      if (!channelId) {
        return Response.json({
          reply: "❌ Could not identify the channel. Try using @handle or channel ID.",
          type: "text"
        });
      }

      const result = await callMCP("subscribe_channel", { channel_id: channelId }, req);  // 🔥 PASS REQUEST

      return Response.json({
        reply: result.success
          ? `✅ Subscribed to ${channelId}!`
          : `❌ Failed to subscribe.`,
        type: result.success ? "action" : "error"
      });
    }

    /* ------------------------------------------
       UNSUBSCRIBE
    ------------------------------------------ */
    if (intent === "unsubscribe") {
      const channelId = extractChannelId(message);

      if (!channelId) {
        return Response.json({
          reply: "❌ Provide a channel ID (starts with UC...)",
          type: "text"
        });
      }

      const subs = await callMCP("my_subscriptions", {}, req);  // 🔥 PASS REQUEST

      if (!subs.success || !subs.data?.items) {
        return Response.json({
          reply: "❌ Could not fetch subscriptions.",
          type: "error"
        });
      }

      const subItem = subs.data.items.find(
        (s) => s.snippet?.resourceId?.channelId === channelId
      );

      if (!subItem) {
        return Response.json({
          reply: `ℹ️ You are not subscribed to ${channelId}.`,
          type: "text"
        });
      }

      const subscriptionId = subItem.id;

      const result = await callMCP("unsubscribe_channel", { subscription_id: subscriptionId }, req);  // 🔥 PASS REQUEST

      return Response.json({
        reply: result.success
          ? `✅ Unsubscribed from ${channelId}!`
          : `❌ Failed to unsubscribe.`,
        type: result.success ? "action" : "error"
      });
    }

    /* ------------------------------------------
       TRENDING
    ------------------------------------------ */
    if (intent === "trending") {
      const result = await callMCP("trending_videos", { max_results: 12 }, req);  // 🔥 PASS REQUEST

      if (result.success) {
        session.videos = result.data.items.map(v => v.id);
        session.lastQuery = "trending";

        return Response.json({
          reply: "🔥 Trending videos!",
          data: result,
          type: "tool_result"
        });
      }
    }

    /* ------------------------------------------
       BEST / TOP CHANNELS
    ------------------------------------------ */
    if (intent === "top_channels") {
      const cleaned = message
        .replace(/best|top|recommend/gi, "")
        .replace(/channels?/gi, "")
        .trim() || "technology";

      const result = await callMCP("search_channels", {
        query: cleaned,
        max_results: 10
      }, req);  // 🔥 PASS REQUEST

      if (!result.success || !result.data?.items?.length) {
        return Response.json({
          reply: `❌ No channels found for "${cleaned}".`,
          type: "text"
        });
      }

      return Response.json({
        reply: `⭐ Top channels for "${cleaned}":`,
        data: result,
        type: "tool_result"
      });
    }

    /* ------------------------------------------
       RECOMMEND
    ------------------------------------------ */
    if (intent === "recommend") {
      if (!session.lastResults?.data?.items?.length) {
        return Response.json({
          reply: "Search for videos first!",
          type: "text"
        });
      }

      const ranked = session.lastResults.data.items
        .map(v => ({ video: v, score: scoreVideo(v, session.lastQuery) }))
        .sort((a, b) => b.score - a.score);

      const best = ranked[0].video;
      session.videos = [best.id?.videoId || best.id];

      return Response.json({
        reply: `⭐ Best video for "${session.lastQuery}"!`,
        data: { data: { items: [best] } },
        type: "tool_result"
      });
    }

    /* ------------------------------------------
       DEFAULT: SEARCH
    ------------------------------------------ */
    let query = cleanQuery(message) || message;

    const result = await callMCP("search_videos", {
      query,
      max_results: 10,
      order: "relevance"
    }, req);  // 🔥 PASS REQUEST

    if (result.success && result.data?.items) {
      const items = result.data.items
        .map(v => ({ video: v, score: scoreVideo(v, query) }))
        .sort((a, b) => b.score - a.score)
        .map(x => x.video);

      session.lastResults = { data: { items } };
      session.lastQuery = query;
      session.videos = items.map(v => v.id?.videoId || v.id);
      session.pageToken = result.data.nextPageToken || null;

      return Response.json({
        reply: `🎬 Found ${items.length} videos about "${query}"! ${
          session.pageToken ? "Say 'more' for next page." : ""
        }`,
        data: { data: { items } },
        type: "tool_result"
      });
    }

    return Response.json({
      reply: "⚠ No results found.",
      type: "text"
    });

  } catch (err) {
    console.error("Error:", err);
    return Response.json({ reply: "⚠ Error occurred", type: "error" }, { status: 500 });
  }
}