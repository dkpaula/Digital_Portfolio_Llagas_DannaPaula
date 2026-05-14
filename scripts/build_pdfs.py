#!/usr/bin/env python3
"""
Generate assets/cover-letter.pdf and assets/resume.pdf (stdlib only).
Run: python3 scripts/build_pdfs.py
"""
from __future__ import annotations

import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = 612, 792
MARGIN_L = 72
FONT_BODY = 10


def pdf_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", "")
    )


def wrap(text: str, width: int = 92) -> list[str]:
    words = text.replace("\n", " ").split()
    if not words:
        return []
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w]) if cur else w
        if len(trial) <= width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def stream_from_ops(ops: list[tuple[int, str]]) -> bytes:
    """Build PDF text: (font_size, text); empty string = small vertical gap."""
    out: list[str] = ["BT"]
    first = True
    for size, text in ops:
        if text == "":
            if not first:
                out.append("0 -7 Td")
            continue
        out.append(f"/F1 {size} Tf")
        esc = pdf_escape(text)
        if first:
            out.append(f"{MARGIN_L} {PAGE_H - 72:.2f} Td")
            first = False
        else:
            lead = 15 if size >= 12 else 11
            out.append(f"0 {-lead:.2f} Td")
        out.append(f"({esc}) Tj")
    out.append("ET")
    return "\n".join(out).encode("latin-1", errors="replace")


def write_pdf(path: Path, stream: bytes) -> None:
    compressed = zlib.compress(stream)
    stream_obj = (
        b"<< /Length "
        + str(len(compressed)).encode()
        + b" /Filter /FlateDecode >> stream\n"
        + compressed
        + b"\nendstream"
    )
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
            f"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
        ).encode(),
        stream_obj,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    parts = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(sum(len(p) for p in parts))
        parts.append(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")

    xref_start = sum(len(p) for p in parts)
    parts.append(f"xref\n0 {len(objects)+1}\n".encode())
    parts.append(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        parts.append(f"{off:010d} 00000 n \n".encode())
    parts.append(
        f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode()
    )
    path.write_bytes(b"".join(parts))


def cover_letter_ops() -> list[tuple[int, str]]:
    L: list[tuple[int, str]] = [
        (14, "Danna Paula Llagas"),
        (FONT_BODY, "llagasdp@gmail.com  |  09999640117  |  Naga City, Camarines Sur"),
        (FONT_BODY, ""),
        (FONT_BODY, "May 14, 2026"),
        (FONT_BODY, ""),
        (FONT_BODY, "Hiring Manager"),
        (FONT_BODY, "AFC SME Finance, Inc."),
        (FONT_BODY, "Ortigas, Metro Manila"),
        (FONT_BODY, ""),
        (FONT_BODY, "Dear Hiring Manager,"),
        (FONT_BODY, ""),
    ]
    for para in [
        "I am writing to express my sincere interest in the Junior IT Developer position at AFC SME Finance, Inc. As a graduate of Ateneo de Naga University with a Bachelor of Science in Information Technology, I am confident that my technical background and professional mindset make me a strong fit for your team.",
        "The role calls for someone who can develop, test, and maintain internal applications supporting lending, accounting, and business operations, and this aligns directly with my academic training and project experience. I am proficient in JavaScript, Python, HTML, CSS, and SQL, and I have working knowledge of relational databases such as MySQL and PostgreSQL, including basic database design and querying. I also understand RESTful API integration and am comfortable working in Git-based workflows and Linux environments.",
        "Beyond my technical skills, I bring a track record of reliability and professionalism. While completing my degree, I held part-time roles as a Gym Attendant and Barista, where I developed strong communication, teamwork, and time management skills, qualities I will carry directly into a collaborative development team.",
        "I am a fast learner who is genuinely eager to grow alongside a senior development team, and I am open to expanding my knowledge of Docker, Kubernetes, and CRM systems as the role evolves. I believe this position is the right environment for me to contribute meaningfully while continuing to grow as a professional.",
        "I would be grateful for the opportunity to discuss how I can contribute to AFC SME Finance, Inc. Please feel free to reach me at llagasdp@gmail.com or 09999640117 at your convenience. Thank you sincerely for your time and consideration.",
    ]:
        for line in wrap(para):
            L.append((FONT_BODY, line))
        L.append((FONT_BODY, ""))
    L.extend([(FONT_BODY, "Sincerely,"), (FONT_BODY, ""), (12, "Danna Paula Llagas")])
    return L


def resume_ops() -> list[tuple[int, str]]:
    L: list[tuple[int, str]] = [
        (16, "Danna Paula Llagas"),
        (FONT_BODY, "Junior IT Developer  |  BS Information Technology"),
        (FONT_BODY, "llagasdp@gmail.com  |  09999640117  |  Naga City, Camarines Sur"),
        (FONT_BODY, ""),
        (11, "PROFESSIONAL SUMMARY"),
        (FONT_BODY, ""),
    ]
    for line in wrap(
        "Information Technology graduate with strengths in full-stack fundamentals, relational databases, "
        "and collaborative software delivery. Seeking a Junior IT Developer role to build and maintain internal "
        "applications while growing under senior mentorship. Known for clear communication, dependable follow-through, "
        "and a disciplined approach to learning new tools and business domains."
    ):
        L.append((FONT_BODY, line))
    L.extend(
        [
            (FONT_BODY, ""),
            (11, "EDUCATION"),
            (FONT_BODY, ""),
            (FONT_BODY, "Bachelor of Science in Information Technology"),
            (FONT_BODY, "Ateneo de Naga University, Naga City, Philippines"),
            (FONT_BODY, "Graduate"),
            (FONT_BODY, ""),
            (11, "TECHNICAL SKILLS"),
            (FONT_BODY, ""),
        ]
    )
    for line in wrap(
        "Languages and web: JavaScript, Python, HTML, CSS. "
        "Data: SQL, MySQL, PostgreSQL (querying, basic schema design). "
        "Tools and practices: Git, Linux, RESTful API concepts, software engineering coursework."
    ):
        L.append((FONT_BODY, line))
    L.extend(
        [
            (FONT_BODY, ""),
            (11, "EXPERIENCE"),
            (FONT_BODY, ""),
            (FONT_BODY, "Barista (part-time)"),
        ]
    )
    for line in wrap(
        "Customer service, accuracy under pressure, teamwork in a fast-paced retail environment."
    ):
        L.append((FONT_BODY, line))
    L.extend([(FONT_BODY, ""), (FONT_BODY, "Gym Attendant (part-time)")])
    for line in wrap(
        "Professional demeanor, safety awareness, scheduling and clear communication with members."
    ):
        L.append((FONT_BODY, line))
    L.extend([(FONT_BODY, ""), (11, "ACADEMIC AND PROJECT HIGHLIGHTS"), (FONT_BODY, "")])
    for line in wrap(
        "Coursework and projects spanning software engineering, database systems, and web-based applications; "
        "comfortable translating requirements into structured solutions and documenting work for team review."
    ):
        L.append((FONT_BODY, line))
    L.extend([(FONT_BODY, ""), (11, "TARGET ROLE"), (FONT_BODY, "")])
    for line in wrap(
        "Junior IT Developer, AFC SME Finance, Inc. (Ortigas, Metro Manila), full-time. "
        "Motivated to support lending, accounting, and internal operations systems with quality and integrity."
    ):
        L.append((FONT_BODY, line))
    return L


def main() -> None:
    write_pdf(ASSETS / "cover-letter.pdf", stream_from_ops(cover_letter_ops()))
    print(f"Wrote {ASSETS / 'cover-letter.pdf'}")
    write_pdf(ASSETS / "resume.pdf", stream_from_ops(resume_ops()))
    print(f"Wrote {ASSETS / 'resume.pdf'}")


if __name__ == "__main__":
    main()
