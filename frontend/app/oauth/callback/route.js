export async function GET(request) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");

  // If missing ?code= — show meaningful error
  if (!code) {
    return new Response("Missing 'code' from Google OAuth", { status: 400 });
  }

  // Forward authorization code to FastAPI backend OAuth handler
  return Response.redirect(
    `http://localhost:8000/oauth/callback?code=${code}`
  );
}
