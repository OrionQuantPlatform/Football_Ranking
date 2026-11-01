# JSON database E2E acceptance

- Enumerate all seasons, competitions, matches, player appearances, shots, supplemental CSV rows and detailed source response families before import.
- Preserve original files under data/sources with hashes; canonical tables live in data/raw and computed outputs in data/computed.
- Player references and match references must resolve; differing names or source IDs must not be silently merged.
- Reassemble every former dashboard partition from table files and compare all values, including nulls and coverage flags.
- Load historical and current seasons through the real dashboard HTTP path and its JavaScript data adapter.
- Reconstruct representative detailed source documents through backend routes; compare against the source archive.
- Build and existing checks must pass. Keep failures and exact reproduction commands in evidence.
- No arbitrary player score or unverified cross-provider identity mapping.
