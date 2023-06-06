import { NextRequest, NextResponse } from "next/server";

export default function middleware(req: NextRequest) {
  const nextUrl = req.nextUrl;

  if (nextUrl.pathname.startsWith("/api")) {
    nextUrl.host = "localhost";
    nextUrl.port = "8000";
    return NextResponse.rewrite(nextUrl);
  }

  return NextResponse.next();
}
