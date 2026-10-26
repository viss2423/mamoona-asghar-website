# Dr. Mamoona Asghar

Academic website for Dr. Mamoona Asghar, School of Computer Science, University of Galway.

## Website

The `dist` folder contains a complete standalone static website. It uses local styles, scripts and images with no website builder, editor overlay, tracking service or external font dependency. Hosting is through GitHub Pages.

## Publications

Current status (26 October 2026): all 110 entries returned across both pages of the verified public Google Scholar profile have been imported. The weekly update workflow is configured with a repository secret and has completed its first successful import and deployment. This is the profile's publication list, which may include preprints or other outputs alongside papers.

The weekly workflow updates the public Scholar author profile lw6LYlgAAAAJ through SerpApi. The author ID comes from her own ORCID researcher links; the university staff directory's older Scholar ID returns 404. To configure this integration again or rotate its API key:

1. Create a free account at https://serpapi.com/users/sign_up . The current free tier lists 250 searches/month; check current terms before subscribing.
2. Open this repository's Settings → Secrets and variables → Actions → New repository secret.
3. Name the secret `SERPAPI_API_KEY` and enter the API key as its value. Never add it to website files or a commit.
4. Open Actions → Publish academic website → Run workflow.
5. Confirm a successful import, paper count and the displayed last-checked date against the Scholar profile. The workflow then runs weekly on Monday at 07:23 UTC, subject to scheduler delays.

It follows all publication pages, preserves Scholar's default citation order and updates titles, author strings, venue, year and citation counts. New papers appear after Scholar indexes them and a successful scheduled deployment runs. The previous publication snapshot is retained in Git; refresh failures stop the deployment and preserve the live website. Matching is a dated snapshot of the public author profile, not an instantaneous guarantee of all papers ever published. Check workflow failures, quota and account state if updates stop. GitHub can disable scheduled runs for inactive repositories.

## Editing and preview

Edit biography, research and projects in `dist/index.html`, styles in `dist/styles.css`. The project list contains four publicly documented projects, not a confirmed complete project inventory. The supervisor should review her biography, photo, logo use and complete project/team details.

Run `python -m http.server 8813 --bind 127.0.0.1 --directory dist`, then open http://127.0.0.1:8813.

## Sources

- https://research.universityofgalway.ie/en/persons/mamoona-asghar/
- https://orcid.org/0000-0001-7460-266X
- https://www.universityofgalway.ie/science-engineering/school-of-computer-science/people/academicstaff/
- https://pay.universityofgalway.ie/people/mamoonaasghar.html
- https://cordis.europa.eu/project/id/101109961/results
- https://vis-malai.cs.universityofgalway.ie/index.php/team/
- https://serpapi.com/google-scholar-author-api
