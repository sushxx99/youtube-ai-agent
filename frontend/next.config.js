/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Ensures environment variables are available
  env: {
    NEXT_PUBLIC_MCP_SERVER_URL: process.env.NEXT_PUBLIC_MCP_SERVER_URL,
    NEXT_PUBLIC_FRONTEND_URL: process.env.NEXT_PUBLIC_FRONTEND_URL,
  },
};

module.exports = nextConfig;
