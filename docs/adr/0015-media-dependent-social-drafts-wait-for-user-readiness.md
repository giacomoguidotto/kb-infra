---
status: accepted
---

# Media-dependent social drafts wait for user readiness

Social Draft Pulse creates approved media-dependent posts as unscheduled drafts. It
schedules them only after the user confirms the required attachment is ready, or
after the user approves replacement copy that works without the attachment.

## Context

[ADR 0010](0010-typefully-schedules-approved-social-drafts.md) lets Social Draft
Pulse schedule approved drafts so routine queue management does not become manual
work. That default is unsafe for a post whose meaning or evidence depends on a photo,
screenshot, or other attachment that only the user can supply. Scheduling such a
draft can publish incomplete copy before the user has added the media.

The approval gate confirms the content direction. It does not prove that a manual
attachment exists or is ready in the social draft queue. Media readiness is therefore
a separate scheduling precondition, not a reason to discard the candidate.

## Decision

- At the idea-summary gate, classify each candidate as media-independent or as
  requiring a specific manual attachment. Optional media does not make otherwise
  complete copy media-dependent.
- After content approval, create both kinds of draft. Schedule media-independent
  drafts normally. Leave media-dependent drafts unscheduled and report the draft link
  or ID plus the exact attachment required in the conversation.
- The user can reply in the same conversation after attaching the media. That reply
  clears the media-readiness precondition. Social Draft Pulse re-reads the live queue
  and schedules the existing draft at its approved time when that slot remains
  eligible and open, otherwise using the next approved, eligible open slot.
- If the user cannot supply the attachment, Social Draft Pulse proposes
  media-independent replacement copy in the conversation. It waits for approval
  before replacing the draft copy and scheduling it.
- Missing-media instructions stay in the conversation, not in public post copy. No
  draft with an outstanding manual attachment is scheduled or published.

## Consequences

- ADR 0010's general scheduling permission is narrowed by a media-readiness
  precondition. Its approval gate and no-immediate-publish boundary still stand.
- Media-dependent ideas can be preserved as useful drafts without risking incomplete
  publication.
- Attachment confirmation does not reopen content approval when the copy is
  unchanged. A media-independent rewrite does because it changes the approved copy.
- `published-social-context` still changes only after a post actually goes live.
