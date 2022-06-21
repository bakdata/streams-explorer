import { NextRequest, NextResponse } from "next/server";

export default function middleware(req: NextRequest) {
  const { pathname, protocol } = req.nextUrl;

  if (pathname.startsWith("/api")) {
    return NextResponse.rewrite(`${protocol}//localhost:8000${pathname}`);
  }

  return NextResponse.next();
}
