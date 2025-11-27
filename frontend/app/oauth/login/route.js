export async function GET() {
  const backend = process.env.NEXT_PUBLIC_MCP_SERVER_URL.replace("/mcp", "");
  return Response.redirect(`${backend}/oauth/login`);
}
