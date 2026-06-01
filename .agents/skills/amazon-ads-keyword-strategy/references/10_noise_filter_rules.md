# Noise Filter Rules

Evidence base: full extraction produced 1413 `irrelevant_noise` records and 217 weak `comment_signal` records. Noise must remain out of the rule library. Comments can support diagnosis only when they contain usable conditions, data, or reasoning, and they should not exceed medium confidence by default.

## Content That Must Not Enter Rule Library

| Noise Type | Definition | Action |
| --- | --- | --- |
| 账号邀请 | Invite codes, registration requests, account exchange, private-contact requests, group/contact promotion. | Mark `irrelevant_noise` with `account_invitation`. |
| 感谢 | "谢谢", "感谢分享", "学习了", "收藏", "mark" without operational content. | Mark `irrelevant_noise` with `thanks_only`. |
| 简单回复 | "好的", "同问", jokes, lightweight agreement, short social reaction. | Mark `irrelevant_noise` with `social_reply` or `too_short`. |
| 无关闲聊 | Tax, sourcing, personal chat, platform complaints, tool promotion without ad/keyword insight. | Mark `irrelevant_noise` with `off_topic`. |
| 情绪表达 | Anger, sarcasm, praise, complaint without actionable ad/keyword content. | Mark as noise or weak signal only if it references a real operational risk. |
| 无数据支撑的绝对判断 | "一定", "绝对", "直接关", "必然有效" without condition, data, or limitation. | Do not create an executable rule; at most `diagnostic_hypothesis` low confidence. |
| 过短评论 | Too short to infer condition or action. | Mark `irrelevant_noise` with `too_short`. |
| 重复评论 | Duplicated or near-duplicated comment content. | Keep one source trace if useful; do not multiply confidence by repetition. |

## Comment Handling

- Comment advice defaults to `medium` or `low confidence`.
- A comment can become `diagnostic_hypothesis` if it proposes a check, explanation, or action with enough context.
- A comment can become `counterexample` if it directly limits a common assumption and has evidence.
- A comment should not become `executable_rule` unless it includes condition, action, reasoning, and limitations.
- Weak agreement or anecdote should remain `comment_signal` and not enter `merged_rules`.

## Rule Rejection Checks

Reject as a rule when:

- no condition is stated,
- no action is stated,
- no reasoning is stated,
- limitations are missing,
- evidence quote is too thin,
- the content is only a summary,
- the source is an irrelevant comment,
- the claim is absolute but unsupported.

## Common Mistakes

- Treating repeated comments as stronger evidence.
- Promoting "低 ACOS 一定好" or "高 ACOS 一定关" into rules.
- Letting tool links or registration comments enter keyword/product-targeting logic because they contain `asin` or `ad` substrings.
- Treating jokes or complaints as market evidence.

## Quality Checklist

- Every comment-derived record has confidence no higher than medium.
- `irrelevant_noise` does not appear in `merged_rules`.
- Account links and registration text are filtered.
- Thanks-only and short social replies are filtered.
- Unsupported absolute claims are downgraded or rejected.
- Evidence quote is short and directly supports the record.
