Digital portfolio — files to add (same folder as this README)
================================================================

Required for full credit / working links
----------------------------------------
  headshot.jpg          Professional photo (square or 4:5 crop; shown in hero card; JPG or PNG — if you use PNG, update index.html src to headshot.png)
  video-resume.mp4      Your video resume (H.264 MP4)
  cover-letter.pdf      Application letter (downloadable; linked from site)
  cover-letter-image.jpg   Preview on Cover Letter page (or use cover-letter-image.png — same base name)

Strongly recommended
--------------------
  resume.pdf            Professional resume (regenerate with same command as cover letter)
  sample-essay.pdf      Academic essay or report (linked from Works)
  certificate.jpg         Scan or export of certificate (JPG or PNG — if PNG, change the link in index.html Works item 06 to certificate.png)

Optional
--------
  video-poster.jpg      Still image shown before the video plays (add poster="assets/video-poster.jpg" on the <video> tag if you use this)

LinkedIn (optional)
-------------------
  In index.html, search for LINKEDIN_URL and set your profile URL, or leave empty string '' to hide the LinkedIn button.

After adding files, open index.html in a browser (or run: python3 -m http.server)
and test every link in Works and the Cover Letter PDF button.

Regenerate cover-letter.pdf + resume.pdf after editing scripts/build_pdfs.py:
  python3 scripts/build_pdfs.py
