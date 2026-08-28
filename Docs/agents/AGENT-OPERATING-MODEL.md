# Agent Operating Model

One agent owns one bounded task and one repository by default.
A cross-repository coordinator owns interface sequencing, not every implementation file.

Required sequence:

1. Read root and repository instructions.
2. Select one task identifier.
3. Declare owned files and interfaces.
4. Inspect Git status.
5. Implement and test one complete slice.
6. Report file manifest, commands, results, and risks.

Agents must not treat another agent's status statement as completion evidence.
