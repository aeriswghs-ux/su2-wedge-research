# Where the files came from

## Starting material

The original research brief and an extracted folder named `su2-wedge-verification` were available on the connected Windows computer. The named starter ZIP, `SU2_Wedge_Research_Starter_2026-11-26.zip`, was not found. `archive/starter` is a recovered copy of the extracted project, not proof of the original ZIP's exact contents.

The starter includes old `NOT EXECUTED` labels. Those are correct for its stage. Read the current README and results for the completed runs.

## Verified results

The earlier work produced `SU2_Wedge_Verified_Results_2026-11-26.zip`. Before preparing this release, the final coarse, medium and fine VTU flow files in that ZIP were compared by SHA-256 with the files being published. All three matched. The hashes are in `source_archive_check.json`.

The release combines that evidence with updated documentation and safer commands for new runs. It does not bundle the 1.5 GB ParaView download or SU2 executables. Download those separately from the official sources in the setup guide.

## Public-copy changes

- Removed Python caches and temporary files.
- Replaced private machine paths in text with `[WORKSPACE]`, `[DOWNLOADS]`, or `[USER]`.
- Moved old placeholder tables out of the current results view; the recovered starter keeps its historical material.
- Added simple-English guides, package versions, a separate-run command, and release checksums.
- Kept numerical solver data, earlier attempts, and the measurement limitations.

Some original hash lists describe files before these documentation and privacy edits. Use `MANIFEST.sha256` in each release ZIP to verify that ZIP's contents. The exact original ZIP was not reuploaded because its public copy now uses these path substitutions.

## Dates and assistance

The verified run date is November 26, 2026 in America/Chicago. A GitHub upload timestamp records publication, which is a separate event.

This is AI- and computer-assisted numerical verification. The published record supports the stated numerical checks through actual solver output, automated tests and analytical comparisons. Independent reproduction and technical review remain open. Personal learning exercises are optional educational material, not conditions for the recorded verification results.
