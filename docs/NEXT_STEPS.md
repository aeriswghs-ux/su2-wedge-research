# What to do next

Work through these in order. Finish the explanation and repeatability steps before adding a harder flow case.

## 1. Understand what is already done

Read the student guide and explain the research question aloud in two minutes. Identify the ramp angle, shock angle, and measurement box on the Mach figure.

**Done when:** you can explain why this is verification, why Mach 2 is supersonic, and why it does not prove anything about hypersonic heating.

## 2. Repeat the checks yourself

Use the setup guide. Run the 11 tests and calculate the Mach 2, 10-degree equation answer. Then regenerate the tables from the saved results.

**Keep:** your version list, commands, test output, and a short note comparing your numbers with the release.

**Done when:** you can point to the raw file behind each table entry, not just a screenshot.

## 3. Make one fresh simulation run

Use `scripts.run_study` with a new name. Review the coarse log before trusting the completed run. Check all three final convergence messages and compare the new measurements with the reference.

**Done when:** you have your own logs, fields and comparison table. Explain any differences instead of hiding them.

## 4. Test how the measurement changes

Choose several boxes in advance, away from the wall, shock, ramp tip and outlet. Write down their coordinates before comparing errors. Repeat the pressure, density and Mach averages for every box. Compare the existing 40%, 50%, and 60% shock thresholds. Next, try a shock detector based on the computed pressure gradient.

**Keep:** every result, including worse agreement. Do not choose a box only because it gives the smallest error.

**Done when:** you can say how much the answer depends on the measurement method.

## 5. Test the numerical setup

With a teacher or mentor, change one feature at a time: boundary distance, another mesh refinement, or a slope limiter. Decide what you will compare before running. Keep separate settings and logs for each case.

**Done when:** you know whether the main conclusion survives these changes. Do not claim a formal order of accuracy unless the data and assumptions support it.

## 6. Write the paper in your own words

Use this outline:

1. **Question:** What are you testing, and why is a wedge useful?
2. **Theory:** What do the shock equations predict? What do they assume?
3. **Method:** What geometry, meshes, settings and measurements did you use?
4. **Checks:** Did the solver settle? How did refinement and measurement choices affect results?
5. **Results:** Present the actual tables and figures with units.
6. **Limits:** Explain what the model leaves out and what is still uncertain.
7. **Conclusion:** Answer only the question the evidence supports.
8. **Sources and help:** Cite the sources you read and disclose AI and mentor assistance.

**Done when:** a reader can trace every numerical claim to a saved file and repeat the method.

## 7. Get an independent review

Ask a physics, math, engineering or computer-science teacher to review the equations, measurements and limits. Ask another person to follow the setup guide from a fresh folder.

Record problems as GitHub issues and make a new release after fixing them. Keep v1.0.0 available so earlier claims remain traceable. Choose a presentation or submission venue only after the review; check its current rules and AI-disclosure requirements.
