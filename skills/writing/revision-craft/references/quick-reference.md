# Revision Craft — Quick Reference


## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Edit this," "make this better," "tighten this up" | `prose-editor` | General editing — the editor determines the appropriate pass |
| "What's the style of this text?" "Analyze this writing" | `style-analyzer` | Style characterization and measurement |
| "This is too long," "cut this down" | `prose-editor` (line pass) | Tightening is a line-editing operation |
| "Does this flow?" "Is the structure right?" | `prose-editor` (structural pass) | Structural assessment |
| "How does this author write?" "What makes this prose distinctive?" | `style-analyzer` | Author style analysis |
| "Make this sound more like McCarthy" "Push toward VanderMeer" "Surprise me with a mutation" | `style-mutator` | Voice transformation — shifts existing prose along style-DNA axes without changing content |

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Style-analyzer says "this prose is deliberately ornate" but prose-editor wants to cut | Style-analyzer wins | Understand intent before editing. Ornate prose that serves its voice should not be simplified. |
| Structural pass says "cut this scene" but the writer is attached | Present the case, let the writer decide | Killing darlings is the writer's job, not the editor's. |
| Line pass and copy pass disagree on a stylistic choice (fragment, comma splice) | Line pass wins | Intentional style choices override mechanical rules. |
