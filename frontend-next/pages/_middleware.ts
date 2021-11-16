import { NextRequest, NextResponse } from "next/server";

export default function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  if (pathname.startsWith("/api")) {
    return NextResponse.rewrite(`http://localhost:8000${pathname}`);
  }
}
