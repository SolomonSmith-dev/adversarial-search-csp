Lyssa — CSPs + Report + Packaging Lead

Files:
	•	Report.pdf
	•	screenshots/ folder
	•	Final ZIP submission

---

Mission

You are responsible for the written and presentation parts of the project.
Your main goals are to:
	1.	Write and format the final report following the instructor’s template.
	2.	Solve and explain the two CSP (Constraint Satisfaction Problem) questions from the assignment.
	3.	Gather everyone’s results, screenshots, and contributions, then package them into the final ZIP file for submission.

You are the final editor and project presenter — the person who makes sure everything looks clean, professional, and complete before we turn it in.

---

What You’re Responsible For

Task	Description
CSP Problems	Solve both CSPs clearly and show constraint graphs.
Report Writing	Combine all sections (intro, AI results, CSPs, contributions, etc.) into one PDF.
Formatting	Use the official homework cover page and match the rubric requirements.
Packaging	Collect all files, tests, and screenshots into one clean .zip file for submission.


---

Part 1 — Constraint Satisfaction Problems (CSPs)

You’ll write out and explain both CSP problems in the report.

⸻

```markdown
Lyssa — CSPs + Report + Packaging Lead

Files:
  - Report.pdf
  - screenshots/ folder
  - Final ZIP submission

---

Mission

You are responsible for the written and presentation parts of the project.
Your main goals are to:
  1. Write and format the final report following the instructor’s template.
  2. Solve and explain the two CSP (Constraint Satisfaction Problem) questions from the assignment.
  3. Gather everyone’s results, screenshots, and contributions, then package them into the final ZIP file for submission.

You are the final editor and project presenter — the person who makes sure everything looks clean, professional, and complete before we turn it in.

---

What You’re Responsible For

Task	Description
CSP Problems	Solve both CSPs clearly and show constraint graphs.
Report Writing	Combine all sections (intro, AI results, CSPs, contributions, etc.) into one PDF.
Formatting	Use the official homework cover page and match the rubric requirements.
Packaging	Collect all files, tests, and screenshots into one clean .zip file for submission.

---

Part 1 — Constraint Satisfaction Problems (CSPs)

You’ll write out and explain both CSP problems in the report.

---

CSP 1: Knights Problem

Problem:
Place k knights on an n×n chessboard so that no two knights attack each other.

What to Include:
  - Variables: One variable for each knight (K₁, K₂, K₃, …).
  - Domain: All possible board cells (row, column).
  - Constraints:
    - No two knights share the same square.
    - No two knights can attack each other (the L-shaped (±1,±2) and (±2,±1) moves are forbidden).
  - Constraint Graph:
    - Draw a node for each knight.
    - Connect edges between every pair that can potentially attack each other.

Short Explanation:
Explain in a few sentences how backtracking or forward-checking would solve this problem (using one knight at a time and skipping invalid placements).

---

CSP 2: Vehicle Scheduling Problem

Problem:
Five vehicles (A, B, C, D, and E) must be scheduled for two stops (CGI and JB Hall) across four time slots {1, 2, 3, 4}.

What to Include:
  - Variables: Each vehicle (A, B, C, D, E).
  - Domain: Pairs of (stop, time) values they can occupy.
  - Constraints:
    - B must arrive in slot 1.
    - D can only operate in slot 3 or 4.
    - A must finish by slot 2.
    - D must arrive before C leaves (order constraint).
    - A, B, and C → only CGI stop.
    - D and E → only JB Hall stop.
    - No two vehicles can occupy the same stop and time at once.
  - Constraint Graph:
    - One node per vehicle.
    - Connect edges wherever two vehicles share a constraint (like timing or stop conflicts).

Short Explanation:
Explain that this can be solved by assigning each vehicle a valid time/stop combination while checking constraints step by step (backtracking or local search).

---

Part 2 — The Final Report

Your report is the official submission document. It will summarize everything the team built and learned.

---

Report Structure

1. Cover Page
Use the exact template provided in the assignment.
Include:
  - Course name
  - Assignment name
  - Submission date
  - Team member names and emails

2. Introduction
Briefly explain what the project was about and what each part (AI, GUI, CSP) accomplished.

3. Algorithms Section
Explain:
  - What Minimax, Alpha-Beta, and Negamax are in simple terms.
  - Why the AI uses recursion and search depth.
  - How the game works on different board sizes.

4. Game Results Section
Include:
  - 3–4 screenshots from Alex’s GUI (gui_start.png, gui_mid.png, gui_end.png).
  - Small notes about what happened in each screenshot.
  - Mention performance: e.g., “On 3×3, the AI always draws. On 4×4 and 5×5, the AI usually wins if depth ≥3.”

5. CSP Section
Include both CSP problem explanations, constraints, and graphs (draw them clearly in Word, Google Drawings, or diagrams.net and export as images).

6. Team Contributions
A small paragraph per person describing what each member did:
  - Solomon: Implemented AI algorithms (Minimax, Alpha-Beta, Negamax).
  - Alex: Built game logic and GUI using pygame.
  - Aparajita: Wrote tests and verified game correctness.
  - Lyssa: Solved CSPs, wrote report, and packaged final submission.

7. Conclusion
Write a short reflection (a few sentences):
  - What worked well.
  - What challenges were faced.
  - What each of you learned about AI and teamwork.

---

Screenshots to Include

You’ll collect these from Alex and Aparajita:
  1. gui_start.png – Empty board at game start.
  2. gui_mid.png – Mid-game screenshot (both AI and human have moves).
  3. gui_end.png – Final result (AI win, human win, or draw).
  4. (Optional) CSP graph diagrams for both problems.

---

Packaging & Submission

Before submission, verify that:
  - The report and all .py files are in the same folder.
  - All screenshots are in a screenshots/ folder.
  - All test files are included in the tests/ folder.
  - The ZIP is named correctly:

Firstname_Lastname_CSUID_HW2.zip

You are the one who will actually zip and submit everything.
Double-check file names and that the report opens properly before uploading.

---

What You Need From the Team

From	What You Need	Why
Solomon	A short summary of each AI algorithm + screenshot of working code	To include in the “AI Algorithms” section
Alex	3–4 screenshots from the GUI + notes on gameplay	To include in “Game Results” section
Aparajita	Test results and any manual testing notes	To show in “Results & Verification” section

Once they give you everything, you’ll assemble it into one clean report.

---

How You’ll Know You’re Done
  - Both CSPs are fully written and illustrated with graphs.
  - The report covers every section listed above and matches the rubric.
  - The ZIP file includes:
    - All .py code
    - The tests folder
    - The screenshots folder
    - The final Report.pdf
  - The report looks clean, organized, and professional.
  - Everyone has reviewed it before submission.

---

Quick Summary for Lyssa

Task	Description
CSPs	Write out both problems clearly with graphs and explanations.
Report	Assemble all code summaries, screenshots, and contributions.
Packaging	Final check that all files are present and properly named.
Submission	Upload the finished ZIP file to Canvas or the class portal.

```
