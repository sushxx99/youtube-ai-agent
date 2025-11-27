export async function GET(request) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");

  if (!code) {
    return new Response("Missing 'code' from Google OAuth", { status: 400 });
  }

  // Get backend URL from env variable
  const backend = process.env.NEXT_PUBLIC_MCP_SERVER_URL.replace("/mcp", "");

  // Redirect Google OAuth code → FastAPI backend callback
  return Response.redirect(`${backend}/oauth/callback?code=${code}`);
}
